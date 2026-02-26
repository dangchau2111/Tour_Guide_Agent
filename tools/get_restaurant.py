import pandas as pd
import difflib
import os
from dotenv import load_dotenv
load_dotenv()

data_path = os.getenv("data_path")

def get_restaurant( filter_tags : str):
    df_restaurant = pd.read_excel(data_path, sheet_name='nha_hang')
    filter_tags_lower = str(filter_tags).lower()
    sim_scores_list = []
    for tag in df_restaurant["Cuisine"]:
        tag_lower = str(tag).lower()

        # Calculate similarity score (returns a float between 0.0 and 1.0)
        score = difflib.SequenceMatcher(None, filter_tags_lower, tag_lower).ratio()

        # Convert score to percentage for easier reading
        score_percentage = round(score * 100, 2)

        sim_scores_list.append(score_percentage)
    df_restaurant["sim_score"] = sim_scores_list
    # print(df_restaurant[["Cuisine", "sim_score"]].sort_values(by="sim_score", ascending=False))
    df_result = df_restaurant.nlargest(5, 'sim_score').copy()
    return df_result[["Name", "address_new", "Description"]]
