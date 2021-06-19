# 한글 분석을 위한 코엔엘파이(konlpy) 설치
# !pip install konlpy 

# 코랩에서 한글 표기를 위해 나눔 글꼴 설치
# !apt-get update -qq
# !apt-get install fonts-nanum* -qq  


import requests                     # HTML 요청 처리
from bs4 import BeautifulSoup       # 웹 크롤링을 위한 패키지 BeautifulSoup 설치
import matplotlib.pyplot as plt
import nltk                         # Natural Language Toolkit 기호 및 통계 자연어 처리를 위한 라이브러리
from konlpy.tag import Kkma         # 오픈소스 한국어 분석기
from konlpy.tag import Okt          # 오픈소스 한국어 분석기
from wordcloud import WordCloud     

# 뉴스 기사를 크롤링하기 위한 날짜를 변수에 저장
query = '코로나'

# 클롤링하기 위한 링크를 변수에 저장
news_url = f'https://search.naver.com/search.naver?query={query}&where=news&ie=utf8&sm=nws_hty'

# 안티 크롤링(Python 코드가 아닌 Mozilla 브라우저로 접속하는 것처럼 우회)
# 일반적으로 각 웹사이트는 해킹, 불법 접속 등을 막기 위해 프로그래머가 코드를 통해 접근하는 것을 방지해놓음
# 브라우저로 접속하는 것처럼 User-Agent에 Mozilla, Chrome 등을 작성하여 우회하는 것을 안티 크롤링이라고 함
headers = {'User-Agent':'Mozilla/5.0'}

# BeautifulSoupdml의 requests.get을 이용하여 HTML을 text로 수집하여 변수에 저장
req = requests.get(news_url, headers = headers)

# HTML 페이지에서 뉴스 기사 제목이 저장된 위치 저장
soup = BeautifulSoup(req.text, 'html.parser')
# print(soup)
news_titles =  soup.select('div.news_wrap.api_ani_send > div > a')

# 기사 제목 리스트 저장하기
crowled_title = []
for i in range(len(news_titles)):
    crowled_title.append(news_titles[i].text)
    print(i+1, news_titles[i].text) 
    
# 뉴스 제목에서 특수 기호 제거하기
title = "".join(crowled_title)
filter_text = ['.','"',',',"'",'·','=','\n','[',']','“','”','‘','’','?','!','…','vs', '▶','→','(',')','+']
for text in filter_text:
    title = title.replace(text, ' ')
filtered_title = title

# Konlpy를 이용하여 기사 제목 내 명사만 추출하기
tw = Okt() 
tokens_ko = tw.nouns(filtered_title)
tokens_ko
ko = nltk.Text(tokens_ko, name='기사 내 명사')
ko.tokens
ko.vocab()

# 단어 길이가 1 이상이면서 '단독' 또는 ' '(공백)이 아닌 단어를 new_ko에 추가하기
new_ko=[]
for word in ko:
  if len(word) > 1 and word != '단독' and  word != ' ':
        new_ko.append(word)
print(new_ko)

# 단어 빈도를 기준으로 내림차순 정렬 후 상위 150개 단어 추출
ko = nltk.Text(new_ko, name = '기사 내 명사 두 번째')
ko.tokens
ko.vocab()
data = ko.vocab().most_common(150)
print(data)

# 단어와 빈도를 dict로 저장하기
data = dict(data)
print(data)

# 워드 클라우드 출력
wordcloud = WordCloud().generate(filtered_title)

font = '/usr/share/fonts/truetype/nanum/NanumGothicEco.ttf'

wc = WordCloud(font_path=font,\
		background_color="white", \
		width=1280, \
		height=960, \
		max_words=100, \
		max_font_size=300)
wc = wc.generate_from_frequencies(data)

plt.figure(figsize=(10,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
