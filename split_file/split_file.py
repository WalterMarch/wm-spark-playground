from datetime import datetime, timezone
from pyspark.sql import SparkSession


def split_file(input_path, output_prefix):
    spark = SparkSession.builder.appName("SplitFile").getOrCreate()

    lines = spark.sparkContext.textFile(input_path)
    lines.repartition(20000).saveAsTextFile(output_prefix)

    spark.stop()


datetime_string = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
input_file_path = (
    "/workspaces/wm-spark-playground/split_file/cord_19_embeddings_2022-06-02.csv"
)
output_file_prefix = (
    f"/workspaces/wm-spark-playground/split_file/output_{datetime_string}"
)

split_file(input_file_path, output_file_prefix)
