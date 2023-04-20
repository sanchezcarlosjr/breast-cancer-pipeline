import requests
import io
import cv2
import numpy as np
import sys
from decouple import config 

response = requests.get(config('REST')+sys.argv[1])
response.raise_for_status()
image = np.load(io.BytesIO(response.content))
cv2.imshow('NPY Image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
