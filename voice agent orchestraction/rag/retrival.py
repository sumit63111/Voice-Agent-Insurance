import asyncio
import logging
import os
import pickle
import json
from pathlib import Path

import faiss
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from livekit.agents.llm import function_tool
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

script_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=script_dir / ".env", override=True)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

USE_RAG = os.getenv("USE_RAG", "true").lower() == "true"

# FAISS Index Directory (single index location)
FAISS_INDEX_DIR = os.getenv("FAISS_INDEX_DIR", os.path.join(script_dir, "faiss_index"))

# OpenAI Embedding Model Configuration
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))  # text-embedding-3-large configured to output 1024 dimensions
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_NAME = os.getenv("FAISS_INDEX_NAME", "hdfc_ergo_policy")  # Index file name without extension

# ---------------------------------------------------------------------------
# Caching for Performance Optimization
# ---------------------------------------------------------------------------

# Cache embeddings and FAISS indexes to avoid reloading on every retrieval
_cached_embeddings = None
_cached_faiss_db = None  # Cache for FAISS database
_embedding_dimension = None
_dimension_verified = False
_faiss_load_count = 0  # Track FAISS index loads
_faiss_first_load_time = None

# ---------------------------------------------------------------------------
# FAISS Retrieval Functions
# ---------------------------------------------------------------------------


def build_local_embeddings():
    """
    Build OpenAI embeddings.
    Ensures embedding and retrieval dimensions are consistent.
    Cached after first call.
    """
    global _cached_embeddings
    
    if _cached_embeddings is None:
        try:
            logger.info("Initializing OpenAI embeddings")
            logger.info(f"Expected dimensions: {EMBEDDING_DIMENSIONS}")
            
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            
            # Initialize OpenAI embeddings with specified dimensions
            _cached_embeddings = OpenAIEmbeddings(
                openai_api_key=OPENAI_API_KEY,
                model="text-embedding-3-large",
                dimensions=EMBEDDING_DIMENSIONS  # Set to 1024 to match ingestion
            )
            logger.info("✅ OpenAI embeddings model loaded and cached")
        except Exception as exc:
            logger.error(f"Failed to initialize OpenAI embedding model: {exc}")
            raise ValueError(f"Failed to initialize OpenAI embeddings: {exc}")
    
    return _cached_embeddings


def get_embedding_dimensions(embeddings) -> int:
    """
    Get the embedding dimensions from the embeddings model.
    This ensures consistency between embedding and retrieval.
    Cached after first call.
    """
    global _embedding_dimension
    
    if _embedding_dimension is None:
        try:
            test_vec = embeddings.embed_query("test")
            _embedding_dimension = len(test_vec)
            logger.info(f"Embedding dimension verified: {_embedding_dimension}")
        except Exception as exc:
            logger.error(f"Failed to get embedding dimensions: {exc}")
            raise
    
    return _embedding_dimension


