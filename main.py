from agents.Orchestrator_Agent import *
from agents.Response_Agent import *
from agents.Planning_Agent import *
from tools.get_food import *
from tools.get_restaurant import *
from tools.get_destination import *
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Init app
app = FastAPI(title="Quy Nhon AI Tour Guide API", description="API cho trợ lý du lịch ảo")

class ChatRequest(BaseModel):
    user_prompt: str

# ==========================================
# LOGIC FUNCTIONS
# ==========================================
def get_context(user_prompt):
    planning_flag = False
    routing_json_string = get_routing_from_orchestrator(user_prompt)
    print("Orchestrator Routing:", routing_json_string)

    try:
        routing_dict = json.loads(routing_json_string)
    except json.JSONDecodeError:
        print("Error: The routing JSON string is not valid. Please check the format!")
        routing_dict = {}

    context = ""

    if "food" in routing_dict:
        food_data = routing_dict.get("food", {}) 
        type_of_food = food_data.get("type_of_food")
        filter_tags = food_data.get("filter_tags")
        food_context = get_food_list(type_of_food, filter_tags)
        context += f"\nThông tin về món ăn:\n{food_context}\n"

    if "restaurant" in routing_dict:
        restaurant_data = routing_dict.get("restaurant", {})
        filter_tags = restaurant_data.get("filter_tags")
        restaurant_context = get_restaurant(filter_tags)
        context += f"\nThông tin về nhà hàng:\n{restaurant_context}\n"

    if "destination" in routing_dict:
        destination_data = routing_dict.get("destination", {})
        filter_tags = destination_data.get("filter_tags")
        destination_context = get_destination(filter_tags)
        context += f"\nThông tin về địa điểm:\n{destination_context}\n"

    if "planning" in routing_dict:
        planning_flag = True
        planning_data = routing_dict.get("planning", {})
        
        time = planning_data.get("time") or "3 ngày"
        budget = planning_data.get("budget") or "5 triệu"
        prefer = planning_data.get("prefer") or "hải sản, biển"

        destination_context = get_destination(prefer)
        restaurant_context = get_restaurant(prefer)
        
        context += f"\n=========================================\n"
        context += f"YÊU CẦU LẬP LỊCH TRÌNH:\n"
        context += f"- Thời gian: {time}\n"
        context += f"- Ngân sách: {budget}\n"
        context += f"- Ưu tiên/Phong cách: {prefer}\n\n"
        context += f"NGUYÊN LIỆU GỢI Ý (Chỉ dùng các dữ liệu dưới đây để xếp lịch):\n\n"
        context += f"[1. ĐỊA ĐIỂM THAM QUAN]\n{destination_context}\n\n"
        context += f"[2. NHÀ HÀNG / QUÁN ĂN]\n{restaurant_context}\n\n"
        context += f"=========================================\n"
    
    return {"planning_flag" : planning_flag, "context" : context}

def get_response(user_prompt: str, context: dict):
    end_context = context["context"]
    final_user_prompt = user_prompt + f"\nSau đây là các thông tin liên quan cho bạn tham khảo:\n{end_context}"
    
    if context["planning_flag"] == False:
        end_response = get_agent_response(final_user_prompt)
    else:
        end_response = get_planning_agent_response(final_user_prompt)

    return {"agent_response" : end_response}

# ==========================================
# XÂY DỰNG API ENDPOINT
# ==========================================
@app.post("/api/chat")
def api_get_answer(request: ChatRequest):
    """
    Return answer for user
    """
    try:
        
        ctx = get_context(request.user_prompt)
        result = get_response(request.user_prompt, ctx)
        
        return {
            "status": "success",
            "data": result["agent_response"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")