import time
start = time.time()
sentence = u'내년도 최저임금을 기존 방식대로 전체 업종에 동일하게 적용하기로 결정했다.\
최저임금의 업종별 차등 적용을 요구해온 사용자위원들은 이에 반발해 전원회의에서 퇴장했다.'
from khaiii import KhaiiiApi
api = KhaiiiApi()
for word in api.analyze(sentence):
    print(word)
print ("time:", time.time() - start)