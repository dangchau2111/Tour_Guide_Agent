import os
import json
from pydantic import BaseModel, ValidationError
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# LLM SETUP AND CONFIGURATION
# ==========================================
HF_TOKEN = os.getenv("HF_TOKEN")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

class FoodExtraction(BaseModel):
    """
    Schema for validating food-related data extraction.
    """
    # Optional[str]: Can be a string or None (null in JSON)
    type_of_food: Optional[str] 
    
    # str: Field MUST be a string and is required
    filter_tags: str

# ==========================================
# PROMPT LOADING
# ==========================================
# Read the system prompt from the specified text file
with open(r"prompts\orchestrator_agent.txt", 'r', encoding='utf-8') as file:
    system_prompt = file.read()

# ==========================================
# CORE LOGIC FUNCTIONS
# ==========================================
def get_route_json(user_prompt):
    """
    Sends the user's prompt to the LLM and retrieves the raw content response.
    """
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
    """
    Validates if the LLM's response matches the Pydantic schema.
    If validation fails, returns the error formatted for a retry prompt.
    """
    try:
        FoodExtraction.model_validate_json(agent_response)
        return {
            "res" : "successfully"
        }
    
    except ValidationError as e:
        # Append validation error details to prompt for self-correction
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
    
def get_routing_from_orchestrator(user_prompt: str):
    """
    Main entry point for the Orchestrator. 
    Includes a retry mechanism to handle schema validation failures.
    """
    max_retries = 1
    for attempt in range(max_retries):
        # 1. Fetch raw JSON response from LLM
        agent_response = get_route_json(user_prompt)
        
        # 2. Validate response against schema
        valid_status = validate_route_json(agent_response, current_prompt=user_prompt)
        
        # 3. Check validation results
        if valid_status["res"] == "successfully":
            return agent_response # Return correct JSON immediately
        else:
            # If validation fails, update prompt with error and retry
            user_prompt = valid_status["user_prompt"]

    # If retries are exhausted, return the last generated response as a fallback
    return agent_response

# Example usage:
# print(get_routing_from_orchestrator(user_prompt="Bạn có thể đề xuất cho tôi các món ăn trưa ở Qui Nhơn không?"))