def get_faiss_db():
    """
    Get or load the FAISS database.
    Cached after first load to avoid reloading on every retrieval.
    
    Returns:
        FAISS database
    """
    global _cached_faiss_db, _dimension_verified, _faiss_load_count, _faiss_first_load_time
    
    if _cached_faiss_db is None:
        # Loading from disk for the first time
        import time
        load_start = time.time()
        logger.info(f"🔄 Loading FAISS index from DISK (first load)...")
        logger.info(f"   Index directory: {FAISS_INDEX_DIR}")
        
        embeddings = build_local_embeddings()
        
        # Load raw FAISS index from disk
        try:
            index_path = Path(FAISS_INDEX_DIR) / f"{FAISS_INDEX_NAME}.index"
            metadata_path = Path(FAISS_INDEX_DIR) / "metadata.pkl"
            chunk_mapping_path = Path(FAISS_INDEX_DIR) / "chunk_mapping.json"
            
            if not index_path.exists():
                raise FileNotFoundError(f"FAISS index file not found: {index_path}")
            
            # Load raw FAISS index
            faiss_index = faiss.read_index(str(index_path))
            logger.info(f"✅ Loaded raw FAISS index with {faiss_index.ntotal} vectors")
            
            # Load chunk mapping
            if chunk_mapping_path.exists():
                with open(chunk_mapping_path, 'r', encoding='utf-8') as f:
                    chunk_mapping = json.load(f)
                logger.info(f"✅ Loaded chunk mapping with {len(chunk_mapping)} chunks")
            else:
                logger.warning("⚠️ chunk_mapping.json not found, creating empty mapping")
                chunk_mapping = {}
            
            # Create LangChain Documents from chunk mapping
            documents = []
            for chunk_id, chunk_data in chunk_mapping.items():
                content = chunk_data.get('content', '')
                metadata = chunk_data.get('metadata', {})
                documents.append(Document(page_content=content, metadata=metadata))
            
            # Ensure documents match index size
            if len(documents) != faiss_index.ntotal:
                logger.warning(
                    f"⚠️ Document count ({len(documents)}) doesn't match index size ({faiss_index.ntotal}). "
                    f"Padding or truncating documents."
                )
                if len(documents) < faiss_index.ntotal:
                    # Pad with empty documents
                    documents.extend([Document(page_content="")] * (faiss_index.ntotal - len(documents)))
                else:
                    # Truncate
                    documents = documents[:faiss_index.ntotal]
            
            # Create FAISS vectorstore from raw index and documents
            # Create minimal vectorstore first, then replace components
            _cached_faiss_db = FAISS.from_documents(
                [Document(page_content="dummy")],
                embeddings
            )
            # Replace with loaded index
            _cached_faiss_db.index = faiss_index
            # Update docstore with all documents
            from langchain_community.docstore.in_memory import InMemoryDocstore
            _cached_faiss_db.docstore = InMemoryDocstore()
            _cached_faiss_db.index_to_docstore_id = {}
            for i, doc in enumerate(documents):
                _cached_faiss_db.docstore.add({i: doc})
                _cached_faiss_db.index_to_docstore_id[i] = i
            
            logger.info(f"✅ Created FAISS vectorstore with {len(documents)} documents")
            
        except Exception as exc:
            logger.error(f"Failed to load FAISS index from {FAISS_INDEX_DIR}: {exc}")
            raise ValueError(
                f"Failed to load FAISS index. "
                f"Please ensure the index exists at {FAISS_INDEX_DIR}."
            )
        
        load_time = time.time() - load_start
        _faiss_load_count += 1
        _faiss_first_load_time = time.time()
        
        logger.info(
            f"✅ FAISS index loaded from DISK in {load_time:.3f}s "
            f"(load count: {_faiss_load_count})"
        )
        
        # Verify dimensions only once during first load
        if not _dimension_verified:
            embedding_dim = get_embedding_dimensions(embeddings)
            index_dim = _cached_faiss_db.index.d if hasattr(_cached_faiss_db.index, 'd') else None
            
            if index_dim:
                if index_dim != embedding_dim:
                    logger.error(
                        f"Dimension mismatch! Index has {index_dim} dimensions, "
                        f"but embeddings have {embedding_dim} dimensions."
                    )
                    # Clear the cached database
                    _cached_faiss_db = None
                    raise ValueError(
                        f"Embedding dimension mismatch. "
                        f"Index expects {index_dim} dimensions, but current model produces {embedding_dim} dimensions. "
                        f"Please rebuild the FAISS index."
                    )
                else:
                    logger.info(
                        f"✅ Dimension match confirmed: Index ({index_dim}) and embeddings ({embedding_dim}) both use {embedding_dim} dimensions"
                    )
                    _dimension_verified = True
            else:
                logger.warning("Could not determine index dimensions")
                _dimension_verified = True
        
        logger.info(f"✅ FAISS index cached in MEMORY - future retrievals will use cached version")
    else:
        # Using cached version from memory
        logger.debug(f"💾 Using FAISS index from MEMORY cache (no disk access)")
    
    return _cached_faiss_db


def retrieve_from_faiss(query: str, k: int = 4) -> str:
    """
    Retrieve documents from FAISS index using similarity search.
    
    Args:
        query: Search query
        k: Number of results to return (default: 4)
    
    Returns:
        Retrieved documents as formatted text
    """
    import time
    total_start = time.time()
    try:
        # Get cached FAISS database (no reload needed after first load)
        load_start = time.time()
        db = get_faiss_db()
        load_time = time.time() - load_start
        
        # Determine if this was from cache or disk
        load_source = "MEMORY (cached)" if _cached_faiss_db is not None and _faiss_load_count == 1 else "DISK"
        if load_time < 0.001:  # Very fast = likely from cache
            load_source = "MEMORY (cached)"
        
        # Time: Similarity search
        search_start = time.time()
        results = db.similarity_search(query, k=k)
        search_time = time.time() - search_start
        
        # Time: Format results
        format_start = time.time()
        result_text = "\n\n".join([doc.page_content for doc in results])
        format_time = time.time() - format_start
        
        total_time = time.time() - total_start
        
        # Log performance metrics with load source
        logger.info(
            f"⚡ FAISS Retrieval Performance Metrics:\n"
            f"   • Index load ({load_source}): {load_time:.3f}s\n"
            f"   • Similarity search: {search_time:.3f}s\n"
            f"   • Result formatting: {format_time:.3f}s\n"
            f"   • TOTAL RETRIEVAL TIME: {total_time:.3f}s ({total_time*1000:.1f}ms)\n"
            f"   • Query: '{query[:50]}{'...' if len(query) > 50 else ''}' | k={k}\n"
            f"   • Cache status: Load count={_faiss_load_count}, "
            f"Cached={'Yes' if _cached_faiss_db is not None else 'No'}"
        )
        
        return result_text
    except Exception as exc:
        total_time = time.time() - total_start
        logger.error(
            f"FAISS retrieval failed after {total_time:.3f}s: {exc}"
        )
        return f"Error retrieving documents: {exc}"


