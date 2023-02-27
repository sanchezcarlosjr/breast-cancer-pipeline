from io import BytesIO
from PIL import Image
import ray
import os

def perform(data):
    path, img = data
    print(path)
    return {
        "path": path,
        "text": "abc"
    }

uri = "s3://minioadmin:minioadmin@?scheme=http&endpoint_override=localhost%3A9000"

ds = ray.data.read_binary_files(
    uri,
    include_paths=True)


# Perform OCR on the images
results = ds.map(perform)

results.take(10)
