from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer("numtest", 
                         bootstrap_servers = ["localhost: 9092"],
                         auto_offset_reset = "earliest",
                         enable_auto_commit = True,
                         group_id = "my-group",
                         value_deserializer = lambda x: loads(x.decode("utf-8"))
                         )

for idx, message in enumerate(consumer):
    message = message.value
    print(f"{idx}. {message}")


# to execute -- open new command prompt and run producer.py
# open new command command prompt and run consumer.py, will print output from producer
