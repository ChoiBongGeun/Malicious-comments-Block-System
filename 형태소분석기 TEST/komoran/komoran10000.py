import time
start = time.time()
from konlpy.tag import Komoran
komoran = Komoran()
for i in range(1,10000):
    for word in komoran.pos("마블 3000만큼 사랑합니다"):
        print(word)
print ("time:", time.time() - start)