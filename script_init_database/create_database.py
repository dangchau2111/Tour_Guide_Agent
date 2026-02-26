from sqlalchemy import create_engine, text
import psycopg2


USER = "postgres"
PASSWORD = "dmdemacia123" 
HOST = "localhost"
PORT = "5432"
NEW_DB_NAME = "BinhDinh_TourGuide"


default_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres"

engine_default = create_engine(default_url, isolation_level="AUTOCOMMIT")

try:
    with engine_default.connect() as conn:

        check_db_query = text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{NEW_DB_NAME}'")
        db_exists = conn.execute(check_db_query).scalar()

        if not db_exists:


            conn.execute(text(f"CREATE DATABASE \"{NEW_DB_NAME}\""))
            

except Exception as e:
    print(f"Error: {e}")
