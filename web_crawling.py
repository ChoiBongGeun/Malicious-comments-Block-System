import requests
from bs4 import BeautifulSoup
import pandas as pd
test_url = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=136900&type=after&page=1"
resp = requests.get(test_url)
html = BeautifulSoup(resp.content, 'html.parser')
html

score_result = html.find('div', {'class': 'score_result'})
lis = score_result.findAll('li')
lis[0]

review_text = lis[0].find('p').getText()
review_text

like = lis[0].find('div', {'class': 'btn_area'}).findAll('span')[1].getText()
dislike = lis[0].find('div', {'class': 'btn_area'}).findAll('span')[3].getText()
like, dislike

nickname = lis[0].findAll('a')[0].find('span').getText()
nickname

from datetime import datetime
created_at = datetime.strptime(lis[0].find('dt').findAll('em')[-1].getText(), "%Y.%m.%d %H:%M")
created_at
results =[]
def get_data(url):
    resp = requests.get(url)
    html = BeautifulSoup(resp.content, 'html.parser')
    score_result = html.find('div', {'class': 'score_result'})
    lis = score_result.findAll('li')
    for li in lis:        
        nickname = li.findAll('a')[0].find('span').getText()
        created_at = datetime.strptime(li.find('dt').findAll('em')[-1].getText(), "%Y.%m.%d %H:%M")
        
        review_text = li.find('p').getText()
        score = li.find('em').getText()
        btn_likes = li.find('div', {'class': 'btn_area'}).findAll('span')
        like = btn_likes[1].getText()
        dislike = btn_likes[3].getText()
        results.append(review_text)

result = html.find('div', {'class':'score_total'}).find('strong').findChildren('em')[1].getText()
int(result.replace(',', ''))

test_url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=136900&type=after'
resp = requests.get(test_url)
html = BeautifulSoup(resp.content, 'html.parser')
result = html.find('div', {'class':'score_total'}).find('strong').findChildren('em')[1].getText()
total_count = int(result.replace(',', ''))

for i in range(1,int(total_count / 10) + 1):
    url = test_url + '&page=' + str(i)
    print('url: ' + url + '')
    get_data(url)

import numpy as np
import pandas as pd
data = pd.DataFrame(results)
data.to_csv('C:\\Users\\dhy00\\Desktop\\결과값.csv', encoding='cp949')
