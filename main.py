from bs4 import BeautifulSoup
import requests
from collections import Counter
import smtplib
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def remov_duplicates(input):
    input = input.split(" ")

    UniqW = Counter(input)

    s = " ".join(UniqW.keys())
    return s


response = requests.get(url="https://pokemondb.net/pokedex/all", headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

pokemon = soup.find_all(name="tr")

top_stats = 1000
pokemon_dictionary = {}
for pokemon in pokemon:
    number = pokemon.find_next(class_="infocard-cell-data").text
    name = pokemon.find_next(class_="cell-name").text
    name = remov_duplicates(name)
    types = pokemon.find_next(class_="cell-icon").text
    stat_total = pokemon.find_next(class_="cell-num cell-total").text

    pokemon_dictionary[name] = number, types, stat_total


for pokemon in pokemon_dictionary:
    sheet_inputs = {
                "pokemon": {
                    "number": pokemon_dictionary[pokemon][0],
                    "name": pokemon,
                    "type": pokemon_dictionary[pokemon][1],
                    "total": pokemon_dictionary[pokemon][2]
                }
            }
    print(sheet_inputs)
    sheet = requests.post(url="https://api.sheety.co/98fb30f8760553c7667099c51d6e73fa/pokemonInformationSheet/pokemon",
                 json=sheet_inputs)
    print(sheet)
