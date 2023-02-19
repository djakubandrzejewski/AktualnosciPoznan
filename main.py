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
from smartcity import newSmartcity, send_smartcity

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




def main():
    while True:
        send_accident()
        send_articule()
        send_smartcity()
        print('waiting')
        time.sleep(2)
if __name__ == "__main__":
    main()
