Portfolio demo project

Short project description: Synthetic data published to local address caught by Spark Streaming and written to S3 parquet table.
Python script creates synthetic IoT devices data with random latency and publishes it to Kafka topic on local address where messages wait to be caught by Spark Streaming, which saves it to AWS S3 bucket in parquet format.

Architecture:

<img width="581" height="61" alt="image" src="https://github.com/user-attachments/assets/79a19d3c-d0d0-473b-9452-5243ab780ba6" />

Attributes:
|"device_type" datatype: "string" values:["temperature", "humidity", "vibration", "co2", "sound"]|
|"device_id" datatype: "string"|
|"timestamp" datatype: "string (ISO 8601 UTC)"|
|"status": datatype: "string" values:["OK", "WARN", "ALERT"]|
|"value" datatype: "number"|

-Units for device_type:
|"temperature": "°C"|
|"humidity": "%"|
|"vibration": "g"|
|"co2": "ppm"|
|"sound": "dB"|


Trigger interval:
Mini-batch is saved with 30 seconds intervals. Spark collects data every 30 seconds and appends it to the target S3 table

Components:
1. synthetic_data_generator.py: generates synthetic data in JSON format for 5 sensors simulating IoT sensor readings data from various devices
2. spark_data_catcher.py: creates Spark Streaming session which catches generated synthetic data from local host to simulate real-time scenario of collecting sensors readings. Data is sent to the S3 bucket in parquet format

Requirements:
# Producer (synthetic_data_generator.py)
kafka-python==2.0.2

# Streaming (spark_data_catcher.py)
pyspark==3.5.3
