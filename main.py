import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import nltk
from konlpy.tag import Okt
from konlpy.tag import Kkma
from wordcloud import WordCloud
from io import BytesIO
import time

tw = Okt()
query = '코로나'
news_url = 'https://search.naver.com/search.naver?query={}&where=news&ie=utf8&sm=nws_hty'
headers = {'User-Agent':'Mozilla/5.0'}

def getImg(query=query):
    first=time.time()
    print(query)
    req = requests.get(news_url.format(query), headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    news_titles = soup.select('div.news_wrap.api_ani_send > div > a')
    crowled_title = []
    for i in range(len(news_titles)):
        crowled_title.append(news_titles[i].text)
        print(i+1, news_titles[i].text)

    title = "".join(crowled_title)
    filter_text = ['.','"',',',"'",'·','=','\n','[',']','“','”','‘','’','?','!','…','vs', '▶','→','(',')','+']
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

    new_ko=[]
    for word in ko:
      if len(word) > 1 and word != '단독' and  word != ' ':
            new_ko.append(word)
    print(new_ko)

    fourth=time.time()

    ko = nltk.Text(new_ko, name = '기사 내 명사 두 번째')
    ko.tokens
    ko.vocab()
    data = ko.vocab().most_common(150)
    print(data)

    data = dict(data)
    print(data)

    fifth=time.time()
    wordcloud = WordCloud().generate(filtered_title)
    font = 'NanumGothicEcoR.ttf'
    wc = WordCloud(font_path=font,\
            background_color="white", \
            width=1280, \
            height=960, \
            max_words=100, \
            max_font_size=300)
    wc = wc.generate_from_frequencies(data)

    sixth=time.time()

    plt.figure(figsize=(10,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')



    seventh=time.time()

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)

    eighth=time.time()

    print(eighth-first)
    print(first,second,third,fifth,sixth,seventh,eighth)
    return img

def getMusic(query):
        response = "".join([i for i in requests.get("https://api.music.msub.kr/?song="+query).json()["song"][int(0)]["lyrics"].replace("<br>", "\n").split("\n") if i!="" and i!=" "])
        for text in ['.','"',',',"'",'·','=','\n','[',']','“','”','‘','’','?','!','…','vs', '▶','→','(',')','+']:response = response.replace(text, ' ')

        plt.figure(figsize=(10,10))
        plt.imshow(WordCloud(font_path='NanumGothicEcoR.ttf',\
                background_color="white", \
                width=1280, \
                height=960, \
                max_words=100, \
                max_font_size=300).generate_from_frequencies(dict(nltk.Text([i for i in nltk.Text(Kkma().nouns(response), name='기사 내 명사') if len(i)>1 and i!=" "], name = '기사 내 명사 두 번째').vocab().most_common(150))), interpolation='bilinear')
        plt.axis('off')


        img = BytesIO()
        plt.savefig(img, format='png', dpi=200)
        img.seek(0)
        return img
