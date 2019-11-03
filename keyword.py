from soynlp.hangle import compose
from soynlp.hangle import decompose
from bs4 import BeautifulSoup 
import requests 
import re
import fasttext
import sys 
import pprint 
import datetime
import os

List=[]

def flatten(l): # 리스트 통합
    flatList = [] 
    for elem in l: 
        if type(elem) == list: 
            for e in elem: 
                flatList.append(e) 
        else: 
            flatList.append(elem) 
    return flatList

def cleantxt(txt): 
    cleantxt = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-+<>@\#$%&\\\=\(\'\"]','', txt)
    return cleantxt

def get_filename():
    r = requests.get(url,headers=header)
    cont = BeautifulSoup(r.text,"html.parser")
    newsname = str(cont).split("<title>")[1].split("</title>")[0]
    clearnewsname = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-+<>@\#$%&\\\=\(\'\"]','', newsname)
    filename=str(datetime.datetime.now().strftime('%m-%d-%H:%M_')+clearnewsname)
    #print(clearnewsname)
    return clearnewsname

def satx():
    file = open('c'+get_filename()+'.txt','w',encoding='utf-8')
    for commentline in flatten(List):
        file.write(cleantxt(commentline)+'\n')
    file.close()

def cr():
    page = 1
    while True :
        c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"
        r=requests.get(c_url,headers=header) 
        cont=BeautifulSoup(r.content,"html.parser")     
        comment_num=str(cont).split('comment":')[1].split(",")[0]
        match=re.findall('"contents":([^\*]*),"userIdNo"', str(cont)) 
        List.append(match) 
# 댓글 가져오기 , 댓글 수 프린트
        if int(comment_num) <= ((page) * 20):
            print("기사 제목 :"+get_filename()+'.txt')
            print('댓글 수'+comment_num+'개')
            break 
        else :  
            page+=1
    if int(comment_num) < 10:
        print ("댓글 수가 10개보다 적습니다.")
    else :
        satx()


def keyword_find(keyword):
 keyword_num=0
 with open('c'+get_filename()+'.txt', encoding='utf8') as f1:
     output = get_filename()+'.txt'
     with open(output, 'w', encoding='utf8') as f2:
                for line in f1:
                    key_pre = line.replace("\n","")
                    if str(keyword) in str(line):
                        f2.write(line)
                        keyword_num+=1
 print('['+ str(keyword)+'] 키워드 덧글 [ '+ str(keyword_num) +' ] 개')

doublespace_pattern = re.compile('\s+')
def keyword_x():
     with open('c'+get_filename()+'.txt', encoding='utf8') as f1:
        output = get_filename()+'.txt' 
        with open(output, 'w', encoding='utf8') as f2:
            for line in f1:
                f2.write(line)

                
def jamo_sentence(sent):
    def transform(char):
        if char == ' ':
            return char
        cjj = decompose(char)
        if cjj is None:
            return char
        if len(cjj) == 1:
            return cjj
        cjj_ = ''.join(c if c != ' ' else '-' for c in cjj)
        return cjj_
    sent_ = ''.join(transform(char) for char in sent)
    sent_ = doublespace_pattern.sub(' ', sent_)
    return (sent_)

def copy_and_print_js():
  with open(get_filename()+'.txt', encoding="utf8") as f1:
    output = get_filename()+'js'+'.txt'
    with open(output, 'w', encoding='utf8') as f2:
      for line in f1:
          f2.write(jamo_sentence(line) + '\n')


