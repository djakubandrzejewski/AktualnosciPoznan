import requests
from bs4 import BeautifulSoup
from datetime import date
import time



def newAccidentTransport():
    BASE_URL = requests.get('https://poznan.pl/mim/smartcity/news,9281/', verify=False).text
    soup = BeautifulSoup(BASE_URL, 'html.parser')

    accidents = soup.find('article', class_='clearfix')

    accidentLink = accidents.find('a', href=True)
    accidentLink = accidentLink['href']

    accidentTitle = accidents.find('h2').text

    accidentDate = accidents.find('time').text

    urlPoznan = "https://poznan.pl/"
    print(f"Link:{accidentLink}")
    print(f"Tytul:{accidentTitle}")
    print(f"Czas trwania: {accidentDate}")

    with open('accident.txt', 'w', encoding='utf-8') as f:
            f.write((f'{accidentTitle.strip()}\n{accidentDate.strip()}\n{urlPoznan}{accidentLink}'))
    with open('accidentHistory.txt', 'w', encoding='utf8') as f:
            f.write(f'{accidentTitle}')

newAccidentTransport()



#wywalic artykuly i zostawic tylko smartcity
#pododawac kategorrie odnosnie komunikatow
#Bezpieczenestwo 1191
#Transport 9281
#Awarie 9280
#wyrzucic wszystkie Tweety
"""
wyjebac artykuly z main strony
dac 3 nowe funkcje z awarii transport bezpieczenstwo
zmienic smartcity
wrzucic na crona i zobaczyc jak dziala
"""