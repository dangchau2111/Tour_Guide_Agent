import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Setup LLM
HF_TOKEN = os.getenv("HF_TOKEN")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# Get system prompt
with open(r"prompts\response_agent.txt", 'r', encoding='utf-8') as file:
    system_prompt = file.read()

def get_agent_response(user_prompt):
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct:together",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
    )
    agent_response = completion.choices[0].message.content
    return agent_response
