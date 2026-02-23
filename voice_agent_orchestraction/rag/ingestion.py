"""
HDFC ERGO Policy Document Ingestion Pipeline
Vector DB: FAISS
Embeddings: OpenAI (text-embedding-3-large, 1024 dimensions)
"""

import json
import os
import pickle
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import faiss
import numpy as np
from openai import OpenAI


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class IngestionConfig:
    """Configuration for the ingestion pipeline"""
    
    # OpenAI Settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    embedding_model: str = "text-embedding-3-large"
    embedding_dimensions: int = 1024
    
    # FAISS Settings
    faiss_index_type: str = "IndexFlatIP"  # Inner Product (cosine similarity for normalized vectors)
    faiss_index_path: str = "faiss_index/hdfc_ergo_policy.index"
    metadata_path: str = "faiss_index/metadata.pkl"
    chunk_mapping_path: str = "faiss_index/chunk_mapping.json"
    
    # Batch Processing
    embedding_batch_size: int = 100  # OpenAI rate limit friendly
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Text Processing
    max_tokens_per_chunk: int = 8000  # Leave buffer for OpenAI token limit
    
    def __post_init__(self):
        os.makedirs(os.path.dirname(self.faiss_index_path), exist_ok=True)


# =============================================================================
# OPENAI EMBEDDING CLIENT
# =============================================================================

