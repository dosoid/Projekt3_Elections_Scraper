"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Evžen Oskin
email: dos333@seznam.cz
"""

import sys
import json
import requests
from bs4 import BeautifulSoup
import projekt_3_funkce as funkce

if __name__ == "__main__":

    web_url = sys.argv[1]
    soubor = sys.argv[2]
    
    web_page = funkce.get_web_page(web_url)
    soup = funkce.get_soup(web_page)