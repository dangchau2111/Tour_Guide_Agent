import json
from pydantic import BaseModel, ValidationError
from typing import Optional

# 1. Define the expected JSON structure (The Blueprint)
# BaseModel is the core class of Pydantic used for data validation
class FoodExtraction(BaseModel):
    # Optional[str] means this field can be a string or None (null in JSON)
    type_of_food: Optional[str] 
    
    # str means this field MUST be a string and cannot be missing
    filter_tags: str

# 2. Simulate responses from the LLM
# Scenario A: The LLM followed instructions perfectly
llm_response_perfect = '{"type_of_food": "món chính", "filter_tags": "ăn sáng"}'

# Scenario B: The LLM made a mistake (forgot the 'filter_tags' key)
llm_response_bad = '{"type_of_food": "đồ tráng miệng"}'

# 3. Create a function to validate the output
def validate_llm_json(raw_json_string: str):
    """
    Takes a raw JSON string from the LLM and validates it against the FoodExtraction model.
    """
    try:
        # .model_validate_json() will automatically parse the string and check all rules
        validated_data = FoodExtraction.model_validate_json(raw_json_string)
        
        print("✅ Validation Successful!")
        # Notice how you can access the data using dot notation (validated_data.filter_tags)
        # instead of dictionary keys (data["filter_tags"])
        print(f"Type of food: {validated_data.type_of_food}")
        print(f"Filter tags: {validated_data.filter_tags}\n")
        
        return validated_data
        
    except ValidationError as e:
        # If the JSON does not match the model, Pydantic raises a ValidationError
        print("❌ Validation Failed! The LLM output is incorrect.")
        print(f"Error Details:\n{e}\n")
        return None
    except Exception as e:
        # Catch other errors, like completely malformed JSON strings (e.g., missing brackets)
        print("❌ Critical Error: The string is not even a valid JSON.")
        return None

# --- Testing the Validator ---

print("--- Testing Scenario A (Perfect JSON) ---")
valid_result = validate_llm_json(llm_response_perfect)

print("--- Testing Scenario B (Bad JSON) ---")
invalid_result = validate_llm_json(llm_response_bad)