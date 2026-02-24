from Orchestrator_Agent import *
from tools.get_food import *
import json

user_prompt = "Bạn có thể đề xuất cho tôi vài món ăn vặt không?"

routing_json_string = get_routing_from_orchestrator(user_prompt)
print(routing_json_string)
#Food
if routing_json_string:
    routing_dict = json.loads(routing_json_string)
    type_of_food = routing_dict.get("type_of_food")
    filter_tags = routing_dict.get("filter_tags")

    food_context = get_food_list(type_of_food, filter_tags)
    print(food_context)