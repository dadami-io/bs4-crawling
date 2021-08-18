\mport requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import nltk
from konlpy.tag import Kkma
from io import BytesIO
from wordcloud import WordCloud
import time

def getImg(query, num):
    response = "".join([i for i in requests.get("https://api.music.msub.kr/?song="+query).json()["song"][int(num)]["lyrics"].replace("<br>", "\n").split("\n") if i!="" and i!=" "])
    for text in ['.','"',',',"'",'·','=','\n','[',']','“','”','‘','’','?','!','…','vs', '▶','→','(',')','+']:response = response.replace(text, ' ')

    plt.figure(figsize=(10,10))
    plt.imshow(WordCloud(font_path='NanumGothicEcoR.ttf',\
            background_color="white", \
            width=1280, \
            height=960, \
            max_words=100, \
            max_font_size=300).generate_from_frequencies(dict(nltk.Text([i for i in nltk.Text(Kkma().nouns(response), name='기사 내 명사') if len(i)>1 and i!=" "], name = '기사 내 명사 두 번째').vocab().most_common(150))), interpolation='bilinear')
    plt.axis('off')
    plt.show()

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return img

getImg("어김없이 mc", 0)
