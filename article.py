import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import tweepy
from os.path import basename
import configparser
import os
from linkpreview import link_preview

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
tweet_ids_articule = "tweet_history_articule.txt"
tweet_ids_accident = "tweet_history_accident.txt"


def newArticule():
    BASE_URL = requests.get('https://www.poznan.pl/').text
    soup = BeautifulSoup(BASE_URL, 'html.parser')
    today = date.today()
    strToday = str(today)
    articules = soup.find_all('section', class_ ='column big')

    for articule in articules:
            articuleDate = articule.find('time').text

            articuleLink = articule.find('a', href=True)
            articuleLink = articuleLink['href']
            articule_title = articule.find('a')
            articule_title = (articule_title['aria-label']).replace(strToday, '')
            articuleImage = articule.find('img')
            articuleImage = articuleImage['data-src']
            urlPoznan = 'http://poznan.pl/'
            articuleImageDownload = urlPoznan.strip(',') + articuleImage.strip()
            articuleImageDownload_response = requests.get(articuleImageDownload)
            with open('articules/articules.txt', 'w', encoding='utf-8') as f:
                f.write((f'{articule_title.strip()}\n{articuleDate.strip()}\n{urlPoznan}{articuleLink}'))
            with open('tweet_history_articule.txt', 'w', encoding='utf8') as f:
                f.write(f'{articule_title}')


def newAccident():
        BASE_URL = requests.get('https://www.poznan.pl').text
        soup = BeautifulSoup(BASE_URL, 'lxml')
        today = date.today()
        strToday = str(today)
        failures = soup.find('article', class_='dotdotdot awarie-news-text')       
        accidentTitle = failures.find('h3').text.strip()
        accidentLink = failures.find('a')
        accidentLink = accidentLink['href']
        urlPoznan = 'http://poznan.pl/'
        accidentCategory = failures.find('div', class_='label-awarie').text
        with open('failures/failures.txt', 'w', encoding='utf8') as f:
            f.write(f'{accidentTitle.strip()}\n{accidentCategory}\n{urlPoznan}{accidentLink}')
        with open('tweet_history_accident.txt', 'w', encoding='utf8') as f:
            f.write(f'{accidentTitle}')
        

def newSmartcity():
    BASE_URL = requests.get('https://www.poznan.pl/smartcity/').text
    soup = BeautifulSoup(BASE_URL, 'html.parser')
    today = date.today()
    strToday = str(today)
    smartcity = soup.find_all('section', class_='column big')

    for articule in smartcity:
            articuleDate = articule.find('time').text
            articuleLink = articule.find('a', href=True)
            articuleLink = articuleLink['href']
            articule_title = articule.find('a')
            articule_title = (articule_title['aria-label']).replace(articuleDate, '')
            articuleImage = articule.find('img')
            articuleImage = articuleImage['data-src']
            urlPoznan = 'http://poznan.pl/'
    with open('smartcity/smartcity.txt', 'w', encoding='utf8') as f:
        f.write((f'{articule_title.strip()}\n{articuleDate.strip()}\n{urlPoznan}{articuleLink}'))


def send_smartcity():
    with open('tweet_history_smartcity.txt', 'r',encoding='utf8') as f:
        last_tweet = f.read().strip()

    newSmartcity()

    with open('smartcity/smartcity.txt', 'r', encoding='utf8') as f:
        articuleTitle = f.readline().strip()
        articuleDate = f.readline().strip()
        articuleLink = f.readline().strip()

    tweet_articule = f"📰{articuleTitle}📰\n{articuleDate}\nDowiedz się więcej: {articuleLink}"
    if last_tweet != articuleTitle:
        api.update_status(tweet_articule)
        with open('tweet_history_smartcity.txt', 'w', encoding='utf8') as f:
            f.write(articuleTitle)
            print('Tweet smartcity sent.', articuleTitle)
    else:
        print('articule smartcity already tweeeted', articuleTitle)


def send_accident():
    #Pobieranie historie komuninikatu
    with open('tweet_history_accident.txt', 'r', encoding='utf8') as f:
        last_tweet = f.read().strip()
    #scrapping
    newAccident()
    #informacje na tweeta
    with open('failures/failures.txt', 'r', encoding='utf8') as f:
        accidentTitle = f.readline().strip()
        accidentCategory = f.readline().strip()
        accidentLink = f.readline().strip()
    accidentImage = 'image/notification.JPEG'
    media = api.media_upload(accidentImage)
    media_id = media.media_id
    link = "https://twitter.com/ryanjjvance/status/1103372254161850368"


    tweet_text = f"❗️NOWE ZDARZENIE❗️\n\n{accidentTitle}\n\nKategoria: {accidentCategory}\n\nDowiedz się więcej: {accidentLink}"

    if last_tweet != accidentTitle:
        #api.update_status_with_media(status=tweet_text, filename="image/smartcity.png", lat=0, long=0)
        api.update_status(
            status=tweet_text,
            media_ids = [media_id],
            attachment_url = accidentLink
        )
        with open('tweet_history_accident.txt', 'w', encoding='utf8') as f:
            f.write(accidentTitle)
        print("Tweet sent:", tweet_text)
    else:
        print("Accident already tweeted:", accidentTitle)

def send_articule():
    with open('tweet_history_articule.txt', 'r', encoding='utf8') as f:
        last_tweet = f.read().strip()

    newArticule()

    with open('articules/articules.txt', 'r', encoding='utf8') as f:
        articuleTitle = f.readline().strip()
        articuleDate = f.readline().strip()
        articuleLink = f.readline().strip()
    tweet_articule = f"📰{articuleTitle}📰\n{articuleDate}\nDowiedz się więcej: {articuleLink}"
    if last_tweet != articuleTitle:
        api.update_status(tweet_articule)    
        with open('tweet_history_articule.txt', 'w', encoding='utf8') as f:
            f.write(articuleTitle)
        print('Tweet (articule) sent.', articuleTitle)
    else:
        print('Articule already tweeted', articuleTitle)


while True:
    send_accident()
    send_articule()
    send_smartcity()
    print('waiting')
    time.sleep(2)