# ---------------------------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------------------------


@function_tool(
    name="RAG_RETRIEVER",
    description=(
        "**⚠️ RAG-FIRST POLICY FOR SPECIFIC HDFC ERGO POLICY QUESTIONS**\n\n"
        "**ALWAYS call this tool for:**\n"
        "- Specific policy terms: Waiting periods (pre-existing diseases, specified diseases, 30-day waiting period), exact coverage limits, room rent limits, ICU limits\n"
        "- Coverage details: Secure Benefit, Plus Benefit, Protect Benefit, Automatic Restore Benefit, Cumulative Bonus, Aggregate Deductible, AYUSH Treatment, Organ Donor Expenses\n"
        "- Claim procedures: Cashless claim process, reimbursement claim process, documentation required, time limits for claim submission, pre-authorization requirements\n"
        "- Network hospitals: Cashless network hospital information, network provider details\n"
        "- Exclusions: Standard exclusions (Section C.2), specific exclusions (Section C.3), waiting period exclusions (Section C.1)\n"
        "- Optional covers: Global Health Cover (Emergency & Planned), Overseas Travel Secure, E-Opinion for Critical Illness, Preventive Health Check-up\n"
        "- Policy definitions: Hospital, Day Care Centre, AYUSH Hospital, Medical Practitioner, Pre-Existing Disease, Sum Insured, Policy Year, etc.\n"
        "- Policy terms & conditions: Renewal terms, portability, migration, grace period, free look period, moratorium period, fraud provisions\n"
        "- Geography coverage: India coverage, global coverage details, overseas treatment conditions\n"
        "- **ALL technical policy queries requiring exact HDFC ERGO my:Optima Secure policy wording**\n\n"
        "**DON'T call this tool for:**\n"
        "- Simple greetings, acknowledgments: \"Okay\", \"Haan\", \"Boliye\", \"Yes go ahead\"\n"
        "- Initial greeting and discovery questions\n"
        "- General benefits explanation during sales pitch (use training knowledge from agent_instruction.txt)\n"
        "- Common objections handling (respond naturally first using training knowledge)\n"
        "- Market insights (medical inflation, coverage gaps)\n"
        "- When asking discovery questions\n"
        "- Closing attempts\n\n"
        "**When in doubt about HDFC ERGO policy details → CALL THIS TOOL**\n\n"
        "**Query Format Examples:**\n"
        "- Waiting period: \"HDFC ERGO my:Optima Secure pre-existing disease waiting period Section C.1\"\n"
        "- Coverage: \"HDFC ERGO my:Optima Secure Secure Benefit Plus Benefit coverage details\"\n"
        "- Claims: \"HDFC ERGO my:Optima Secure claim procedure documentation required\"\n"
        "- Exclusions: \"HDFC ERGO my:Optima Secure standard exclusions Section C.2\"\n"
        "- Optional covers: \"HDFC ERGO my:Optima Secure Global Health Cover overseas treatment\"\n"
        "- Network: \"HDFC ERGO cashless network hospital list\"\n"
        "- Protect Benefit: \"HDFC ERGO my:Optima Secure Protect Benefit non-medical expenses covered\"\n\n"
        "**Response Protocol:**\n"
        "(1) Detect specific policy question → (2) Call RAG_RETRIEVER with clear query → (3) Synthesize retrieved information naturally → "
        "(4) Paraphrase in conversational language (NEVER copy-paste verbatim) → (5) If RAG returns no results, admit limitation and offer escalation"
    ),
)
async def rag_retriever_tool(query: str) -> str:
    """
    Retrieve information from FAISS knowledge base.
    
    Args:
        query: Search query
    
    Returns:
        Retrieved context with instructions for the agent
    """
    import time
    tool_start = time.time()
    
    try:
        if not query or not query.strip():
            return "Please provide a search query to retrieve information."
        
        logger.info(f"🔍 RAG Query: {query.strip()}")

        context = retrieve_from_faiss(query.strip(), k=4)
        if not context or not context.strip():
            tool_time = time.time() - tool_start
            logger.info(f"⏱️ RAG Time: {tool_time:.3f}s ({tool_time*1000:.1f}ms)")
            return (
                f"I couldn't find relevant information in the knowledge base for your query. "
                "[INSTRUCTION: You MUST now immediately respond to the user explaining you couldn't find "
                "the information. Do not wait. Respond now in the detected language.]"
            )

        tool_time = time.time() - tool_start
        logger.info(f"⏱️ RAG Time: {tool_time:.3f}s ({tool_time*1000:.1f}ms)")
        return (
            f"Here's what I found in the knowledge base:\n\n{context}\n\n"
            f"[INSTRUCTION: You MUST now immediately synthesize this information "
            f"and provide a natural spoken response to the user's question. "
            f"Do not wait. Respond now in the detected language.]"
        )
    except Exception as exc:
        tool_time = time.time() - tool_start
        logger.error(
            f"⏱️ RAG Time (error): {tool_time:.3f}s - Error: {exc}", exc_info=True
        )
        return (
            f"Error retrieving information: {exc} "
            f"[INSTRUCTION: You MUST now immediately respond to the user explaining there was an error. "
            f"Do not wait. Respond now in the detected language.]"
        )




