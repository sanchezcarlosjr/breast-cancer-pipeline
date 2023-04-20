import ray
from ray.data.datasource import FileExtensionFilter
import requests
import json
from decouple import config 

ds = ray.data.read_binary_files(
    config('FILESYSTEM'),
    include_paths=True,
    partition_filter=FileExtensionFilter("LJPEG")
)

def perform(batch):
    from ljpeg.ljpeg import read,od_correct
    from ljpeg.utils import get_ics_info_from_text
    from ray.data.datasource import Datasource, NumpyDatasource
    import tempfile
    import requests
    import cv2
    import numpy 
    import numpy as np
    import os.path
    import requests_cache
    requests_cache.install_cache(cache_name='minio_cache', backend='sqlite', expire_after=180)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(batch[0][1])
        temp_file.flush()
        temp_path = temp_file.name
    ics = batch[0][0].split(".")[-3].replace("_", "-")+".ics"
    url = config('REST')+ics
    ics_text = requests.get(url, stream=True).text
    ics_info = get_ics_info_from_text(ics_text.split("\n"), os.path.basename(ics)[0])
    name = os.path.basename(batch[0][0]).split(".")[-2]
    W = ics_info[name]['width']
    H = ics_info[name]['height']
    image = read(temp_path)
    os.remove(temp_path)
    if W != image.shape[1]:
        image = image.reshape((H, W))
    # gray correction
    image = od_correct(image, ics_info)
    image = numpy.interp(image, (0.0, 4.0), (255, 0))
    image = image.astype(numpy.uint8)

    image = image[70:image.shape[0]-250, 30:image.shape[0]]

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    # Use Otsu's binarization
    _, binary_image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Apply morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    closed_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, kernel)
    # Apply the mask to the original image
    image = cv2.bitwise_and(image, image, mask=closed_image)
    
    # Find the contours in the image
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    image = image[y:y+h, x:x+w]

    # Apply magma
    image = cv2.convertScaleAbs(image)
    image = cv2.applyColorMap(image, cv2.COLORMAP_MAGMA)

    image = cv2.resize(image, (224, 336))

    # save numpy file
    dsImage = ray.data.from_numpy([image])
    path = os.path.dirname(batch[0][0])+"/"+name+".npy"
    dsImage.write_numpy(config('UPLOADS').replace("REPLACE_THIS", path))

    return batch


ds.map_batches(perform).take_all()