class OpenAIEmbedder:
    """Handle OpenAI embedding generation with retry logic"""
    
    def __init__(self, config: IngestionConfig):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.dimensions = config.embedding_dimensions
        
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=text,
            dimensions=self.dimensions
        )
        return response.data[0].embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts with retry logic"""
        embeddings = []
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.client.embeddings.create(
                    model=self.config.embedding_model,
                    input=texts,
                    dimensions=self.dimensions
                )
                embeddings = [item.embedding for item in response.data]
                break
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    raise
        
        return embeddings
    
    def embed_chunks_batched(
        self, 
        chunks: List[Dict], 
        batch_size: Optional[int] = None
    ) -> np.ndarray:
        """Embed all chunks in batches with progress tracking"""
        batch_size = batch_size or self.config.embedding_batch_size
        total_chunks = len(chunks)
        all_embeddings = []
        
        print(f"Embedding {total_chunks} chunks in batches of {batch_size}...")
        
        for i in range(0, total_chunks, batch_size):
            batch = chunks[i:i + batch_size]
            texts = [c['content'] for c in batch]
            
            # Truncate if needed
            texts = [t[:self.config.max_tokens_per_chunk * 4] for t in texts]  # Rough char limit
            
            print(f"  Processing batch {i//batch_size + 1}/{(total_chunks-1)//batch_size + 1}...")
            batch_embeddings = self.embed_batch(texts)
            all_embeddings.extend(batch_embeddings)
            
            # Rate limit protection
            if i + batch_size < total_chunks:
                time.sleep(0.5)
        
        return np.array(all_embeddings, dtype=np.float32)


# =============================================================================
# FAISS INDEX MANAGER
# =============================================================================

class FAISSIndexManager:
    """Manage FAISS index creation, saving, and loading"""
    
    def __init__(self, config: IngestionConfig):
        self.config = config
        self.dimension = config.embedding_dimensions
        self.index = None
        self.chunk_mapping = {}
        
    def create_index(self) -> faiss.Index:
        """Create new FAISS index"""
        # Using IndexFlatIP for cosine similarity (with normalized vectors)
        # Alternative: IndexFlatL2 for Euclidean distance
        self.index = faiss.IndexFlatIP(self.dimension)
        print(f"Created FAISS index: {self.config.faiss_index_type}, dim={self.dimension}")
        return self.index
    
    def normalize_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """L2 normalize vectors for cosine similarity with IndexFlatIP"""
        faiss.normalize_L2(vectors)
        return vectors
    
    def add_vectors(
        self, 
        vectors: np.ndarray, 
        chunks: List[Dict],
        normalize: bool = True
    ):
        """Add vectors to index with metadata tracking"""
        if self.index is None:
            self.create_index()
        
        # Normalize for cosine similarity
        if normalize:
            vectors = self.normalize_vectors(vectors.copy())
        
        # Add to FAISS
        self.index.add(vectors)
        
        # Store metadata mapping
        start_idx = len(self.chunk_mapping)
        for i, chunk in enumerate(chunks):
            faiss_id = start_idx + i
            self.chunk_mapping[faiss_id] = {
                'chunk_id': chunk['id'],
                'content': chunk['content'],
                'metadata': chunk['metadata'],
                'faiss_id': faiss_id
            }
        
        print(f"Added {len(chunks)} vectors to index. Total: {self.index.ntotal}")
    
    def save(self):
        """Save index and metadata to disk"""
        # Save FAISS index
        faiss.write_index(self.index, self.config.faiss_index_path)
        
        # Save metadata
        with open(self.config.metadata_path, 'wb') as f:
            pickle.dump({
                'chunk_mapping': self.chunk_mapping,
                'config': {
                    'model': self.config.embedding_model,
                    'dimensions': self.config.embedding_dimensions,
                    'created_at': datetime.now().isoformat()
                }
            }, f)
        
        # Save human-readable chunk mapping
        with open(self.config.chunk_mapping_path, 'w') as f:
            json.dump(self.chunk_mapping, f, indent=2, default=str)
        
        print(f"Saved index to: {self.config.faiss_index_path}")
        print(f"Saved metadata to: {self.config.metadata_path}")
        print(f"Saved mapping to: {self.config.chunk_mapping_path}")
    
    def load(self) -> Tuple[faiss.Index, Dict]:
        """Load index and metadata from disk"""
        self.index = faiss.read_index(self.config.faiss_index_path)
        
        with open(self.config.metadata_path, 'rb') as f:
            data = pickle.load(f)
            self.chunk_mapping = data['chunk_mapping']
        
        print(f"Loaded index with {self.index.ntotal} vectors")
        return self.index, self.chunk_mapping
    
    def search(
        self, 
        query_vector: np.ndarray, 
        k: int = 5,
        normalize: bool = True
    ) -> Tuple[List[int], List[float]]:
        """Search index for k nearest neighbors"""
        if normalize:
            query_vector = query_vector.copy()
            faiss.normalize_L2(query_vector.reshape(1, -1))
        
        distances, indices = self.index.search(query_vector.reshape(1, -1), k)
        return indices[0].tolist(), distances[0].tolist()


# =============================================================================
# POLICY INGESTION PIPELINE
# =============================================================================

class PolicyIngestionPipeline:
    """Complete pipeline: chunks → embeddings → FAISS index"""
    
    def __init__(self, config: Optional[IngestionConfig] = None):
        self.config = config or IngestionConfig()
        self.embedder = OpenAIEmbedder(self.config)
        self.index_manager = FAISSIndexManager(self.config)
        
    def load_chunks(self, chunks_path: str) -> List[Dict]:
        """Load chunks from JSON file"""
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        print(f"Loaded {len(chunks)} chunks from {chunks_path}")
        return chunks
    
    def validate_chunks(self, chunks: List[Dict]) -> bool:
        """Validate chunk structure before embedding"""
        required_fields = {'id', 'content', 'metadata'}
        
        for i, chunk in enumerate(chunks):
            missing = required_fields - set(chunk.keys())
            if missing:
                raise ValueError(f"Chunk {i} missing fields: {missing}")
            
            if not chunk['content'].strip():
                raise ValueError(f"Chunk {i} has empty content")
        
        print(f"Validated {len(chunks)} chunks")
        return True
    
    def create_enriched_text(self, chunk: Dict) -> str:
        """
        Create enriched text for embedding by adding context headers.
        This improves retrieval by making semantic meaning explicit.
        """
        metadata = chunk['metadata']
        
        # Build context prefix based on chunk type
        context_parts = []
        
        # Section context
        if 'section' in metadata:
            context_parts.append(f"Section {metadata['section']}")
        
        # Type context
        if 'type' in metadata:
            type_labels = {
                'definition': 'Definition',
                'base_coverage': 'Base Coverage',
                'optional_coverage': 'Optional Coverage',
                'waiting_period': 'Waiting Period',
                'standard_exclusion': 'Standard Exclusion',
                'specific_exclusion': 'Specific Exclusion',
                'plan_comparison': 'Plan Comparison'
            }
            context_parts.append(type_labels.get(metadata['type'], metadata['type']))
        
        # Plan context
        if 'plan_name' in metadata:
            context_parts.append(f"Plan: {metadata['plan_name']}")
        elif 'plans' in metadata and len(metadata['plans']) <= 3:
            context_parts.append(f"Plans: {', '.join(metadata['plans'])}")
        
        # Term/Title context
        if 'term' in metadata:
            context_parts.append(f"Term: {metadata['term']}")
        elif 'title' in metadata:
            context_parts.append(f"Topic: {metadata['title']}")
        
        # Assemble enriched text
        if context_parts:
            context_header = " | ".join(context_parts)
            return f"[{context_header}]\n\n{chunk['content']}"
        
        return chunk['content']
    
    def run(
        self, 
        chunks_path: str,
        use_enriched_text: bool = True,
        save_intermediate: bool = True
    ) -> Dict[str, Any]:
        """
        Execute full ingestion pipeline
        
        Args:
            chunks_path: Path to chunks JSON file
            use_enriched_text: Whether to add context headers for better embedding
            save_intermediate: Save embeddings array to disk
        
        Returns:
            Statistics about ingestion
        """
        start_time = time.time()
        
        # Step 1: Load and validate
        print("=" * 60)
        print("STEP 1: Load and Validate Chunks")
        print("=" * 60)
        chunks = self.load_chunks(chunks_path)
        self.validate_chunks(chunks)
        
        # Step 2: Prepare texts for embedding
        print("\n" + "=" * 60)
        print("STEP 2: Prepare Texts")
        print("=" * 60)
        
        if use_enriched_text:
            print("Creating enriched texts with context headers...")
            texts = [self.create_enriched_text(c) for c in chunks]
            # Store enriched text for later use
            for i, chunk in enumerate(chunks):
                chunk['_enriched_text'] = texts[i]
        else:
            texts = [c['content'] for c in chunks]
        
        # Step 3: Generate embeddings
        print("\n" + "=" * 60)
        print("STEP 3: Generate Embeddings")
        print(f"Model: {self.config.embedding_model}")
        print(f"Dimensions: {self.config.embedding_dimensions}")
        print("=" * 60)
        
        embeddings = self.embedder.embed_chunks_batched(chunks)
        
        # Save intermediate if requested
        if save_intermediate:
            embeddings_path = "faiss_index/embeddings.npy"
            np.save(embeddings_path, embeddings)
            print(f"Saved embeddings to: {embeddings_path}")
        
        # Step 4: Create FAISS index
        print("\n" + "=" * 60)
        print("STEP 4: Build FAISS Index")
        print("=" * 60)
        
        self.index_manager.create_index()
        self.index_manager.add_vectors(embeddings, chunks, normalize=True)
        
        # Step 5: Save index
        print("\n" + "=" * 60)
        print("STEP 5: Save Index and Metadata")
        print("=" * 60)
        
        self.index_manager.save()
        
        # Statistics
        elapsed = time.time() - start_time
        stats = {
            'total_chunks': len(chunks),
            'embedding_dimensions': self.config.embedding_dimensions,
            'index_size': self.index_manager.index.ntotal,
            'elapsed_seconds': elapsed,
            'chunks_per_second': len(chunks) / elapsed,
            'index_path': self.config.faiss_index_path,
            'metadata_path': self.config.metadata_path
        }
        
        print("\n" + "=" * 60)
        print("INGESTION COMPLETE")
        print("=" * 60)
        print(f"Total chunks indexed: {stats['total_chunks']}")
        print(f"Embedding dimensions: {stats['embedding_dimensions']}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print(f"Speed: {stats['chunks_per_second']:.2f} chunks/second")
        
        return stats


# =============================================================================
# RETRIEVAL INTERFACE (for testing)
# =============================================================================

class PolicyRetriever:
    """Query interface for the FAISS index"""
    
    def __init__(self, config: Optional[IngestionConfig] = None):
        self.config = config or IngestionConfig()
        self.embedder = OpenAIEmbedder(self.config)
        self.index_manager = FAISSIndexManager(self.config)
        self._load_index()
        
    def _load_index(self):
        """Load existing index"""
        self.index_manager.load()
        
    def retrieve(
        self, 
        query: str, 
        k: int = 5,
        plan_filter: Optional[str] = None,
        section_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User query text
            k: Number of results to retrieve
            plan_filter: Optional plan name to filter results
            section_filter: Optional section to filter results
        
        Returns:
            List of retrieved chunks with scores
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        query_vector = np.array([query_embedding], dtype=np.float32)
        
        # Search index
        indices, scores = self.index_manager.search(query_vector, k=k * 3)  # Over-fetch for filtering
        
        # Build results
        results = []
        for idx, score in zip(indices, scores):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue
                
            chunk_data = self.index_manager.chunk_mapping.get(idx)
            if not chunk_data:
                continue
            
            # Apply filters
            metadata = chunk_data['metadata']
            
            if plan_filter:
                applicable_plans = (
                    metadata.get('plans', []) + 
                    metadata.get('inbuilt_for', []) +
                    metadata.get('optional_for', [])
                )
                if plan_filter not in applicable_plans:
                    continue
            
            if section_filter:
                if not metadata.get('section', '').startswith(section_filter):
                    continue
            
            results.append({
                'chunk_id': chunk_data['chunk_id'],
                'content': chunk_data['content'],
                'metadata': metadata,
                'score': float(score),
                'faiss_id': idx
            })
            
            if len(results) >= k:
                break
        
        return results
    
    def format_results(self, results: List[Dict]) -> str:
        """Format results for display"""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"RETRIEVED {len(results)} RESULTS")
        output.append(f"{'='*60}")
        
        for i, r in enumerate(results, 1):
            meta = r['metadata']
            output.append(f"\n--- Result {i} (Score: {r['score']:.4f}) ---")
            output.append(f"Chunk ID: {r['chunk_id']}")
            output.append(f"Section: {meta.get('section', 'N/A')}")
            output.append(f"Type: {meta.get('type', 'N/A')}")
            
            if 'plan_name' in meta:
                output.append(f"Plan: {meta['plan_name']}")
            elif 'plans' in meta:
                output.append(f"Plans: {', '.join(meta['plans'][:3])}")
            
            if 'term' in meta:
                output.append(f"Term: {meta['term']}")
            elif 'title' in meta:
                output.append(f"Title: {meta['title']}")
            
            output.append(f"\nContent:\n{r['content'][:500]}...")
            output.append("-" * 40)
        
        return "\n".join(output)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution for ingestion"""
    
    # Initialize configuration
    config = IngestionConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        embedding_model="text-embedding-3-large",
        embedding_dimensions=1024,
        embedding_batch_size=50  # Conservative for rate limits
    )
    
    # Verify API key
    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    # Run ingestion
    pipeline = PolicyIngestionPipeline(config)
    
    stats = pipeline.run(
        chunks_path="hdfc_ergo_policy_chunks.json",
        use_enriched_text=True,
        save_intermediate=True
    )
    
    # Test retrieval
    print("\n" + "=" * 60)
    print("TESTING RETRIEVAL")
    print("=" * 60)
    
    retriever = PolicyRetriever(config)
    
    test_queries = [
        "What is Pre-Existing Disease waiting period?",
        "How much room rent is covered in Optima Lite?",
        "Is obesity surgery covered?",
        "What are the conditions for Plus Benefit?",
        "Tell me about Global Health Cover"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        results = retriever.retrieve(query, k=3)
        print(retriever.format_results(results))


def quick_test():
    """Quick test with existing index"""
    config = IngestionConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    retriever = PolicyRetriever(config)
    
    while True:
        query = input("\nEnter query (or 'quit'): ").strip()
        if query.lower() == 'quit':
            break
        
        plan = input("Filter by plan (or press Enter): ").strip() or None
        
        results = retriever.retrieve(query, k=3, plan_filter=plan)
        print(retriever.format_results(results))


if __name__ == "__main__":
    # Run full ingestion
    main()
    
    # Or for testing only:
    # quick_test()