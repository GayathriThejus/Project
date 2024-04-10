# import cv2
# import matplotlib.pyplot as plt

# def show_image(image):
#     plt.figure(figsize=(10,10))
#     plt.imshow(image)
#     plt.show()                #without this,the img would be created but not displayed

# in_image=cv2.imread("schoolbus-1.jpg")
# show_image(in_image)

# small=in_image[0:200,0:200]
# show_image(small)
# print(small.shape)

import requests
from pprint import pprint
from geopy.distance import distance

BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'
query = 'Peringavu bus stop'

response=requests.get(f"{BASE_URL}&q={query}")
# pprint(response.json())
data = response.json()
latitude=data[0].get('lat')
longitude=data[0].get('lon')
print(latitude,longitude) 

query='Cheroor Bus Stop'
response=requests.get(f"{BASE_URL}&q={query}")
data=response.json()
# pprint(response.json())
latitude2=data[0].get('lat')
longitude2=data[0].get('lon')
print(latitude2,longitude2)

location=float(latitude),float(longitude)
location2=float(latitude2),float(longitude2)

km=distance(location,location2)
print("Distance between the locations:")
print(f"{km}")