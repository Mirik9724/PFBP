import sys
import os
sys.path.append(os.path.dirname(__file__))

import torch
from sintAudi import *
from transformers import AutoModelForCausalLM, AutoTokenizer#, BitsAndBytesConfig

model = None
tokenizer = None

async def loadModel():
    global model, tokenizer

    model_name = "Qwen/Qwen2.5-0.5B-Instruct"

    # bnb_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_compute_dtype=torch.float16
    # )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.float32,
        device_map=None
    )

    model.to("cpu")
    model.eval()
    model = torch.compile(model)
    torch.set_num_threads(os.cpu_count())

    print("Load model")


async def useBot(msg):
    messages = [
        {"role": "user", "content": msg}
    ]

    # У Qwen есть свой chat template
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=96,
            temperature=0.7,
            do_sample=True
        )

    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[-1]:],
        skip_special_tokens=True
    )

    return response


if __name__ == "__main__":
    import asyncio

    async def test():
        sp = Voice()
        await loadModel()
        sp.say(await useBot("Расскажи о Пушкине"))

    asyncio.run(test())