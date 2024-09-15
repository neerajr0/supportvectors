

import instructor
from pydantic import BaseModel
from openai import OpenAI
from typing import List

class SensitivePrompt(BaseModel):
    prompt: str


class SensitivePrompts(BaseModel):
    prompts: List[SensitivePrompt]


# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

def fetch_response(messages, model):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_model=model
    )

    return completion

def generate_prompts():
    
    with open('prompt.txt') as file:
        output: SensitivePrompts = fetch_response(
            [
                {
                    "role": "user",
                    "content": file.read()
                }
            ],
            SensitivePrompts
        )
        return output

if __name__ == "__main__":

    with open('sensitive_prompts.py', 'w') as file:
        file.write(str(generate_prompts()))