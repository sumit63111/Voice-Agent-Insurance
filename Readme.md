## HDFC ERGO Voice Insurance Agent – Overview

This project implements a **voice-first sales & support agent** for HDFC ERGO health insurance using **LiveKit**.  
The agent runs as a real-time conversational system with:
- **Deepgram Nova‑3** for speech-to-text (STT)
- **ElevenLabs** for text-to-speech (TTS)
- **OpenAI GPT‑4.1‑mini** as the primary LLM
- A **RAG layer + caching** on top of HDFC ERGO my:Optima Secure documents for accurate answers
- Optional **fine-tuned Gemma‑3‑4B (LoRA)** for domain‑specialized behavior  
  *(Note: due to resource constraints, the fine‑tuned Gemma‑3‑4B model is not currently wired into the live inference path; the main agent uses OpenAI GPT‑4.1‑mini.)*

---

## What This Project Does

- **Create a LiveKit agent orchestration**
  - Real‑time voice agent using `livekit.agents` and `AgentSession`
  - Handles greeting, user turns, and LLM responses

- **Use a modern speech/LLM stack**
  - **STT**: Deepgram Nova‑3 (multilingual, streaming)
  - **TTS**: ElevenLabs (or equivalent neural TTS) for natural outbound audio
  - **LLM**: OpenAI `gpt‑4.1‑mini` (via `voice_agent_orchestraction/llm/llm_service.py`)

- **Implement RAG with caching for fast retrieval**
  - Hybrid **FAISS + BM25** retriever over HDFC ERGO policy PDFs
  - FAISS index + BM25 index **cached in memory** for low‑latency responses
  - Strict policy in `main.py` that forces the agent to **always call RAG** before answering HDFC ERGO questions

- **TTS caching (design)**
  - **TTS cache** can implemented to optimize **cost and latency**, especially for repeated TTS outputs

- **Fine‑tune Gemma‑3‑4B with LoRA**
  - `finetune_lora_uv.py` shows **QLoRA** training for Gemma‑3‑4B
  - Fine‑tuning uses LoRA adapters (parameter‑efficient) instead of full model training
  - The resulting adapter is **for experimentation/offline use**; it is **not integrated into the main online agent** because of GPU/resource limits

- **Transcription logging**
  - `voice_agent_orchestraction/utils/transcription_logger.py` logs **user and agent transcriptions** to file and console
  - Can be enabled/disabled via environment variable

---

## Project Structure (High Level)

- **`main.py`**: Entrypoint for the LiveKit worker + voice agent
- **`voice_agent_orchestraction/`**
  - **`stt/stt_service.py`** – Deepgram Nova‑3 STT client
  - **`tts/tts_service.py`** – TTS client (e.g., ElevenLabs)
  - **`llm/llm_service.py`** – OpenAI GPT‑4.1‑mini configuration
  - **`prompt/agent_instruction.txt`** – System prompt for the agent
  - **`rag/`** – RAG system (chunking, indexing, retrieval, hybrid search)
  - **`utils/transcription_logger.py`** – transcription logging utilities
- **`Telephony/Readme.md`** – telephony + LiveKit trunk/dispatch setup
- **`voice_agent_orchestraction/rag/Readme.md`** – detailed RAG design and configuration
- **`fine tuning/Readme.md`** – fine‑tuning notes for Gemma‑3‑4B with LoRA
- **`samples/Readme.md`** – sample redirection / example usage (e.g., dialogs, payloads)
- **`requirements.txt`** – Python dependencies

---

## Libraries & Technologies Used

- **Core**
  - **Python 3.10+**
  - **PyTorch** (`torch`)

- **Model & Training**
  - **Transformers** (`AutoModelForCausalLM`, `AutoTokenizer`, `BitsAndBytesConfig`, `Trainer`)
  - **PEFT** (`LoraConfig`, `get_peft_model`, `prepare_model_for_kbit_training`)
  - **datasets** (Hugging Face `load_dataset` for JSON/JSONL)

- **Voice & Realtime**
  - **LiveKit Agents SDK** (`livekit.agents`, `AgentSession`, VAD, turn detection)
  - **Deepgram** (streaming STT – Nova‑3)
  - **TTS provider** (e.g., ElevenLabs)

- **RAG & Retrieval**
  - **FAISS** for vector search
  - **OpenAI embeddings** (`text-embedding-3-large` 1024‑dim)
  - **(Optional)** local embedding model (e.g. small **Qwen‑0.6B** encoder) for ultra‑low‑latency, on‑prem embedding generation when you have sufficient GPU/CPU
  - **BM25** (`rank-bm25`) for keyword search

---

## Environment Setup

- **1. Create a virtual environment**
  - **Windows (PowerShell)**:
    - `python -m venv .venv`
    - `.\.venv\Scripts\activate`

- **2. Install dependencies**
  - `pip install -r requirements.txt`

