## Gemma-3 Insurance Agent Fine-Tuning (QLoRA + LoRA)

This folder contains my end‑to‑end setup for fine‑tuning `google/gemma-3-4b-it` into an insurance sales/ support agent, using QLoRA (4‑bit quantization + LoRA adapters).  
The goal is to train a model that can answer health‑insurance related questions in English and Hindi (Hinglish), and then run it as an interactive console chatbot.

---

## High‑Level Overview

- **Base model**: `google/gemma-3-4b-it`
- **Task**: Instruction / dialogue tuning for an insurance sales agent
- **Method**: QLoRA (4‑bit quantization) + LoRA adapters on key attention/MLP layers
- **Training data**:
  - `fine tuning/data/insurance_sales_data_expanded.jsonl` – used in Colab via the notebook
  - JSONL with multi‑turn dialogues (`dialogue` field) or single‑turn `prompt`/`response`
- **Outputs**:
  - LoRA adapter directory: `./gemma-3-finetuned` (created by the notebook)
  - Script‑based adapter directory: `--output_dir` from `Training.py`
- **Inference**: Load base Gemma‑3 in 4‑bit + merge LoRA adapter via `peft.PeftModel`, then run a simple text chat loop.

---

## Project Structure (this folder)

- **`Training.ipynb`**
  - Colab notebook used to run the complete QLoRA fine‑tuning and interactive chat.
- **`Training.py`**
  - Stand‑alone Python script (CLI) to run the same style of LoRA/QLoRA fine‑tuning from the command line.
- **`data/insurance_sales_data_expanded.jsonl`**
  - Training data with insurance conversations.
- **`Readme.md`**
  - This documentation.

There is also a top‑level script `finetune_lora_uv.py` that is effectively the same as `fine tuning/Training.py` and can be used in the same way.

---

## Training Data Format

I experimented with **two slightly different data formats**, depending on whether I was in the notebook or using the CLI script.

### 1. Multi‑turn dialogue format (used in `Training.ipynb`)

Each JSON line has a `dialogue` field that contains a whole conversation as text, e.g.:

```json
{
  "dialogue": "User: क्या Hospitalization के बाद के खर्चे भी Cover होते हैं?\nAgent: जी हाँ, hospitalization से पहले और बाद के खर्चे भी plan के अनुसार cover हो सकते हैं...\nUser: अगर मैं Claim नहीं करता तो क्या फायदा मिलेगा?\nAgent: जी हाँ, आपको no-claim bonus जैसा benefit मिल सकता है..."
}
```

Inside the notebook:

- I **parse this single string** into a sequence of chat messages with roles:
  - Lines starting with `"User:"` → `{"role": "user", "content": ...}`
  - Lines starting with `"Agent:"` → `{"role": "assistant", "content": ...}`
- I then treat the **last assistant turn** as the target to predict and the earlier turns as context.
- I apply Gemma’s **chat template** (`tokenizer.apply_chat_template`) to get the model’s expected prompt format.
- Inputs are truncated/padded to a fixed `max_length`, and labels are masked with `-100` for the prompt part so that loss is only computed on the assistant answer.

This allows the model to learn from **multi‑turn, realistic insurance sales dialogues**.

### 2. Single‑turn prompt/response format (used by `Training.py` / `finetune_lora_uv.py`)

Here, the JSONL has two fields: `prompt` and `response`:

```json
{
  "prompt": "Customer asks: \"क्या Hospitalization के बाद के खर्चे भी cover होते हैं?\" Answer like an insurance agent in Hindi.",
  "response": "जी हाँ, ज़्यादातर health insurance plans में hospitalization से पहले और बाद के खर्चे भी cover होते हैं..."
}
```

The script builds a chat example as:

- User message → `{"role": "user", "content": prompt}`
- Assistant message → `{"role": "assistant", "content": response}`
- Then it runs `tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)` and treats the full text as both inputs and labels (standard causal LM fine‑tuning).

---

## Notebook Workflow (`Training.ipynb`)

The notebook captures the full fine‑tuning pipeline, roughly in this order:

### 1. Install dependencies

Using pip:

```bash
pip install -U transformers peft bitsandbytes datasets accelerate
```

Libraries used:

- **transformers** – models, tokenizers, Trainer
- **peft** – LoRA / QLoRA utilities
- **bitsandbytes** – 4‑bit quantization
- **datasets** – loading JSONL dataset
- **accelerate** – underlying hardware acceleration

### 2. Authenticate with Hugging Face (optional but recommended)

The notebook uses:

```python
from huggingface_hub import notebook_login
notebook_login()
```

This allows accessing gated models and optionally pushing results back to the Hub.

### 3. Configuration and tokenizer

Key configuration in the notebook:

