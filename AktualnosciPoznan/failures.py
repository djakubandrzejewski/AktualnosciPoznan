import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import tweepy
from os.path import basename
import configparser
configAPI = configparser.ConfigParser()
configAPI.read('config.ini')

api_key = configAPI['twitter']['api_key']
api_key_secret = configAPI['twitter']['api_key_secret']

access_token = configAPI['twitter']['access_token']
access_token_secret = configAPI['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
tweet_ids_articule = "tweet_history_articule.txt"
tweet_ids_accident = "tweet_history_accident.txt"

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
def send_accident():
    with open('history_tweet/tweet_history_accident.txt', 'r', encoding='utf8') as f:
        last_tweet = f.read().strip()
    newAccident()

    with open('failures/failures.txt', 'r', encoding='utf8') as f:
        accidentTitle = f.readline().strip()
        accidentCategory = f.readline().strip()
        accidentLink = f.readline().strip()
    accidentImage = 'images/image.png'


    tweet_text = f"❗️NOWE ZDARZENIE❗️\n\n{accidentTitle}\n\nKategoria: {accidentCategory}\n\nDowiedz się więcej: {accidentLink}"

    if last_tweet != accidentTitle:
        api.update_status_with_media(status=tweet_text, filename=accidentImage)
        with open('history_tweet/tweet_history_accident.txt', 'w', encoding='utf8') as f:
            f.write(accidentTitle)
        print("Tweet sent:", tweet_text)
    else:
        print("Accident already tweeted:", accidentTitle)
       


    
