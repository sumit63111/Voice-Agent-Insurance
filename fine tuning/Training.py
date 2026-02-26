# finetune_lora_uv.py
"""
LoRA/QLoRA fine-tuning for Gemma-3-4B.
"""

import argparse
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType


def build_chat_training_example(tokenizer, prompt, response):
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response},
    ]
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )


def preprocess(batch, tokenizer, max_length):
    enc = tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=max_length,
        return_tensors="pt",
    )
    enc["labels"] = enc["input_ids"].clone()
    return enc


def main():
    parser = argparse.ArgumentParser()

    # Main params
    parser.add_argument("--model_dir", type=str, required=True)
    parser.add_argument("--data_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="./lora_out")

    # Training hyperparams
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--per_device_train_batch_size", type=int, default=1)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=3e-4)
    parser.add_argument("--max_length", type=int, default=1024)

    # LoRA params (NEW)
    parser.add_argument("--lora_r", type=int, default=8)
    parser.add_argument("--lora_alpha", type=int, default=16)
    parser.add_argument("--lora_dropout", type=float, default=0.05)

    parser.add_argument("--full_finetune", action="store_true")

    args = parser.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"DEVICE = {device}")

    # ----------------------- TOKENIZER -----------------------
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_dir, use_fast=False, trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ----------------------- MODEL LOAD -----------------------
    if not args.full_finetune:
        print("\n== Loading Gemma-3-4B in 4-bit NF4 mode (QLoRA) ==\n")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

        model = AutoModelForCausalLM.from_pretrained(
            args.model_dir,
            device_map="auto",
            quantization_config=bnb_config,
            trust_remote_code=True,
        )

        model = prepare_model_for_kbit_training(model)
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    else:
        print("\n== Loading FULL Gemma-3-4B ==\n")
        model = AutoModelForCausalLM.from_pretrained(
            args.model_dir,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
        )
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    # ----------------------- LORA CONFIG -----------------------
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ]

    print("Applying LoRA to:", target_modules)

    lora_cfg = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules=target_modules,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )

    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()

    # ----------------------- DATASET -----------------------
    print(f"\nLoading dataset: {args.data_file}")
    ds = load_dataset("json", data_files=args.data_file, split="train")

    ds = ds.map(
        lambda e: {"text": build_chat_training_example(tokenizer, e["prompt"], e["response"])},
        remove_columns=ds.column_names,
    )

    ds = ds.map(
        lambda batch: preprocess(batch, tokenizer, args.max_length),
        batched=True,
        remove_columns=ds.column_names,
    )
    ds.set_format("torch")

    # ----------------------- TRAINING -----------------------
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        bf16=True,
        logging_steps=20,
        save_steps=500,
        save_total_limit=2,
        remove_unused_columns=False,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds,
        tokenizer=tokenizer,
    )

    print("\n==== STARTING TRAINING ====\n")
    trainer.train()

    print("\n==== SAVING LORA ADAPTER ====\n")
    model.save_pretrained(args.output_dir)
    print("DONE.")


if __name__ == "__main__":
    main()
