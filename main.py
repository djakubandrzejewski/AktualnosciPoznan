import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import tweepy
from os.path import basename
import configparser
import twitterAPI
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
tweet_history_file = "tweet_history.txt"

api = tweepy.API(auth)


def newArticule():
    BASE_URL = requests.get('https://www.poznan.pl/').text
    soup = BeautifulSoup(BASE_URL, 'html.parser')
    today = date.today()
    strToday = str(today)
    articules = soup.find_all('section', class_ ='column big')
    for articule in articules:
        if strToday in articuleDate:
            articuleLink = articule.find('a', href=True)
            articuleLink = articuleLink['href']
            articule_title = articule.find('a')
            articule_title = (articule_title['aria-label']).replace(strToday, '')
            articuleImage = articule.find('img')
            articuleImage = articuleImage['data-src']
            urlPoznan = 'http://poznan.pl/'
            articuleImageDownload = urlPoznan.strip(',') + articuleImage.strip()
            articuleImageDownload_response = requests.get(articuleImageDownload)
            with open('images/image.jpg', 'wb') as f:
                f.write(articuleImageDownload_response.content)


            with open('articules/articules.txt', 'w', encoding='utf-8') as f:
                f.write((f'{articule_title.strip()}\n{articuleDate.strip()}\n{urlPoznan}{articuleLink}'))

            with open('tweet_history_file', 'w') as f:
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
        f.write(f'{accidentTitle.strip()}\n{accidentCategory} {urlPoznan}{accidentLink}')   
    with open('tweet_history_file', 'w') as f:
        f.write(f'{accidentTitle}')





def sendArticule(articule):
    old_articule = newArticule()
    if id(articule) != id(old_articule):
        api.update_status(f'{articuleTitle} opublikowany: {articuleDate}\n Link: {articuleLink}')
        
def sendAccident(failure):
    old_failure = newAccident()
    if id(failure) != id(old_failure):
        api.update_status((f'{accidentTitle} opublikowany: {accidentDate}\n Link: {accidentLink}'))
    
def add_tweet(tweet):
    for existing_tweet in tweets:
        if existing_tweet == tweet:
            return
    tweets.append(tweet)


if __name__ == '__main__':
    sent_tweets = set()
    tweet_history = set()
    while True:
        time_wait = 1
        print(f'Sprawdzania nowego artykulu za: {time_wait} sekund.')
        time.sleep(1)
        tweets = []
        with open('articules/articules.txt', 'r', encoding='utf8') as f:
            articuleTitle = f.readline().strip()
            articuleDate = f.readline().strip()
            articuleLink = f.readline().strip()
        with open('failures/failures.txt', 'r', encoding='utf8') as f:
            accidentTitle = f.readline().strip()
            accidentDate = f.readline().strip()
            accidentLink = f.readline().strip()
        
        if articuleTitle not in sent_tweets:
            try:
                sendArticule(newArticule)
                sent_tweets.add(articuleTitle)
            except tweepy.errors.Forbidden:
                time.sleep(1)
        
        if accidentTitle not in sent_tweets:
            try:
                sendAccident(newAccident)
                sent_tweets.add(accidentTitle)
            except tweepy.errors.Forbidden:
                time.sleep(1)
            
