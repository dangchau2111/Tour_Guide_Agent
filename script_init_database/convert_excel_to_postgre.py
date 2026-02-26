import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2


DB_URL = "postgresql://postgres:dmdemacia123@localhost:5432/BinhDinh_TourGuide"
engine = create_engine(DB_URL)

file_path = "data\data_raw.xlsx"


sheets_config = {
    "nha_hang": {
        "table_name": "restaurant",
        "columns": {
            "Name": "name",
            "address_new": "address",
            "Cuisine": "category",
            "Description": "description"
        }
    },
    "dia_diem": {
        "table_name": "destination",
        "columns": {
            "name": "name",
            "Category": "category",
            "Address_new": "address",
            "describe": "description"
        }
    },
    "am_thuc": {
        "table_name": "food",
        "columns": {
            "ten_mon_an": "name",
            "loai_mon_an": "category",
            "Tags": "tags",
            "Description": "description"
        }
    }
}


for sheet_name, config in sheets_config.items():
    table_name = config["table_name"]
    col_mapping = config["columns"]
    
    try:
        
        cols_to_read = list(col_mapping.keys())
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=cols_to_read)
        
        df = df.rename(columns=col_mapping)
        
        df = df.fillna("")
        df = df.astype(str)
        
       
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
        
    except Exception as e:
        print(f"Error, Sheet name: '{sheet_name}': {e}\n")
