import sys
import json
import requests
from bs4 import BeautifulSoup

def get_web_page(web_url: str) –> str:
    '''Vratí obsah webové stránky jako string'''

    returt requests.get(web_url).text

def get_soup(web_page: str) -> BeautifulSoup:
    '''Vytvoří objekt BeautifulSoup a připraví k parsování html'''

    return BeautifulSoup(web_page, "html.parser")


def projekt(web_url: str, soubor: str):
    '''Získá data z odkazu a uloží do souboru.csv'''



if __name__ == "__main__":
    print("Tento soubor obsahuje pouze funkce, hlavní projekt je v souboru Projekt_3.py")

