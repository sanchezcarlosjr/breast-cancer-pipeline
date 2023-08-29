import ray
from ray.data.datasource import FileExtensionFilter
from decouple import config 

print(config('FILESYSTEM'))

ds = ray.data.read_binary_files(
    config('FILESYSTEM'),
    include_paths=True,
    partition_filter=FileExtensionFilter("tif")
)

print(ds)

def perform(batch):
    from ray.data.datasource import Datasource, NumpyDatasource
    import tempfile
    import requests
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import cv2
    import numpy as np
    from PIL import Image
    import os.path
    from decouple import config 
    import io
    
    for item in batch:
        print("Starting ", item[0])
        # Read
        image = np.frombuffer(item[1], dtype=np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        _, binary_mask = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

        masked_image = cv2.bitwise_and(img, img, mask=binary_mask)

        selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        opened_mask = cv2.morphologyEx(masked_image, cv2.MORPH_OPEN, selem)

        contours, _ = cv2.findContours(opened_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        cropped_img = img[y:y+h, x:x+w]

        norm_img = cv2.normalize(cropped_img, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)

        magma = plt.get_cmap('magma')
        colored_img = magma(norm_img)
        
        colored_img = (colored_img * 255).astype(np.uint8)

        colored_img = cv2.cvtColor(colored_img, cv2.COLOR_RGBA2RGB)
        
        # resize
        image = cv2.resize(image, (336, 224))

        dsImage = ray.data.from_numpy([image])
        name = ".".join(os.path.basename(item[0]).split(".")[:2])+".npy"
        path = 'pi-v2'+"/"+name
        upload_directory = config('UPLOADS').replace("REPLACE_THIS", path)
        dsImage.write_numpy(upload_directory)
        print("Done ", upload_directory)

    return batch


ds.map_batches(perform).take_all()


