from kafka import KafkaProducer
from json import dumps
from time import sleep

# always start ZooKeeper and Kafka broker server

producer = KafkaProducer(bootstrap_servers = ["localhost:9092"], 
                         value_serializer = lambda x: dumps(x).encode("utf-8"))

for num in range(1000):
    data = {"number": num}
    # producer.send(topic, value = message val)
    producer.send("numtest", value = data)
    sleep(3)

