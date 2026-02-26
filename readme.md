# Project: Bình Định Tour Guide Assistant (Multi-Agent System)

## Guide line for setup:
1. Open cmd and run command "pip install -r requirements.txt".
2. Init .env file with:
    - HF_TOKEN="Token of Hugging Face here"
    - DB_PASS="PostgreSQL password here"
    - DB_URL = "postgresql://postgres:"""PostgreSQL password here"""@localhost:5432/BinhDinh_TourGuide"
    - data_path = "data\data_raw.xlsx"
2. Run file create_database.py.
3. Run file convert_excel_to_postgre.py.
4. Open cmd and run command "uvicorn main:app --reload".
5. Open cmd and run command "streamlit run app.py".