import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import tweepy
from os.path import basename
import configparser
import os
from failures import newAccident, send_accident
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
            with open('articules/articules.txt', 'w', encoding='utf-8') as f:
                f.write((f'{articule_title.strip()}\n{articuleDate.strip()}\n{urlPoznan}{articuleLink}'))
            with open('history_tweet/tweet_history_articule.txt', 'w', encoding='utf8') as f:
                f.write(f'{articule_title}')

def send_articule():
    with open('history_tweet/tweet_history_articule.txt', 'r', encoding='utf8') as f:
        last_tweet = f.read().strip()

    newArticule()

    with open('articules/articules.txt', 'r', encoding='utf8') as f:
        articuleTitle = f.readline().strip()
        articuleDate = f.readline().strip()
        articuleLink = f.readline().strip()
    tweet_articule = f"📰{articuleTitle}📰\n{articuleDate}\nDowiedz się więcej: {articuleLink}"
    if last_tweet != articuleTitle:
        api.update_status(tweet_articule)    
        with open('history_tweet/tweet_history_articule.txt', 'w', encoding='utf8') as f:
            f.write(articuleTitle)
        print('Tweet (articule) sent.', articuleTitle)
    else:
        print('Articule already tweeted', articuleTitle)