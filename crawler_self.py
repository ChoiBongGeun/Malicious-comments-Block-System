List=[] 
from bs4 import BeautifulSoup 
import requests 
import re 
import sys 
import pprint 
import datetime


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
    print(filename)
    return filename

def satx():
    file = open(get_filename(),'w',encoding='utf-8')
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
            print('댓글 수'+comment_num+'개')
            break 
        else :  
            page+=1
    if int(comment_num) < 10:
        print ("댓글 수가 10개보다 적습니다.")
    else :
        satx()

while True :
    url = input('기사링크 입력\n')
    oid=url.split("oid=")[1].split("&")[0] 
    aid=url.split("aid=")[1]
    header = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "referer": url,
    }
    cr()
    
