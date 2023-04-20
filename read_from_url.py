import requests
import cv2
import numpy as np

response = requests.get(sys.argv[1])
response.raise_for_status()
image = np.frombuffer(response.content, np.uint16)
image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
image = cv2.resize(image, (224,336))
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
