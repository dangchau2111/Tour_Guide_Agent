from Orchestrator_Agent import *
from Response_Agent import *
from tools.get_food import *
from tools.get_restaurant import *
from tools.get_destination import *
import json

user_prompt = "Tôi muốn tìm các nhà hàng hải sản"

routing_json_string = get_routing_from_orchestrator(user_prompt)
print(routing_json_string)
# Convert the routing JSON string to a Python dictionary
try:
    routing_dict = json.loads(routing_json_string)
    
except json.JSONDecodeError:
    print("Error: The routing JSON string is not valid. Please check the format!")
    routing_dict = {}

context = ""

# Call get Food tool if the routing JSON is valid and contains necessary information
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


user_prompt += f"\nSau đây là các thông tin liên quan cho bạn tham khảo:\n{context}"
response = get_agent_response(user_prompt)
print(response)