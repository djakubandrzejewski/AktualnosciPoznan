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

api = tweepy.API(auth)

def newArticule():
    BASE_URL = requests.get('https://www.poznan.pl/').text
    soup = BeautifulSoup(BASE_URL, 'html.parser')
    today = date.today()
    strToday = str(today)
    articules = soup.find_all('section', class_ ='column big')
    for articule in articules:
        articuleDate = articule.find('time').text.replace('', '')
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
                f.write((f'{articule_title.strip()}\n{articuleDate.strip()}\nhttps://www.poznan.pl{articuleLink}'))

def sendArticule(articule):
    old_articule = newArticule()
    if articule != old_articule:
        api.update_status(f'Artykuł: {articuleTitle} opublikowany: {articuleDate}\n Link: {articuleLink}')
        



if __name__ == '__main__':
    while True:
        newArticule()
        time_wait = 1
        print(f'Sprawdzania nowego artykulu za: {time_wait} sekund.')
        time.sleep(1)
        with open('articules/articules.txt', 'r', encoding='utf8') as f:
            articuleTitle = f.readline().strip()
            articuleDate = f.readline().strip()
            articuleLink = f.readline().strip()
        


        try:
            sendArticule(newArticule)
        except tweepy.errors.Forbidden:
            time.sleep(1)

            




# 600 - 10 minut
# 60 -  1 minut
# 6 - 1 sekunda