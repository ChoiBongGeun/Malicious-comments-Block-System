import time
start = time.time()

from konlpy.tag import Hannanum
Hannanum = Hannanum()
for word in Hannanum.pos("마블 3000만큼 사랑합니다"):
    print(word)
print ("time:", time.time() - start)