import time
start = time.time()

from konlpy.tag import Twitter
twitter = Twitter()
for word in twitter.pos("마블 3000만큼 사랑합니다"):
    print(word)
print ("time:", time.time() - start)