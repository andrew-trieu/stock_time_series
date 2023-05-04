from json import dumps, loads
import os
import time

from dotenv import load_dotenv
from kafka import KafkaConsumer, KafkaProducer
import requests
import psycopg
from psycopg.rows import dict_row

from keys import return_keys


load_dotenv()

# websocket api for real-time market data?
BASE_URL = "https://api.twelvedata.com"
SYMBOL = "APPL"
KAFKA_BOOTSTRAP_SERVER = 
KAFKA_TOPIC
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER

keys = return_keys()  # get rid of this - use os.getenv directly

producer = KafkaProducer(bootstrap_servers = [f"{keys['kafka_server']}"],
                         value_serializer = lambda x: dumps(x).encode("utf-8"))
consumer = KafkaConsumer("train_dataset", 
                         bootstrap_servers = [f"{keys['kafka_server']}"],
                         auto_offset_reset = "earliest",
                         enable_auto_commit = True,
                         value_deserializer = lambda x: loads(x.decode("utf-8"))
                         )

conn_info = f"host = {keys['postgres_host']} " \
            f"port = {keys['postgres_port']} " \
            f"dbname = {keys['postgres_db']} " \
            "connect_timeout = 10 " \
            f"user = {keys['postgres_user']}" \
            f"password = {keys['postgres_pw']}"
postgres_conn = psycopg.connect(conninfo = conn_info,
                             row_factory = dict_row)
cursor = postgres_conn.cursor()  # cursor enables execution of database operations

# each index in time_series_data is a dictionary of form:
# symbol (str), interval (str), open (fl), high (fl), close (fl), date (str)
time_series_data = []

url = BASE_URL + f"/time_series?symbol={SYMBOL}&interval=1day&apikey={keys['stocks']}"
with requests.get(url, params = {"outputsize": 365, "format": "JSON"}) as r:
    if not r.ok:
        raise RuntimeError(f"Error code: {r.status_code} - {r.text}")
    response = r.json()
    interval = response["meta"]["interval"]
    for timestep in response["values"]: 
        sorted_data = dict(symbol = SYMBOL,
                           open = f"{timestep['open']}",
                           high = f"{timestep['high']}",
                           close = f"{timestep['close']}",
                           date = f"{timestep['datetime']}")
        time_series_data.append(sorted_data)

# sending data to kafka topic
for entry in time_series_data:
    producer.send("train_dataset", value = entry)

# keep calling the API with kafka, check for 