- `MODEL_ID = "google/gemma-3-4b-it"`
- `DATA_PATH = "/content/insurance_sales_data_expanded.jsonl"`
- `OUTPUT_DIR = "./gemma-3-finetuned"`
- `max_length = 1024`
- `batch_size = 1`
- `grad_acc = 8`
- `lr = 2e-4`
- `epochs = 1`
- `lora_r = 8`, `lora_alpha = 16`

Tokenizer setup:

- Load `AutoTokenizer.from_pretrained(MODEL_ID)`
- Ensure a valid `pad_token` (fall back to `eos_token` if needed)
- Use Gemma’s built‑in `apply_chat_template` for correct chat formatting

### 4. Data preprocessing

In `Training.ipynb`, I:

1. **Parse dialogues** using `parse_dialogue_to_messages(dialogue_str)`:
   - Converts `"User:"` / `"Agent:"` lines into a message list.
2. **Build examples** in `build_example(example)`:
   - Split context vs. target (last assistant turn).
   - Build a **prompt** by applying the chat template with `add_generation_prompt=True`.
   - Tokenize prompt and target separately, then concatenate.
   - Create `labels` where:
     - Prompt tokens → `-100` (ignored in loss)
     - Target tokens → actual token IDs
   - Construct:
     - `input_ids`
     - `attention_mask`
     - `labels`
     - `token_type_ids` (all zeros; added for completeness)
   - Truncate or pad everything to `max_length`.
3. Use `datasets.load_dataset("json", data_files=DATA_PATH, split="train")` and `map` to apply the above transformation.

Finally, I call `dataset.set_format("torch")` so the Trainer can consume the tensors directly.

### 5. Model loading (QLoRA)

I load the base Gemma‑3 model in **4‑bit** using `BitsAndBytesConfig`:

- `load_in_4bit=True`
- `bnb_4bit_compute_dtype=torch.bfloat16`
- `bnb_4bit_use_double_quant=True`
- `bnb_4bit_quant_type="nf4"`

Then:

- `AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=bnb_config, device_map="auto", trust_remote_code=True)`
- Prepare for k‑bit training:
  - `prepare_model_for_kbit_training(model)`
  - `model.gradient_checkpointing_enable()`
  - `model.config.use_cache = False` (for compatibility with gradient checkpointing)

### 6. LoRA configuration

I attach LoRA adapters with:

- **Target modules**: `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`
- **Rank and scaling**:
  - `r = 8`
  - `lora_alpha = 16`
  - `lora_dropout = 0.05`
- **Task type**: `TaskType.CAUSAL_LM`

The model is wrapped via:

```python
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

This keeps only a small percentage of parameters trainable (~0.38%) while the rest stay frozen in 4‑bit.

### 7. Training (Trainer API)

I configure `TrainingArguments`:

- `output_dir = OUTPUT_DIR`
- `per_device_train_batch_size = 1`
- `gradient_accumulation_steps = 8`
- `learning_rate = 2e-4`
- `num_train_epochs = 1` (adjustable)
- `bf16 = True`
- `logging_steps = 10`
- `save_strategy = "epoch"`
- `report_to = "none"` (no external logging)

Then create and run the Trainer:

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer,
)

trainer.train()
```

After training:

```python
model.save_pretrained(OUTPUT_DIR)
```

This saves only the **LoRA adapter weights** into `./gemma-3-finetuned`.

### 8. GPU memory cleanup

After training, I explicitly:

- Delete large objects (`trainer`, `model`, `base_model` if present)
- Call `gc.collect()`
- Call `torch.cuda.empty_cache()`

This recovers VRAM in the Colab session before loading the model again for inference.

### 9. Inference: Insurance Agent Chatbot

For inference, I:

1. **Reload the tokenizer** from `MODEL_ID`.
2. **Reload base Gemma‑3** in 4‑bit with the same `BitsAndBytesConfig`.
3. **Attach the trained adapter**:

```python
from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained(...4-bit config...)
model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)  # ADAPTER_PATH = "./gemma-3-finetuned"
model.eval()
```

4. **Define a helper function** `agent_response(user_input)` that:
   - Wraps the user query as a chat message:
     - `{"role": "user", "content": "Answer as a helpful insurance agent: <user_input>"}`  
   - Applies the chat template with `add_generation_prompt=True`.
   - Generates a response with:
     - `max_new_tokens=128`
     - `temperature=0.4`
     - `repetition_penalty=1.2`
     - `no_repeat_ngram_size=3`
     - Appropriate `eos_token_id` and `pad_token_id`
   - Strips the prompt from the output and decodes only the newly generated tokens.
5. **Run a simple console chat loop**:

```python
print("--- Insurance Agent Bot Active (Type 'quit' to stop) ---")
while True:
    user_query = input("You: ")
    if user_query.lower() in ["quit", "exit", "stop"]:
        break
    print("Agent:", agent_response(user_query))
```

This produced good responses, including Hindi/Hinglish examples like:

