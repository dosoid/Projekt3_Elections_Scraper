README

# Projekt 3 pro Engeto Python Akademii

## Elections scraper

### Popis projektu

Cílem je extrahování výsledků parlamentních voleb v roce 2017 pro vybraný okres z odkazu. Data jsou extrahována pomocí knihovny BeautifulSoup a následně ukládána do formátu CSV.

### Instalace knihoven

Knihovny použité v kódu jsou uložené v souboru requirements.txt.

```sh
pip3 install -r requirements.txt
```

### Spuštění projektu

Soubor main.py se spouští z příkazového řádku a požaduje dva argumenty.

```sh
python3 main.py <odkaz_uzemniho_celku> <vystupni_soubor>
```
Výstupem pak je soubor .csv s výsledky voleb.

### Příklad použití

Vysledky hlasování pro okres Benešov

1. argument: "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"
2. argument: vysledky.csv

Spuštění programu:

```sh
python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky.csv
```

Průběh:

```sh
Stahuji data z vybraného url: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Data byla uložena do souboru vysledky.csv
Ukončuji program Election Scraper
```

Častečný výstup

```sh
Location_code,Location,Registered,Envelopes,Valid,....
529303,Benešov,13 104,8 485,8...
532568,Bernartice,191,148,148,4...
```

Celou výslednou ukázku najdete v souboru vysledky.csv
