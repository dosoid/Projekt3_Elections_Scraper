# README
Elections scraper

Projekt 3 pro Engeto Python Akademii

Popis projektu

Cílem je extrahování výsledků parlamentních voleb v roce 2017 pro vybraný okres z odkazu. Data jsou extrahována pomocí knihovny BeautifulSoup a následně ukládána do formátu CSV.

Instalace knihoven

Knihovny použité v kódu jsou uložené v souboru requirements.txt.

Spuštění projektu

Soubor main.py se spouští z příkazového řádku a požaduje dva argumenty.

python3 main.py <odkaz_uzemniho_celku> <vystupni_soubor>

Výstupem pak je soubor .csv s výsledky voleb.

Příklad použití

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky.csv

