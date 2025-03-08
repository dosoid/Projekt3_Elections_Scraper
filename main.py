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
    try:
        return requests.get(web_url).text
    
    except requests.exceptions.RequestException as error:
        print(f"Chyba při stahování stránky: {error}")
        sys.exit(1)

def get_soup(web_page: str) -> BeautifulSoup:
    '''Vytvoří objekt BeautifulSoup a připraví k parsování html'''

    return BeautifulSoup(web_page, "html.parser")

def get_loc_number(lines) -> list:
    '''Vrátí seznam čísel obcí'''
    
    return [line.find("td", class_="cislo").text.strip() for line in lines if line.find("td", class_="cislo")]

def get_loc_name(lines) -> list:
    '''Vrátí seznam názvů obcí'''

    return [line.find("td", class_="overflow_name").text.strip() for line in lines if line.find("td", class_="overflow_name")]

def get_pointers(lines) -> list:
    '''Vrátí seznam odkazů na obce'''

    return [line.find("a")["href"] for line in lines if line.find("a")]

def point_to_loc(soup: BeautifulSoup) -> tuple:
    '''Vrátí seznam odkazů na obce'''

    lines = soup.find_all("tr") # najde všechny řádky

    return get_loc_number(lines), get_loc_name(lines), get_pointers(lines)


def table_work(soup: BeautifulSoup, table: int, column: int) -> list:
    '''Zpracuje tabulku na stance'''

    result = []
    tables = soup.find_all("table", class_="table")

    if len(tables) > table:
        lines = tables[table].find_all("tr")[2:]
        for line in lines:
            cells = line.find_all("td")
            if len(cells) >= column:
                result.append(cells[column].text.strip())

    return result

def web_scrape(soup: BeautifulSoup, location_code: str, location_name: str) -> dict:
    '''Vrátí slovník s daty z webové stránky'''

    result = dict() # vytvoří slovník pro uložení dat

    tables = soup.find_all("table", class_="table") # najde v html všechny tabulky s třídou table

    if tables: 
        table_one = tables[0] # první tabulka na stránce
        lines_table_one = table_one.find_all("tr")[2:] # řádky z 1. tabulky

        for line in lines_table_one:
            cells = line.find_all("td")
            if len(cells) > 7:
                result["Registered"] = cells[3].text.strip() # vrátí počet voličů
                result["Envelopes"] = cells[4].text.strip() # vrátí počet vydaných obálek
                result["Valid"] = cells[7].text.strip() # vrátí počet platných hlasů
        
    result["Political_partys"] = table_work(soup, 1, 1) + (table_work(soup, 2, 1)) # vrátí seznam stran
    result["Voice_count"] = table_work(soup, 1, 2) + (table_work(soup, 2, 2)) # vrátí seznam hlasů
    result["Location"] = location_name # vrátí název obce
    result["Location_code"] = location_code # vrátí číslo obce
    
    return result

def save_to_csv(result: dict, soubor: str, headless: bool) -> None:
    '''Uloží všechna data do csv souboru'''
    
    write_mode = "w" if headless else "a" # v případě 1.zápisu vytvoří soubor, jinak přidává data
    with open(soubor, mode=write_mode, encoding="utf-8", newline="") as file:
        zapisovac = csv.writer(file)
        if headless:
            head = ["Location_code", "Location", "Registered", "Envelopes", "Valid"] + result["Political_partys"]
            zapisovac.writerow(head)

        content = [result["Location_code"], result["Location"], result["Registered"], result["Envelopes"], result["Valid"]] + result["Voice_count"]
        zapisovac.writerow(content)

def print_usage(): 
    '''Vypíše to terminálu správné použití programu'''

    print("\n Správné použití příklad:")
    print("   python3 main.py \"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101\" vysledky.csv\n")

def check_url_response(url: str) -> bool:
    '''Ověří, zda je URL dostupná'''
    
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
def arguments_check(url: str, file: str) -> bool:
    '''Kontroluje zda byly zadány správné argumenty'''

    if not url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("Špatný formát url adresy")

        return False
    
    if not check_url_response(url):
        print("URL není dostupná")

        return False
    
    if not file.endswith(".csv"):
        print("Druhý argument musí být format souboru s příponou .csv")

        return False
    
    return True



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Použití: python3 main.py <url> <soubor.csv>")
        sys.exit(1)
    url_loc = sys.argv[1]
    file = sys.argv[2]

    if not arguments_check(url_loc, file):
        print_usage()
        sys.exit(1)

    try:
        content_loc = get_web_page(url_loc) # stažení obsahu webové stránky
        soup_location = get_soup(content_loc) # vytvoření objektu BeautifulSoup
        print(f"Stahuji data z vybraného url: {url_loc}")
        loc_number, loc_name, loc_pointer = point_to_loc(soup_location) # získání seznamů čísel obcí, názvů obcí a odkazů na obce
    
        for index, pointer in enumerate(loc_pointer):
            url = f"https://www.volby.cz/pls/ps2017nss/{pointer}"
            content = get_web_page(url)
            soup = get_soup(content)
            result = web_scrape(soup, loc_number[index], loc_name[index])
            save_to_csv(result, file, headless=(index == 0))

        print(f"Data byla uložena do souboru {file}")
        print("Ukončuji program Election Scraper")
        sys.exit(0)

    except Exception as error:
        print(f"Chyba: {error}")
        sys.exit(1)

