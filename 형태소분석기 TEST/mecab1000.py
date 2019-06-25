import time
start = time.time()

from konlpy.tag import Mecab
Mecab = Mecab()
sentence = u'감정노동자 보호법은 사업주로 하여금 감정노동으로부터 근로자를 보호하는 예방 조치를 이행하도록 강제한다.\
다만 현장 근로자들을 중심으론 이 같은 법안이 현장에 제대로 적용되기 위해서는 회사의 수직적 위계 구조와 인력 부족 문제 등\
구조적 문제가 우선 해결돼야 한다는 지적도 나온다.'
sentences = [sentence] * 10000
morphs = [Mecab.morphs(sentence) for sentence in sentences]
print ("time:", time.time() - start)