- `“क्या Hospitalization के बाद के खर्चे भी Cover होते हैं?”`
- `“Waiting period कितना होता है?”`
- `“Plus benefit के बारे में बताइए।”`

---

## Command‑Line Training Script (`Training.py`)

`Training.py` mirrors the logic of the notebook but as a **pure Python script** that you can run locally or on a server.

### What it does

1. Parses arguments:

- `--model_dir` – base model (e.g. `google/gemma-3-4b-it` or a local path)
- `--data_file` – path to JSONL training data (with `prompt` and `response`)
- `--output_dir` – where to save the LoRA adapter (default: `./lora_out`)
- `--num_train_epochs` – number of training epochs (default: `3`)
- `--per_device_train_batch_size` – batch size per GPU (default: `1`)
- `--gradient_accumulation_steps` – grad accumulation for effective batch size (default: `8`)
- `--learning_rate` – LR (default: `3e-4`)
- `--max_length` – max sequence length (default: `1024`)
- LoRA hyperparams: `--lora_r`, `--lora_alpha`, `--lora_dropout`
- `--full_finetune` – if set, load full fp16/bf16 model instead of 4‑bit QLoRA

2. Loads the tokenizer and ensures `pad_token` is set.

3. Loads the model:

- **Default**: 4‑bit NF4 (QLoRA) with `BitsAndBytesConfig`, `device_map="auto"`.
- If `--full_finetune` is passed: load full Gemma‑3 with `torch_dtype=torch.bfloat16`.

4. Prepares the model for training (`prepare_model_for_kbit_training`, gradient checkpointing, `use_cache=False`).

5. Sets up **LoRA** with the same target modules as in the notebook.

6. Loads the dataset:

- `datasets.load_dataset("json", data_files=args.data_file, split="train")`
- `build_chat_training_example()` builds:
  - `messages = [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]`
  - Uses `tokenizer.apply_chat_template(..., tokenize=False, add_generation_prompt=False)` to build the final text.
- `preprocess()` tokenizes, pads to `max_length`, and sets `labels = input_ids.clone()`.

7. Creates `TrainingArguments` and a Hugging Face `Trainer`, then calls `trainer.train()`.

8. Saves the adapter to `output_dir` with `model.save_pretrained(args.output_dir)`.

### Example usage

From the root of the project (adjust paths as needed):

```bash
python "fine tuning/Training.py" ^
  --model_dir "google/gemma-3-4b-it" ^
  --data_file "fine tuning/data/insurance_sales_data_expanded.jsonl" ^
  --output_dir "fine tuning/gemma-3-insurance-lora" ^
  --num_train_epochs 1 ^
  --per_device_train_batch_size 1 ^
  --gradient_accumulation_steps 8 ^
  --learning_rate 2e-4
```

On Linux/macOS, the same command without `^` line continuations:

```bash
python "fine tuning/Training.py" \
  --model_dir "google/gemma-3-4b-it" \
  --data_file "fine tuning/data/insurance_sales_data_expanded.jsonl" \
  --output_dir "fine tuning/gemma-3-insurance-lora" \
  --num_train_epochs 1 \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --learning_rate 2e-4
```

---

## How to Reproduce My Results

1. **Hardware**
   - A GPU with at least ~8 GB VRAM (e.g. T4) is enough thanks to 4‑bit QLoRA.
2. **Environment**
   - Python 3.9+ recommended.
   - Install dependencies:

```bash
pip install -U "transformers>=4.46.0" peft bitsandbytes datasets accelerate
```

3. **Get the data**
   - Place your JSONL at `fine tuning/data/insurance_sales_data_expanded.jsonl`
     - Either with `dialogue` (for the notebook), or `prompt` / `response` (for `Training.py`).

4. **Option A – Use the notebook (`Training.ipynb`)**
   - Open in Google Colab.
   - Enable GPU, run all cells.
   - This will:
     - Download Gemma‑3‑4B‑IT.
     - Preprocess the insurance dialogues.
     - Fine‑tune with QLoRA.
     - Save the adapter to `./gemma-3-finetuned`.
     - Start an interactive insurance agent chat loop.

5. **Option B – Use the script (`Training.py`)**
   - Run the command‑line example above.
   - After training, load the adapter with the same pattern used in the notebook’s inference section.

---

## Notes for People Reading This on GitHub

- This repository shows a **practical, GPU‑friendly QLoRA workflow** for turning Gemma‑3 into a domain‑specific assistant (here: health insurance sales).
- You can **swap in your own domain** simply by:
  - Changing the JSONL data.
  - Adjusting the “insurance agent” style prompt text in the inference function.
- The LoRA adapter directory (e.g. `gemma-3-finetuned`) can be:
  - Loaded locally with `PeftModel.from_pretrained`.
  - Or pushed to the Hugging Face Hub and shared.

If you have any questions or want to adapt this setup to a different domain (e.g. banking, support, sales), you can reuse the same pipeline with new data and minimal code changes.