- **3. Configure environment variables**
  - There should be a `code.env.example` / `.env.example` file with all required keys.
  - **Steps:**
    - Copy `.env.example` → `.env`
    - Fill in values:
      - **LiveKit** keys
      - **OPENAI_API_KEY**
      - **DEEPGRAM_API_KEY**
      - **TTS provider keys** (e.g., ElevenLabs)
      - RAG‑related envs (see RAG Readme)

- **4. Optional: enable transcription logging**
  - In `.env`:
    - `TRANSCRIPTION_LOG_ENABLED=true`

---

## How to Run the Agent

- **Terminal / Console mode (for quick testing)**
  - **Command:**
    - `python main.py console`
  - **What it does:**
    - Starts the LiveKit worker in **console audio mode**
    - Uses your microphone + speakers directly from the terminal
    - Good for quick, local manual testing

- **Playground / Telephony mode**
  - **Command:**
    - `python main.py dev`
  - **What it does:**
    - Starts a LiveKit worker suitable for use with:
      - LiveKit Playground (Web UI)
      - Telephony dispatch rules (Exotel, Twilio, etc.)
  - To configure telephony trunks and dispatch rules, see:
    - `Telephony/Readme.md`

---

## RAG: Retrieval‑Augmented Generation

- **What RAG does here**
  - Uses **hybrid retrieval** (FAISS + BM25) on HDFC ERGO my:Optima Secure policy docs
  - Adds strict guardrails so the agent **must** query RAG for:
    - Contact info
    - Policy features, coverage, exclusions, waiting periods
    - Network hospitals and other factual data

- **Caching**
  - FAISS and BM25 indices are:
    - Loaded once on startup
    - Cached in memory for fast retrieval
  - Embedding latency depends on the encoder:
    - With hosted APIs (e.g., OpenAI embeddings) you pay both model + network latency.
    - With a **small local embedding model** (for example a ~0.6B parameter model such as Qwen‑0.6B run on a decent GPU), you can push **per‑query embedding time down to ~60 ms**, making end‑to‑end RAG round‑trips much faster for real‑time voice.

- **Learn more (design & configuration)**
  - See **RAG Readme**:
    - `voice_agent_orchestraction/rag/Readme.md`

---

## Fine‑Tuning (Gemma‑2‑4B with LoRA)

- **Script**
  - `finetune_lora_uv.py` – QLoRA/LoRA training for Gemma‑2‑4B

- **What it does**
  - Loads Gemma‑2‑4B in **4‑bit NF4** mode (QLoRA) using `BitsAndBytesConfig`
  - Applies **LoRA adapters** to key attention and MLP modules
  - Trains on chat‑style JSON/JSONL data (`prompt` + `response`)
  - Saves only LoRA adapter weights to `--output_dir`

- **High‑level run example**
  - Example:
    - `python finetune_lora_uv.py --model_dir /path/to/gemma-2-4b --data_file /path/to/data.jsonl --output_dir ./lora_out`

- **More details**
  - See **Fine Tuning Readme**:
    - `fine tuning/Readme.md`

---

## Telephony Integration

- For detailed **SIP/telephony** integration with LiveKit (e.g., Exotel, Twilio):
  - How to create **Inbound Trunks**
  - How to create **Dispatch Rules**
  - How to verify inbound calls reach the agent

- Refer to:
  - `Telephony/Readme.md`

---

## Samples & Examples

- **Sample dialogs / payloads / prompts**
  - See:
    - `samples/Readme.md`
  - This can be used as a **redirection page** to:
    - Example transcripts
    - Example JSON payloads (e.g., for fine‑tuning)

> **Demo video**
>
> You can watch a short end‑to‑end demo of the voice agent here:  
> [`samples/demo.mp4`](samples/demo.mp4)

---

## End‑to‑End Flow Summary

- **1. User speaks**
  - Audio captured → Deepgram Nova‑3 → text transcript

- **2. Agent reasoning**
  - Transcript sent to LLM (OpenAI GPT‑4.1‑mini or fine‑tuned Gemma‑2‑4B)
  - For any HDFC ERGO question, the agent:
    - Calls **RAG retriever**
    - Combines retrieved chunks with the current conversation
    - Generates a grounded answer

- **3. Response to user**
  - LLM text → TTS (ElevenLabs) → audio back to user
  - Transcriptions logged (if enabled) for both user and agent

---

## If You Want to Extend This Project

- **Possible improvements**
  - Implement and persist a **TTS audio cache** (e.g., file‑based or Redis) keyed by text + voice
  - Add more **domain‑specific fine‑tuning** using `finetune_lora_uv.py`
  - Wire the fine‑tuned Gemma model as an alternative LLM backend

- **Where to look**
  - Agent logic & orchestration: `main.py`, `voice_agent_orchestraction/llm/llm_service.py`
  - RAG internals: `voice_agent_orchestraction/rag/*.py` and its `Readme.md`
  - Telephony: `Telephony/Readme.md`
  - Fine‑tuning: `finetune_lora_uv.py` and `fine tuning/Readme.md`

This README is a high‑level guide; for deep dives, follow the specific Readme files referenced above.
