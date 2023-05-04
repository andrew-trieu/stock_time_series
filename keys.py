import os
from dotenv import load_dotenv

load_dotenv()

def return_keys():
    keys = {"stocks": os.getenv("API_KEY"),
            "kafka_server": os.getenv("KAFKA_SERVER"),
            "postgres_host": os.getenv("POSTGRES_HOST"),
            "postgres_db": os.getenv("POSTGRES_DB"),
            "postgres_port": os.getenv("POSTGRES_PORT"),
            "postgres_user": os.getenv("POSTGRES_USER"),
            "postgres_pass": os.getenv("POSTGRES_PASSWORD")
            }

    return keys


