from io import BytesIO
from PIL import Image
import ray
import os

def perform(data):
    print(data[0])
    return {
        "path": "abc",
        "text": "abc"
    }

ds = ray.data.read_binary_files(
    "s3://minioadmin:minioadmin@normal_02?scheme=http&endpoint_override=192.168.0.8%3A9000",
    include_paths=True
)

pipe = ds.map(perform)

pipe.take(10)