def copy_and_print_model():
  bad=0
  suspicion=0
  nomal=0
  with open(get_filename()+'js'+'.txt', encoding="utf8") as f1:
    output_txt = '악플_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
        with open('의심_'+get_filename()+'.txt', 'a', encoding='utf8') as f3:
            with open('일반_'+get_filename()+'.txt', 'a', encoding='utf8') as f4:
                for line in f1:
                    js_pre = line.replace("\n","")
                    check_text = model.predict(js_pre)
                    
                    #print(line)
                    if 'label__악플' in str(check_text):
                        #print ("욕")
                        f2.write(line)
                        bad+=1
                    elif 'label__의심' in str(check_text):
                        #print ("욕아님")
                        #print(line)
                        #print('일반에 추가합니다 \n'+line)
                        f3.write(line)
                        suspicion+=1
                    elif 'label__일반' in str(check_text):
                        #print(js_pre)
                        #line2 = line.replace("\n\n","")
                        nomal+=1
                        f4.write(line)
                        
                    else : print(" 아무것도 아닌 라벨 ")
    print("악플: "+str(bad)+'개')
    print("의심: "+str(suspicion)+'개')
    print("일반: "+str(nomal)+'개')


def hangulman(txt):
    hangul = re.compile('[^ \- ㄱ-ㅣ 가-힣]+') 
    result = hangul.sub('', txt) 
    #result = result.replace('일반','') #라벨링이 남아있는 파일에 경우에 사용
    #result=result.replace('ㄳ','ㄱㅅ').replace('ㄵ','ㄴㅈ').replace('ㄶ','ㄴㅎ').replace('ㄺ','ㄹㄱ').replace('ㄻ','ㄹㅁ').replace('ㄼ','ㄹㅂ').replace('ㄽ','ㄹㅅ').replace('ㄾ','ㄹㅌ').replace('ㄿ','ㄹㅍ').replace('ㅀ','ㄹㅎ').replace('ㅄ','ㅂㅅ')
    return result

def copy_and_print_hangulman():
  with open('악플_'+get_filename()+'.txt', encoding="utf8") as f1:
    output_txt = '한글만_'+'악플_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
      for line in f1:
            f2.write(hangulman(line) + '\n')
            
  with open('일반_'+get_filename()+'.txt', encoding="utf8") as f1:
    output_txt = '한글만_'+'일반_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
      for line in f1:
            f2.write(hangulman(line) + '\n')
            
  with open('의심_'+get_filename()+'.txt', encoding="utf8") as f1:
    output_txt = '한글만_'+'의심_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
      for line in f1:
            f2.write(hangulman(line) + '\n')

