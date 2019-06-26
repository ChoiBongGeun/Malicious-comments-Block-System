sentence = u'내년도 최저임금을 기존 방식대로 전체 업종에 동일하게 적용하기로 결정했다.\
최저임금의 업종별 차등 적용을 요구해온 사용자위원들은 이에 반발해 전원회의에서 퇴장했다.\
최저임금위원회 사용자위원들은 이날 오후 정부세종청사에서 열린 최저임금위원회 제5차 전원회의 도중 퇴장해 기자들과 만나 \
"금일 최저임금위원회는 최저임금 고시에 월 환산액을 병기하고 2020년 최저임금을 모든 업종에 동일하게 적용하기로 결정했다"고 밝혔다.'
sentences = [sentence] * 10000

import time
from konlpy.tag import Hannanum, Kkma, Komoran, Okt, Mecab
from khaiii import KhaiiiApi
api = KhaiiiApi()
morphs_processors= [('Hannanum', Hannanum()), ('Kkma', Kkma()), ('Komoran', Komoran()), ('Okt', Okt()), ('mecab', Mecab())]
for name, morphs_processor in morphs_processors:
    strat_time = time.time()
    morphs = [morphs_processor.pos(sentence) for sentence in sentences]                                          
    elapsed_time = time.time() - strat_time
    print('morphs_processor name = %20s, %.5f secs' % (name, elapsed_time))
strat_time = time.time()
morphs = [api.analyze(sentence) for sentence in sentences]
elapsed_time = time.time() - strat_time
print('morphs_processor name = %20s, %.5f secs' % ('khaiii', elapsed_time))