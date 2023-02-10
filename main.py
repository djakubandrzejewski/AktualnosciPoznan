import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import tweepy
from os.path import basename
import configparser
import os

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


            with open('articules/articules.txt', 'w', encoding='utf-8') as f:
                f.write((f'{articule_title.strip()}\n{articuleDate.strip()}\n{urlPoznan}{articuleLink}'))

    with open('tweet_history_articule.txt', 'w') as f:
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
    with open('tweet_history_accident.txt', 'w') as f:
        f.write(f'{accidentTitle}')



def sendArticule(articule):
    with open('tweet_history_articule.txt', 'r') as history:
        historyTweet = history.readline()
    with open('articules/articules.txt', 'r') as articule:
        articuleTweet = articule.readline()
    if historyTweet != articuleTweet:
        api.update_status(f'📰{articuleTitle}📰\n{articuleDate}\nDowiedz się więcej:{articuleLink}')

        
def sendAccident(failure):
    with open('tweet_history_accident.txt', 'r') as history:
        historyTweet = history.readline()
    with open('failures/failures.txt', 'r') as failure:
        accidentTweet = failure.readline()
    if historyTweet != accidentTweet:
        tweet = f'❗{accidentTitle}❗\n Dowiedz się więcej: {accidentLink}'
        api.update_status_with_media(filename="image/smartcity.png",status=tweet)



def read_first_line(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline()
    return first_line


if __name__ == '__main__':

    firstLineOfArticule = read_first_line('tweet_history_articule.txt')
    firstLineOfAccident = read_first_line('tweet_history_accident.txt')
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
        
        if articuleTitle != firstLineOfArticule:
            try:
                
                sendArticule(newArticule)
                sent_tweets.add(articuleTitle)
            except tweepy.errors.Forbidden:
                time.sleep(1)
        
        if accidentTitle != firstLineOfAccident:
            try:
                sendAccident(newAccident)
                sent_tweets.add(accidentTitle)
            except tweepy.errors.Forbidden:
                time.sleep(1)
