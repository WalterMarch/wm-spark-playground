from datetime import datetime, timezone
import os
from pyspark.sql import SparkSession


def split_file(input_path, output_prefix):
    spark = SparkSession.builder.appName("SplitFile").getOrCreate()

    print(f"Reading file @ {datetime.now()}")
    lines = spark.sparkContext.textFile(input_path)
    partition_count = lines.count() // 100
    print(f"Start saving files @ {datetime.now()}")
    lines.repartition(partition_count).saveAsTextFile(output_prefix)
    spark.stop()
    print(f"End saving files @ {datetime.now()}")


def clean_up(output_prefix):
    file_list = os.listdir(output_prefix)
    for file in file_list:
        if file.endswith(".crc"):
            os.remove(os.path.join(output_prefix, file))


datetime_string = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
input_file_path = (
    "/workspaces/wm-spark-playground/split_file/cord_19_embeddings_2022-06-02.csv"
)
output_file_prefix = (
    f"/workspaces/wm-spark-playground/split_file/output_{datetime_string}"
)

print(f"Starting @ {datetime.now()}")
split_file(input_file_path, output_file_prefix)
print(f"Start clean up @ {datetime.now()}")
clean_up(output_file_prefix)
print(f"Ending @ {datetime.now()}")
