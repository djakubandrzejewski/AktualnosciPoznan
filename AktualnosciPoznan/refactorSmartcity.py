import requests
from bs4 import BeautifulSoup
from datetime import date
import time


def newSmartcity():
    BASE_URL = requests.get("https://poznan.pl/mim/smartcity/news/", verify=False).text
    soup = BeautifulSoup(BASE_URL, 'html.parser')

    smartcity = soup.find('article', class_='clearfix')

    smartcityLink = smartcity.find('a', href=True)
    smartcityLink = smartcityLink['href']

    smartcityTitle = smartcity.find('h2').text

    smartcityDate = smartcity.find('time').text

    print(f"Link:{smartcityLink}")
    print(f"Tytul:{smartcityTitle}")
    print(f"Data:{smartcityDate}")


newSmartcity()