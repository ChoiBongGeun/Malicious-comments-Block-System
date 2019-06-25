import time
start = time.time()
from khaiii import KhaiiiApi
api = KhaiiiApi()
for word in api.analyze("마블 3000만큼 사랑합니다"):
    print(word)
print ("time:", time.time() - start)