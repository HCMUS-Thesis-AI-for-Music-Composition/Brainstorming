import os
import torch
from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import GPT2LMHeadModel, AutoTokenizer
from peft import PeftModel
from infer_stage1 import infer_prompt

# Initialize FastAPI
app = FastAPI()

# Define the directory for the saved model and tokenizer
save_directory = "./custom_gpt2_model_ver2"
checkpoint_directory = "./output_9_6/checkpoint-45000"


# Load model and tokenizer during startup
@app.on_event("startup")
def load_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    base_model = GPT2LMHeadModel.from_pretrained(save_directory, device_map={"": "cpu"})
    model = PeftModel.from_pretrained(
        base_model, checkpoint_directory, device_map={"": "cpu"}
    )


class InferenceRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate_text(request: InferenceRequest):
    prompt = infer_prompt(request.prompt)
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate tokens
    generated_ids = model.generate(
        input_ids,
        max_length=512,
        do_sample=True,
        temperature=0.2,
        num_beams=4,
        eos_token_id=tokenizer.encode("</s>")[0],
    )

    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return {"generated_text": generated_text}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=3000)
print(infer_prompt("Có đàn piano"))
