from bs4 import BeautifulSoup
import requests


def lookup():
    r = requests.get('https://aznps.com/the-plant-list/')
    r.text()