"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Evžen Oskin
email: dos333@seznam.cz
"""

import sys
import json
import csv
import requests
from bs4 import BeautifulSoup

def get_web_page(web_url: str) -> str:
    '''Vratí obsah webové stránky jako string'''

    return requests.get(web_url).text

def get_soup(web_page: str) -> BeautifulSoup:
    '''Vytvoří objekt BeautifulSoup a připraví k parsování html'''

    return BeautifulSoup(web_page, "html.parser")

def odkaz_na_obec(soup: BeautifulSoup) -> tuple:
    '''Vrátí seznam odkazů na obce'''

    obce_cisla = []
    obce_nazvy = []
    odkazy = []
    radky = soup.find_all("tr")

    for radek in radky:
        cislo_bunka = radek.find("td", class_="cislo")
        nazev_bunka = radek.find("td", class_="overflow_name")
        odkaz = radek.find("a")

        if cislo_bunka and nazev_bunka and odkaz:
            odkazy.append(odkaz["href"])
            obce_cisla.append(cislo_bunka.text.strip())
            obce_nazvy.append(nazev_bunka.text.strip())
   

    return obce_cisla, obce_nazvy, odkazy


def table_work(soup: BeautifulSoup, tabulka: int, sloupec: int) -> list:
    '''Zpracuje tabulku na stance'''

    vysledek = []
    tabulky = soup.find_all("table", class_="table")
    radky = tabulky[tabulka].find_all("tr")[2:]

    for radek in radky:
        bunky = radek.find_all("td")
        if len(bunky) >= 3:
            vysledek.append(bunky[sloupec].text.strip())

    return vysledek

def web_scrape(soup: BeautifulSoup, code_obec: str, name_obec: str) -> dict:
    '''Vrátí slovník s daty z webové stránky'''

    vysledek = dict()

    tabulky = soup.find_all("table", class_="table") # najde v html všechny tabulky s třídou table

    tabulka_jedna = tabulky[0] # první tabulka na stránce
    radky_tabulka_jedna = tabulka_jedna.find_all("tr")[2:] # řádky z 1. tabulky

    for radek in radky_tabulka_jedna:
        bunky = radek.find_all("td")
        pocet_volicu = bunky[3].text.strip() # vrátí počet voličů
        vydane_obalky = bunky[4].text.strip() # vrátí počet vydaných obálek
        platne_hlasy = bunky[7].text.strip() # vrátí počet platných hlasů
    
    strany = table_work(soup, 1, 1) + (table_work(soup, 2, 1)) # vrátí seznam stran
    hlasy = table_work(soup, 1, 2) + (table_work(soup, 2, 2)) # vrátí seznam hlasů

    vysledek["Location_code"] = code_obec
    vysledek["Location"] = name_obec
    vysledek["Registered"] = pocet_volicu
    vysledek["Envelopes"] = vydane_obalky
    vysledek["Valid"] = platne_hlasy
    vysledek["Partys"] = strany
    vysledek["Voice_count"] = hlasy
    
    return vysledek

def save_to_csv(vysledek: dict, soubor: str, headless: bool) -> None:
    '''Uloží všechna data do csv souboru'''
    
    write_mode = "w" if headless else "a"
    with open(soubor, mode=write_mode, encoding="utf-8", newline="") as file:
        zapisovac = csv.writer(file)
        if headless:
            head = ["Code", "Location", "Registered", "Envelopes", "Valid"] + vysledek["Partys"]
            zapisovac.writerow(head)

        content = [vysledek["Location_code"], vysledek["Location"], vysledek["Registered"], vysledek["Envelopes"], vysledek["Valid"]] + vysledek["Voice_count"]
        zapisovac.writerow(content)




if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Type: python projekt_3.py <url> <soubor.csv>")
        sys.exit(1)
    url_obec = sys.argv[1]
    soubor = sys.argv[2]
    obsah_obec = get_web_page(url_obec)
    soup_obec = get_soup(obsah_obec)
    obce_cislo, obce_nazvy, obce_odkaz = odkaz_na_obec(soup_obec)
 
   
    for index, odkaz in enumerate(obce_odkaz):
        url = f"https://www.volby.cz/pls/ps2017nss/{odkaz}"
    
        obsah = get_web_page(url)
        soup = get_soup(obsah)
        vysledek = web_scrape(soup, obce_cislo[index], obce_nazvy[index])
        save_to_csv(vysledek, soubor, headless=(index == 0))
    print(f"Data byla uložena do souboru {soubor}")


