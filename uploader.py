from minio.sse import SseS3
from minio import Minio
from minio.commonconfig import ComposeSource

client = Minio("127.0.0.1:9000", "minioadmin", "minioadmin", secure=False)

sources = [
    ComposeSource("normal_02", "case0200/A_0200_1.LEFT_CC.LJPEG")
]

result = client.compose_object(
    "normal_02",
    "case0200/A_0200_1.LEFT_CC.LJPEG",
    sources,
    metadata={"size": "123x414141"}
)
print(result.object_name, result.version_id)
