from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import os

#Spark Session config
spark = (
    SparkSession.builder
    .appName("KafkaToS3Stream")
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3",
            "org.apache.hadoop:hadoop-aws:3.3.4"
        ])
    )
    .getOrCreate()
)

#Hadoop configuration from the Spark context
hadoop_conf = spark._jsc.hadoopConfiguration()

#S3 credentials from environment variables
hadoop_conf.set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
hadoop_conf.set("fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")
hadoop_conf.set("fs.s3a.path.style.access", "true")

schema = StructType([
    StructField("device_id", StringType()),
    StructField("device_type", StringType()),
    StructField("timestamp", StringType()),
    StructField("value", DoubleType()),
    StructField("unit", StringType()),
    StructField("status", StringType())
])

#Reading kafka topic from set localhost
iot_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "iot_sensors")
    .option("startingOffsets", "latest")
    .load()
)

#JSON parser - unnesting / flattening JSON into Spark StructType
iot_parsed = (
    iot_stream
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

#Timestamp conversion (kafka saves 'event_time' as string)
iot_parsed = iot_parsed.withColumn("event_time", col("timestamp").cast(TimestampType()))

#Writing to S3 sink
output_path = "s3a://real-time-processing-kafka-sink/iot_streaming_data/"

query = (
    iot_parsed
    .writeStream
    .format("parquet")
    .option("path", output_path)
    .option("checkpointLocation", "s3a://real-time-processing-kafka-sink/checkpoints/iot_streaming_data/")
    .outputMode("append")
    #Saving mini-batch every 30 seconds
    .trigger(processingTime="30 seconds")
    .start()
)

print("Streamingfrom Kafka → S3 ... (Ctrl+C to stop)")
query.awaitTermination()