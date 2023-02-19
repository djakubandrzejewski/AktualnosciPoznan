import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import tweepy
from os.path import basename
import configparser
import os
from failures import newAccident, send_accident
from articules import newArticule, send_articule

configAPI = configparser.ConfigParser()
configAPI.read('config.ini')

api_key = configAPI['twitter']['api_key']
api_key_secret = configAPI['twitter']['api_key_secret']

access_token = configAPI['twitter']['access_token']
access_token_secret = configAPI['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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
    with open('history_tweet/tweet_history_smartcity.txt', 'r',encoding='utf8') as f:
        last_tweet = f.read().strip()

    newSmartcity()


    with open('smartcity/smartcity.txt', 'r', encoding='utf8') as f:
        articuleTitle = f.readline().strip()
        articuleDate = f.readline().strip()
        articuleLink = f.readline().strip()

    tweet_articule = f"📰{articuleTitle}📰\n{articuleDate}\nDowiedz się więcej: {articuleLink}"
    if last_tweet != articuleTitle:
        api.update_status(tweet_articule)
        with open('history_tweet/tweet_history_smartcity.txt', 'w', encoding='utf8') as f:
            f.write(articuleTitle)
            print('Tweet smartcity sent.', articuleTitle)
    else:
        print('SmartCity already tweeted', articuleTitle)
