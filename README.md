Project description: Synthetic data published to local address caught by Spark Streaming and written to S3 parquet table

Synthetic data python script creates IoT devices data with random latency and publishes it to Kafka topic on local address where messages wait to be catched by Spark Streaming engine which saves it to AWS S3 bucket

Synthetic data generator attributes:
> Values generated for metrics devices: "temperature": "°C", "humidity" "%", "vibration": "g", "co2": "ppm", "sound": "dB"
> Descriptive attributes: "device_id", "timestamp", "status": ["OK", "WARN", "ALERT"]