def decode(s):
    def process(t):
        assert len(t) % 3 == 0
        t_ = t.replace('-', ' ')
        chars = [tuple(t_[3*i:3*(i+1)]) for i in range(len(t_)//3)]
        recovered = [compose(*char) for char in chars]
        recovered = ''.join(recovered)
        return recovered
    return ' '.join(process(t) for t in s.split())

def decode_sentence(sent):
    return ' '.join(decode(token) for token in sent.split())

def copy_and_print_decode():
  copy_and_print_hangulman()
  with open('한글만_'+'악플_'+get_filename()+'.txt', encoding="utf8") as f1:
    output_txt = '악플_자모결합_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
      for line in f1:
          temporary_conversion1 = line.replace('-ㅏ-','ㅆㅏㄾ').replace('-ㅐ-','ㅆㅐㄾ').replace('-ㅑ-','ㅆㅑㄾ').replace('-ㅒ-','ㅆㅒㄾ').replace('-ㅓ-','ㅆㅓㄾ').replace('-ㅔ-','ㅆㅔㄾ').replace('-ㅕ-','ㅆㅕㄾ').replace('-ㅖ-','ㅆㅖㄾ').replace('-ㅗ-','ㅆㅗㄾ').replace('-ㅘ-','ㅆㅘㄾ').replace('-ㅙ-','ㅆㅙㄾ').replace('-ㅚ-','ㅆㅚㄾ').replace('-ㅛ-','ㅆㅛㄾ').replace('-ㅜ-','ㅆㅜㄾ').replace('-ㅝ-','ㅆㅝㄾ').replace('-ㅞ-','ㅆㅞㄾ').replace('-ㅟ-','ㅆㅟㄾ').replace('-ㅠ-','ㅆㅠㄾ').replace('-ㅡ-','ㅆㅡㄾ').replace('-ㅢ-','ㅆㅢㄾ').replace('-ㅣ-','ㅆㅣㄾ')
          temporary_conversion2 = temporary_conversion1.replace('ㄳ--','ㅎㅞㄳ').replace('ㄵ--','ㅎㅞㄵ').replace('ㄶ--','ㅎㅞㄶ').replace('ㄺ--','ㅎㅞㄺ').replace('ㄻ--','ㅎㅞㄻ').replace('ㄼ--','ㅎㅞㄼ').replace('ㄽ--','ㅎㅞㄽ').replace('ㄾ--','ㅎㅞㄾ').replace('ㄿ--','ㅎㅞㄿ').replace('ㅀ--','ㅎㅞㅀ').replace('ㅄ--','ㅎㅞㅄ').replace('--','ㅢㄿ')
          temporary_conversion = decode(temporary_conversion2)
          conversion = temporary_conversion.replace('긢','ㄱ').replace('늺','ㄴ').replace('딆','ㄷ').replace('릞','ㄹ').replace('믪','ㅁ').replace('븶','ㅂ').replace('싎','ㅅ').replace('읦','ㅇ').replace('즲','ㅈ').replace('칊','ㅊ').replace('킖','ㅋ').replace('틢','ㅌ').replace('픮','ㅍ').replace('흺','ㅎ').replace('끮','ㄲ').replace('띒','ㄸ').replace('삂','ㅃ').replace('씚','ㅆ').replace('쯾','ㅉ').replace('쌅','ㅏ').replace('쌡','ㅐ').replace('쌽','ㅑ').replace('쌡','ㅒ').replace('썵','ㅓ').replace('쎑','ㅔ').replace('쎭','ㅕ').replace('쏉','ㅖ').replace('쏥','ㅗ').replace('쐁','ㅘ').replace('쐝','ㅙ').replace('쐹','ㅚ').replace('쑕','ㅛ').replace('쑱','ㅜ').replace('쒍','ㅝ').replace('쒩','ㅞ').replace('쓅','ㅟ').replace('쓡','ㅠ').replace('쓽','ㅡ').replace('씙','ㅢ').replace('씵','ㅣ').replace('훿','ㄳ').replace('휁','ㄵ').replace('휂','ㄶ').replace('휅','ㄺ').replace('휆','ㄻ').replace('휇','ㄼ').replace('휈','ㄽ').replace('휉','ㄾ').replace('휊','ㄿ').replace('휋','ㅀ').replace('휎','ㅄ')
          f2.write(conversion+'\n')
  with open('한글만_'+'일반_'+get_filename()+'.txt', encoding="utf8") as f1:
    output_txt = '일반_자모결합_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
      for line in f1:
          temporary_conversion1 = line.replace('-ㅏ-','ㅆㅏㄾ').replace('-ㅐ-','ㅆㅐㄾ').replace('-ㅑ-','ㅆㅑㄾ').replace('-ㅒ-','ㅆㅒㄾ').replace('-ㅓ-','ㅆㅓㄾ').replace('-ㅔ-','ㅆㅔㄾ').replace('-ㅕ-','ㅆㅕㄾ').replace('-ㅖ-','ㅆㅖㄾ').replace('-ㅗ-','ㅆㅗㄾ').replace('-ㅘ-','ㅆㅘㄾ').replace('-ㅙ-','ㅆㅙㄾ').replace('-ㅚ-','ㅆㅚㄾ').replace('-ㅛ-','ㅆㅛㄾ').replace('-ㅜ-','ㅆㅜㄾ').replace('-ㅝ-','ㅆㅝㄾ').replace('-ㅞ-','ㅆㅞㄾ').replace('-ㅟ-','ㅆㅟㄾ').replace('-ㅠ-','ㅆㅠㄾ').replace('-ㅡ-','ㅆㅡㄾ').replace('-ㅢ-','ㅆㅢㄾ').replace('-ㅣ-','ㅆㅣㄾ')
          temporary_conversion2 = temporary_conversion1.replace('ㄳ--','ㅎㅞㄳ').replace('ㄵ--','ㅎㅞㄵ').replace('ㄶ--','ㅎㅞㄶ').replace('ㄺ--','ㅎㅞㄺ').replace('ㄻ--','ㅎㅞㄻ').replace('ㄼ--','ㅎㅞㄼ').replace('ㄽ--','ㅎㅞㄽ').replace('ㄾ--','ㅎㅞㄾ').replace('ㄿ--','ㅎㅞㄿ').replace('ㅀ--','ㅎㅞㅀ').replace('ㅄ--','ㅎㅞㅄ').replace('--','ㅢㄿ')
          temporary_conversion = decode(temporary_conversion2)
          conversion = temporary_conversion.replace('긢','ㄱ').replace('늺','ㄴ').replace('딆','ㄷ').replace('릞','ㄹ').replace('믪','ㅁ').replace('븶','ㅂ').replace('싎','ㅅ').replace('읦','ㅇ').replace('즲','ㅈ').replace('칊','ㅊ').replace('킖','ㅋ').replace('틢','ㅌ').replace('픮','ㅍ').replace('흺','ㅎ').replace('끮','ㄲ').replace('띒','ㄸ').replace('삂','ㅃ').replace('씚','ㅆ').replace('쯾','ㅉ').replace('쌅','ㅏ').replace('쌡','ㅐ').replace('쌽','ㅑ').replace('쌡','ㅒ').replace('썵','ㅓ').replace('쎑','ㅔ').replace('쎭','ㅕ').replace('쏉','ㅖ').replace('쏥','ㅗ').replace('쐁','ㅘ').replace('쐝','ㅙ').replace('쐹','ㅚ').replace('쑕','ㅛ').replace('쑱','ㅜ').replace('쒍','ㅝ').replace('쒩','ㅞ').replace('쓅','ㅟ').replace('쓡','ㅠ').replace('쓽','ㅡ').replace('씙','ㅢ').replace('씵','ㅣ').replace('훿','ㄳ').replace('휁','ㄵ').replace('휂','ㄶ').replace('휅','ㄺ').replace('휆','ㄻ').replace('휇','ㄼ').replace('휈','ㄽ').replace('휉','ㄾ').replace('휊','ㄿ').replace('휋','ㅀ').replace('휎','ㅄ')
          f2.write(conversion+'\n')
  with open('한글만_'+'의심_'+get_filename()+'.txt', encoding="utf8") as f1:
    output_txt = '의심_자모결합_'+get_filename()+'.txt'
    with open(output_txt, 'w', encoding='utf8') as f2:
      for line in f1:
          temporary_conversion1 = line.replace('-ㅏ-','ㅆㅏㄾ').replace('-ㅐ-','ㅆㅐㄾ').replace('-ㅑ-','ㅆㅑㄾ').replace('-ㅒ-','ㅆㅒㄾ').replace('-ㅓ-','ㅆㅓㄾ').replace('-ㅔ-','ㅆㅔㄾ').replace('-ㅕ-','ㅆㅕㄾ').replace('-ㅖ-','ㅆㅖㄾ').replace('-ㅗ-','ㅆㅗㄾ').replace('-ㅘ-','ㅆㅘㄾ').replace('-ㅙ-','ㅆㅙㄾ').replace('-ㅚ-','ㅆㅚㄾ').replace('-ㅛ-','ㅆㅛㄾ').replace('-ㅜ-','ㅆㅜㄾ').replace('-ㅝ-','ㅆㅝㄾ').replace('-ㅞ-','ㅆㅞㄾ').replace('-ㅟ-','ㅆㅟㄾ').replace('-ㅠ-','ㅆㅠㄾ').replace('-ㅡ-','ㅆㅡㄾ').replace('-ㅢ-','ㅆㅢㄾ').replace('-ㅣ-','ㅆㅣㄾ')
          temporary_conversion2 = temporary_conversion1.replace('ㄳ--','ㅎㅞㄳ').replace('ㄵ--','ㅎㅞㄵ').replace('ㄶ--','ㅎㅞㄶ').replace('ㄺ--','ㅎㅞㄺ').replace('ㄻ--','ㅎㅞㄻ').replace('ㄼ--','ㅎㅞㄼ').replace('ㄽ--','ㅎㅞㄽ').replace('ㄾ--','ㅎㅞㄾ').replace('ㄿ--','ㅎㅞㄿ').replace('ㅀ--','ㅎㅞㅀ').replace('ㅄ--','ㅎㅞㅄ').replace('--','ㅢㄿ')
          temporary_conversion = decode(temporary_conversion2)
          conversion = temporary_conversion.replace('긢','ㄱ').replace('늺','ㄴ').replace('딆','ㄷ').replace('릞','ㄹ').replace('믪','ㅁ').replace('븶','ㅂ').replace('싎','ㅅ').replace('읦','ㅇ').replace('즲','ㅈ').replace('칊','ㅊ').replace('킖','ㅋ').replace('틢','ㅌ').replace('픮','ㅍ').replace('흺','ㅎ').replace('끮','ㄲ').replace('띒','ㄸ').replace('삂','ㅃ').replace('씚','ㅆ').replace('쯾','ㅉ').replace('쌅','ㅏ').replace('쌡','ㅐ').replace('쌽','ㅑ').replace('쌡','ㅒ').replace('썵','ㅓ').replace('쎑','ㅔ').replace('쎭','ㅕ').replace('쏉','ㅖ').replace('쏥','ㅗ').replace('쐁','ㅘ').replace('쐝','ㅙ').replace('쐹','ㅚ').replace('쑕','ㅛ').replace('쑱','ㅜ').replace('쒍','ㅝ').replace('쒩','ㅞ').replace('쓅','ㅟ').replace('쓡','ㅠ').replace('쓽','ㅡ').replace('씙','ㅢ').replace('씵','ㅣ').replace('훿','ㄳ').replace('휁','ㄵ').replace('휂','ㄶ').replace('휅','ㄺ').replace('휆','ㄻ').replace('휇','ㄼ').replace('휈','ㄽ').replace('휉','ㄾ').replace('휊','ㄿ').replace('휋','ㅀ').replace('휎','ㅄ')
          f2.write(conversion+'\n')
          

print("모델 로드 중 ...")
model = fasttext.load_model("model_jscomment.bin")
url = input('기사링크 입력\n')
keyword = input('키워드 입력\n')
oid=url.split("oid=")[1].split("&")[0] 
aid=url.split("aid=")[1]
header = {
"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"referer": url,
}

print("[ 1 / 4 ] 댓글 크롤링 중 ...")
cr()
if keyword=='':
    keyword_x()
else:
    keyword_find(keyword)

print("[ 2 / 4 ] 댓글 자소분리 중 ...")
copy_and_print_js()
print("[ 3 / 4 ] 자소분리 댓글 fasttext 모델에서 분류 중 ...")
copy_and_print_model()
print("[ 4 / 4 ] 분류된 파일 자소분리 복구 중 ...")
copy_and_print_decode()
os.remove(get_filename()+'js.txt')
os.remove('일반_'+get_filename()+'.txt')
os.remove('악플_'+get_filename()+'.txt')
os.remove('의심_'+get_filename()+'.txt')
os.remove('한글만_일반_'+get_filename()+'.txt')
os.remove('한글만_악플_'+get_filename()+'.txt')
os.remove('한글만_의심_'+get_filename()+'.txt')
os.remove('c'+get_filename()+'.txt')


