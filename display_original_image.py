import requests
import cv2
import numpy as np
from decouple import config
from PIL import Image
import sys
import io

response = requests.get('http://127.0.0.1:9000/mammograms/A_0002_1.LEFT_CC.tif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=YF92W1C3LA1HSFQC5P25%2F20230710%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230710T152506Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJZRjkyVzFDM0xBMUhTRlFDNVAyNSIsImV4cCI6MTY4OTA0NTg3MywicGFyZW50IjoibWluaW9hZG1pbiJ9.ajWaARVO2m8v7VqDqWxzJoaghf-QxdBSs5Vzrj6BgM-RABP5_aRMpyMEh6uKoEAcHgzrIZOhK5XV8teNJHpigA&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=0c2046ae5552ddda49f6a33dfe8dc0a5b5c19a76ecf49b8fe1fe545ec4a45c40')
response.raise_for_status()
image_data = io.BytesIO(response.content)
image = Image.open(image_data)
image = np.array(image)
image = cv2.resize(image, (224,336))
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
