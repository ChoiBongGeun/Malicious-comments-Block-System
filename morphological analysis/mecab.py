import time
start = time.time()

from konlpy.tag import Mecab
Mecab = Mecab()
def morph(input_data) :
    preprocessed = Mecab.pos(input_data) 
    print(preprocessed)

morph("마블 3000만큼 사랑합니다")
print ("time:", time.time() - start)