# ---------------------------------------------------------------------------
# Main entrypoints for main agent script
# ---------------------------------------------------------------------------


def get_prompt_file_path() -> str:
    prompt_file = os.getenv("PROMPT_FILE", "prompt/agent_instruction.txt")
    file_path = Path(prompt_file)
    if not file_path.is_absolute():
        file_path = script_dir.parent / prompt_file
    return str(file_path)


def get_additional_instructions() -> str:
    return ""


def get_tools(session_ref=None, ctx_ref=None):
    """
    Get list of tools available to the agent.
    
    Args:
        session_ref: Reference to the AgentSession (optional, not used currently)
        ctx_ref: Reference to the JobContext (optional, not used currently)
    
    Returns:
        List of tool functions
    """
    tools = [rag_retriever_tool]
    logger.info("✅ RAG retriever tool added")
    return tools


async def initialize():
    """Initialize Findoc use case module"""
    logger.info("Findoc use case module initialized")
    
    if not USE_RAG:
        logger.info("USE_RAG is disabled for Findoc use case")
        return

    logger.info("\n" + "="*60)
    logger.info("Initializing RAG System")
    logger.info("="*60)

    # Pre-load and verify embeddings during initialization
    # This ensures everything is cached and ready for fast retrieval
    try:
        emb = build_local_embeddings()
        embedding_dim = get_embedding_dimensions(emb)
        logger.info(
            f"Using OpenAI embeddings with {embedding_dim} dimensions "
            f"(configured: {EMBEDDING_DIMENSIONS})"
        )
        
        # Ensure configured dimensions match actual dimensions
        if embedding_dim != EMBEDDING_DIMENSIONS:
            logger.warning(
                f"Dimension mismatch: configured {EMBEDDING_DIMENSIONS}, "
                f"actual {embedding_dim}. Using actual dimension."
            )
    except Exception as exc:
        logger.warning(f"Could not determine embedding dimension: {exc}")

    # Check and pre-load FAISS index
    logger.info(f"\n🔵 Checking FAISS index at {FAISS_INDEX_DIR}...")
    faiss_dir = Path(FAISS_INDEX_DIR)
    if not faiss_dir.exists() or not any(faiss_dir.iterdir()):
        logger.warning(
            f"⚠️ FAISS index missing at {FAISS_INDEX_DIR}. "
            f"Please ensure the index exists at this location."
        )
        logger.warning("RAG retrieval will not work until index is available.")
    else:
        logger.info("FAISS index found - pre-loading and verifying...")
        try:
            # Pre-load the FAISS index during initialization to cache it
            db = get_faiss_db()
            index_dim = db.index.d if hasattr(db.index, 'd') else None
            embedding_dim = get_embedding_dimensions(build_local_embeddings())
            if index_dim:
                logger.info(
                    f"✅ FAISS index pre-loaded from DISK and cached in MEMORY: "
                    f"{index_dim} dimensions match embeddings ({embedding_dim})\n"
                    f"   Future retrievals will use the cached version (no disk access)"
                )
            else:
                logger.info("✅ FAISS index pre-loaded from DISK and cached in MEMORY (dimension verification skipped)")
        except Exception as exc:
            logger.warning(f"Could not pre-load FAISS index: {exc}")
    
    logger.info("\n" + "="*60)
    logger.info("RAG System Initialization Complete")
    logger.info("="*60 + "\n")


__all__ = [
    "initialize",
    "get_tools",
    "get_prompt_file_path",
    "get_additional_instructions",
    "rag_retriever_tool",
]




