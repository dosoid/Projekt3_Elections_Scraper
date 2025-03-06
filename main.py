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

def point_to_loc(soup: BeautifulSoup) -> tuple:
    '''Vrátí seznam pointerů na obce'''

    loc_number = [] # seznam čísel obcí
    loc_name = [] # seznam názvů obcí
    pointers = [] # seznam pointerů na obce
    lines = soup.find_all("tr") # najde všechny řádky

    for line in lines:
        cell_number = line.find("td", class_="cislo")
        cell_name = line.find("td", class_="overflow_name")
        pointer = line.find("a")

        if cell_number and cell_name and pointer:
            pointers.append(pointer["href"])
            loc_number.append(cell_number.text.strip())
            loc_name.append(cell_name.text.strip())
   

    return loc_number, loc_name, pointers


def table_work(soup: BeautifulSoup, tabulka: int, sloupec: int) -> list:
    '''Zpracuje tabulku na stance'''

    result = []
    tables = soup.find_all("table", class_="table")
    lines = tables[tabulka].find_all("tr")[2:]

    for line in lines:
        cells = line.find_all("td")
        if len(cells) >= 3:
            result.append(cells[sloupec].text.strip())

    return result

def web_scrape(soup: BeautifulSoup, location_code: str, location_name: str) -> dict:
    '''Vrátí slovník s daty z webové stránky'''

    result = dict()

    tables = soup.find_all("table", class_="table") # najde v html všechny tables s třídou table

    table_one = tables[0] # první tabulka na stránce
    lines_table_one = table_one.find_all("tr")[2:] # řádky z 1. tables

    for line in lines_table_one:
        cells = line.find_all("td")
        voters_count = cells[3].text.strip() # vrátí počet voličů
        issued_envelopes = cells[4].text.strip() # vrátí počet vydaných obálek
        valid_votes = cells[7].text.strip() # vrátí počet platných hlasů
    
    political_partys = table_work(soup, 1, 1) + (table_work(soup, 2, 1)) # vrátí seznam stran
    votes = table_work(soup, 1, 2) + (table_work(soup, 2, 2)) # vrátí seznam hlasů

    result["Location_code"] = location_code
    result["Location"] = location_name
    result["Registered"] = voters_count
    result["Envelopes"] = issued_envelopes
    result["Valid"] = valid_votes
    result["Political_partys"] = political_partys
    result["Voice_count"] = votes
    
    return result

def save_to_csv(result: dict, soubor: str, headless: bool) -> None:
    '''Uloží všechna data do csv souboru'''
    
    write_mode = "w" if headless else "a"
    with open(soubor, mode=write_mode, encoding="utf-8", newline="") as file:
        zapisovac = csv.writer(file)
        if headless:
            head = ["Location_code", "Location", "Registered", "Envelopes", "Valid"] + result["Political_partys"]
            zapisovac.writerow(head)

        content = [result["Location_code"], result["Location"], result["Registered"], result["Envelopes"], result["Valid"]] + result["Voice_count"]
        zapisovac.writerow(content)




if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Type: python projekt_3.py <url> <soubor.csv>")
        sys.exit(1)
    url_loc = sys.argv[1]
    soubor = sys.argv[2]
    content_loc = get_web_page(url_loc)
    soup_obec = get_soup(content_loc)
    loc_number, loc_name, loc_pointer = point_to_loc(soup_obec)
 
   
    for index, pointer in enumerate(loc_pointer):
        url = f"https://www.volby.cz/pls/ps2017nss/{pointer}"
    
        content = get_web_page(url)
        soup = get_soup(content)
        result = web_scrape(soup, loc_number[index], loc_name[index])
        save_to_csv(result, soubor, headless=(index == 0))
    print(f"Data byla uložena do souboru {soubor}")


