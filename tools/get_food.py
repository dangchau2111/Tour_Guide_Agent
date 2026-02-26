import pandas as pd
import difflib
import os
import unicodedata
from dotenv import load_dotenv
load_dotenv()

data_path = os.getenv("data_path")

def get_food_list(type_of_food : str, filter_tags : str):
    df_food = pd.read_excel(data_path, sheet_name='am_thuc')

    # Filter by type of food first
    allowed_types = ["món chính", "món phụ", "đồ ăn vặt", "đồ tráng miệng", "đồ uống"]

    if str(type_of_food).lower() in allowed_types:
        type_of_food = str(type_of_food).lower()
    else:
        type_of_food = None

    if type_of_food is not None:
        df_filtered = df_food[df_food['loai_mon_an'].str.lower() == type_of_food].copy()
    else:
        df_filtered = df_food


    # Filter by tags
    filter_tags_lower = str(filter_tags).lower()
    sim_scores_list = []

    for tag in df_filtered["Tags"]:
        tag_lower = str(tag).lower()

        # Calculate similarity score (returns a float between 0.0 and 1.0)
        score = difflib.SequenceMatcher(None, filter_tags_lower, tag_lower).ratio()

        # Convert score to percentage for easier reading
        score_percentage = round(score * 100, 2)

        sim_scores_list.append(score_percentage)

    df_filtered["sim_score"] = sim_scores_list
    
    df_result = df_filtered.nlargest(5, 'sim_score').copy()

    return df_result[["ten_mon_an", "Description"]]

