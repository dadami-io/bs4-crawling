from bs4.element import Declaration
import requests
from bs4 import BeautifulSoup #파싱 모듈 임포트
import matplotlib.pyplot as plt #데이터 분석 모듈 matplotlib 임포트
import nltk
from konlpy.tag import Okt 
from wordcloud import WordCloud #워드클라우드 모듈
from io import BytesIO
import time
import gc

tw = Okt()
query = 'null'
news_url = 'https://search.naver.com/search.naver?query={}&where=news&ie=utf8&sm=nws_hty'
headers = {'User-Agent':'Mozilla/5.0'} #유저에이전트를 헤더에 걸어둠으로서 봇이 아니라고 서버를 속임

def getImg(query=query):
    first=time.time()
    gc.collect()
    req = requests.get(news_url.format(query), headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    news_titles = soup.select('div.news_wrap.api_ani_send > div > a') #파싱할 부분 파싱
    crowled_title = []
    for i in range(len(news_titles)):
        crowled_title.append(news_titles[i].text)

    title = "".join(crowled_title)
    filter_text = ['.','"',',',"'",'·','=','\n','[',']','“','”','‘','’','?','!','…','vs', '▶','→','(',')','+'] #이런 문자들은 데이터에서 제외
    for text in filter_text:
        title = title.replace(text, ' ')
    filtered_title = title

    second=time.time()

    tokens_ko = tw.nouns(filtered_title)
    tokens_ko
    ko = nltk.Text(tokens_ko, name='기사 내 명사')
    ko.tokens
    ko.vocab()

    third=time.time()

    new_ko=[] #형태소분석 - 명사만 추출
    for word in ko:
      if len(word) > 1 and word != '단독' and  word != ' ':
            new_ko.append(word)

    fourth=time.time()

    ko = nltk.Text(new_ko, name = '기사 내 명사 두 번째')
    ko.tokens
    ko.vocab()
    data = ko.vocab().most_common(150)

    data = dict(data)

    fifth=time.time()
    wordcloud = WordCloud().generate(filtered_title)
    font = 'NanumGothicEcoR.ttf'
    wc = WordCloud(font_path=font,\
            background_color="white", \
            width=1280, \
            height=960, \
            max_words=100, \
            max_font_size=300)
    wc = wc.generate_from_frequencies(data) #워드클라우드 생성

    sixth=time.time()

    plt.figure(figsize=(10,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')



    seventh=time.time()

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200) #만들어진 이미지 세이브
    img.seek(0)

    eighth=time.time()
    gc.collect()
    plt.close('all')
    plt.clf()
    return img
    



def getMusic(query):    
        response = "".join([i for i in requests.get("https://api.music.msub.kr/?song="+query).json()["song"][int(0)]["lyrics"].replace("<br>", "\n").split("\n") if i!="" and i!=" "])
        for text in ['.','"',',',"'",'·','=','\n','[',']','“','”','‘','’','?','!','…','vs', '▶','→','(',')','+']:response = response.replace(text, ' ')

        plt.figure(figsize=(10,10))
        gc.collect()
        plt.imshow(WordCloud(font_path='NanumGothicEcoR.ttf',\
                background_color="white", \
                width=1280, \
                height=960, \
                max_words=100, \
                max_font_size=300).generate_from_frequencies(dict(nltk.Text([i for i in nltk.Text(Okt().nouns(response), name='기사 내 명사') if len(i)>1 and i!=" "], name = '기사 내 명사 두 번째').vocab().most_common(150))), interpolation='bilinear')
        plt.axis('off')


        img = BytesIO()
        plt.savefig(img, format='png', dpi=200)
        img.seek(0)
        gc.collect()
        plt.close('all')
        plt.clf()
        return img