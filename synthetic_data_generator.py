import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

#Kafka config
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "iot_sensors"

#Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

#Adding sensors as synthetic environment
devices = [
    {"device_id": "sensor_001", "type": "temperature"},
    {"device_id": "sensor_002", "type": "humidity"},
    {"device_id": "sensor_003", "type": "vibration"},
    {"device_id": "sensor_004", "type": "co2"},
    {"device_id": "sensor_005", "type": "sound"}
]

#Synthetic data script
def generate_iot_event(device):
    base_values = {
        "temperature": round(random.uniform(18, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "vibration": round(random.uniform(0, 1), 3),
        "co2": random.randint(400, 1200),
        "sound": random.randint(30, 90)
    }

    event = {
        "device_id": device["device_id"],
        "device_type": device["type"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "value": base_values[device["type"]],
        "unit": {
            "temperature": "°C",
            "humidity": "%",
            "vibration": "g",
            "co2": "ppm",
            "sound": "dB"
        }[device["type"]],
        "status": random.choice(["OK", "WARN", "ALERT"])
    }
    return event

#Sending generated data to Kafka Topic - script picks random sensor and sends its data to given Kafka topic
if __name__ == "__main__":
    print(f"Starting Kafka producer → topic `{KAFKA_TOPIC}`")

    try:
        while True:
            device = random.choice(devices)
            event = generate_iot_event(device)
            producer.send(KAFKA_TOPIC, value=event)
            print(f"Sent: {event}")
            #Simulating randomized delay between sensor reading (events)
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("\n Stopped by user")
    finally:
        producer.close()