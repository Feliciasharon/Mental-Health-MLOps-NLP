import json
import time
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP = "host.docker.internal:9092"
TOPIC_NAME = "predictions"

def main():
    print("Starting Kafka consumer...")

    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="mlops-consumer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    for message in consumer:
        data = message.value
        print("Received message:", data)

        # Simulate processing
        time.sleep(1)

if __name__ == "__main__":
    main()
