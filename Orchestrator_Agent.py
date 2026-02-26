import os
import json
from pydantic import BaseModel, ValidationError
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Setup LLM
HF_TOKEN = os.getenv("HF_TOKEN")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

class FoodExtraction(BaseModel):
    # Optional[str] means this field can be a string or None (null in JSON)
    type_of_food: Optional[str] 
    
    # str means this field MUST be a string and cannot be missing
    filter_tags: str

# Get system prompt
with open(r"prompts\orchestrator_agent.txt", 'r', encoding='utf-8') as file:
    system_prompt = file.read()
    


def get_route_json(user_prompt):
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

def validate_route_json(agent_response, current_prompt):
    try:
        FoodExtraction.model_validate_json(agent_response)
        return {
            "res" : "successfully"
        }
    
    except ValidationError as e:
        new_prompt = current_prompt + f"\nLưu ý đừng mắc lỗi sau nhé:\n{e}"
        return {
            "res" : "failed",
            "user_prompt": new_prompt
        }
    
    except Exception as e:
        new_prompt = current_prompt + f"\nLưu ý đừng mắc lỗi sau nhé:\n{e}"
        return {
            "res" : "failed",
            "user_prompt": new_prompt
        }
    
def get_routing_from_orchestrator(user_prompt:str):

    max_retries = 1
    for attempt in range(max_retries):
        # Get response from LLM
        agent_response = get_route_json(user_prompt)
        
        # Validate the response
        valid_status = validate_route_json(agent_response, current_prompt = user_prompt)
        
        # Check if validation passed
        if valid_status["res"] == "successfully":
            return agent_response # Return immediately if correct
        else:
            # If failed, update the prompt with the error message and retry
            user_prompt = valid_status["user_prompt"]

    # If it fails all 3 attempts, return the last generated response 
    return agent_response

# print(get_routing_from_orchestrator(user_prompt="Bạn có thể đề xuất cho tôi các món ăn trưa ở Qui Nhơn không?"))