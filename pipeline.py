import ray
from ray.data.datasource import FileExtensionFilter
from decouple import config 

ds = ray.data.read_binary_files(
    config('FILESYSTEM'),
    include_paths=True,
    partition_filter=FileExtensionFilter("tif")
)

def perform(batch):
    from ljpeg.ljpeg import read,od_correct
    from ljpeg.utils import get_ics_info_from_text
    from ray.data.datasource import Datasource, NumpyDatasource
    import tempfile
    import requests
    import cv2
    import numpy as np
    import os.path
    from decouple import config 
    
    # Read
    image = np.frombuffer(batch[0][1], dtype=np.uint16)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

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
    name = os.path.basename(batch[0][0]).split(".")[-2]
    path = os.path.dirname(batch[0][0])+"/"+name+".npy"
    dsImage.write_numpy(config('UPLOADS').replace("REPLACE_THIS", path))

    return batch


ds.map_batches(perform).take_all()
