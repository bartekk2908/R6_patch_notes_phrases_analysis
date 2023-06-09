from re import findall
from requests import get
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from os.path import isfile


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

patch_notes_urls = {
    "3.1.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/338U35A3jskG4DPMrUAwcY",
    "3.1.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/2xnVeIL4RABFg1XWcvCgtH",
    "3.2.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/6pEtYtyWisZf14LdqAcVfa",
    "3.2.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/6i8cYfwPW51OY74AJVOTQv",
    "3.2.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/M8eD0b4CPihVbhJizbte2",
    "3.3.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/7y2kQGd9m08h89j7usuXiZ",
    "3.3.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5hzvWfJ2PneczWy11i5YgO",
    "3.3.1.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/3LwFGv82G9gF9DqJ19BkeR",
    "3.3.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/3gjWQ8fMoge0iDMtsFRUkf/y3s32-patch-notes",
    "3.4.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/LkCrjdAXnSXMr909or9Lp/y3s4-patch-notes-addendum",
    "3.4.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/1WhXpnmmRHqhTNvKl1QMRP/y3s41-patch-notes",
    "3.4.2": "https://www.ubisoft.com/en-ca/game/rainbow-six/siege/news-updates/qkEtGtzqDf6xyFs5SjOsV/y3s42-patch-notes",
    "4.1.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/7H0nLhI9TijO1oa9t2I1PA/y4s1-burnt-horizon-patch-notes-addendum",
    "4.1.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/1wAigSUF1TMZhmn7l4bIGl/y4s1.1-patch-notes",
    "4.1.2": "https://www.ubisoft.com/en-ca/game/rainbow-six/siege/news-updates/2mY2NPyrt5YjND1mCWmkA9/y4s1.2-patch-notes",
    "4.1.3": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/111DnmJVti04F7FRLGikDl/y4s1.3-patch-notes",
    "4.2.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/1Q1WJE9RzEo2YgawegUT8v/y4s2-patch-notes-addendum",
    "4.2.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/2Cu9jB5INfTaNWYLlJS8Ng/y4s21-patch-notes",
    "4.2.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/4oMqRauYdU29BUUDMeRhdb/y4s22-patch-notes",
    "4.2.3": "https://www.ubisoft.com/en-ca/game/rainbow-six/siege/news-updates/1gWxzOpDKUThMgW7usLz4n/y4s2.3-patch-notes",
    "4.3.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/68yopyiTymUw3hTH8i7csx/y4s3-ember-rise-patch-notes-addendum",
    "4.3.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/6inHTieNHnz15VUeZYQ0mk/y4s3.1-patch-notes",
    "4.3.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/1kyzlgyZfKDhCDlVLlX1s9/y4s32-patch-notes",
    "4.3.3": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/2SYqHd919GLVhLswSOpmKY/y4s33-patch-notes",
    "4.4.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/Y754L5blJTDmMD0mmY9be/y4s4-shifting-tides-patch-notes-addendum",
    "4.4.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/16aCp6SD21srYEjBWz8rsS/y4s41-patchnotes",
    "4.4.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/3wFfmd9yTUXy9arSYh1IyL/y4s4.2-patch-notes",
    "4.4.3": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/3nC1sOyNkEt3Kw8MfHUvvj",
    "5.1.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/4Yr3NSbqrMf305JoV9igdu",
    "5.1.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5O4NZLCGCXvahaLWj6Yzdj/y5s11-patch-notes",
    "5.1.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/4QAhnXnPk7Ffse8scw3k0Z/y5s12-patch-notes",
    "5.2.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/6ZAUq5r1JwOfFWsvlvLBmW/y5s2-steel-wave-patch-notes-addendum",
    "5.2.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/1gM2zQmnrHrOND4YtgsDFy/y5s21-patch-notes",
    "5.2.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/211yXFjWZrOuHcEjN1uL4X/y5s22-patch-notes",
    "5.2.3": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/77zg9g8ruBc3K6FlRJIooQ",
    "5.3.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/3D6v1UHB1uL9bJRhVBshjw",
    "5.3.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/KUQ0lqkyGNmQHZGji5oO7",
    "5.3.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/59NsvOS5yiF2zrSRPq0mEL",
    "5.3.3": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/4zw9z2LVwYzjqbu6Dxs2mx",
    "5.4.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/37OWCWpDjEuE0rCcNMMu8m",
    "5.4.1": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/1hovQi352rwiTKyb5c8cyH",
    "5.4.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/uFFCdFX2fwTayoDtZSCKK",
    "5.4.3": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/5Zhi3DUCuQAz3k3P1qbSyL",
    "6.1.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/2aVk29GIryIx6CNXtfz6LW",
    "6.1.1": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/DxDeyDzzW11lK12ikVPWN/y6s11-patch-notes",
    "6.1.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5ASwSUq1CZcQdyXNWoHedF",
    "6.1.3": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/4vvqslbIykRrOKnb3XbCPd",
    "6.2.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/3gJRBcbp6vGmbGscAWj61k",
    "6.2.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/w9foYj4j0oumm9ydFrXJY",
    "6.2.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/5ZMF9L4RORllBhrRV618tr",
    "6.3.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/4DWOjAkLM70Yma491GE4qm",
    "6.3.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5o0onUmj3Sd5wc2ei18Dsd",
    "6.3.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5AsMMjZyakGlJWN6fhKnVP",
    "6.4.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/4z12b55jc54EgsB8PKAeD7",
    "6.4.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5F5lSqxuI2iYkr8oZxhBan",
    "6.4.2": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/AAAzimMg8bPRW3c1jKVDl",
    "7.1.0": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5uvJIketTRZux4L1T4I3Ij",
    "7.1.1": "https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/5bkGPo8PkQKUfuXByhMoPx",
    "7.1.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/4vjuyUcQI9YPAJovw6WCgE/y7s12-patch-notes",
    "7.1.3": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/19uFROeb5EjABdx9lpagmy/y7s13-patch-notes",
    "7.2.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/5sNMTeAQ47ee9eHVHjvMfg/y7s2-vector-glare-patch-notes-addendum",
    "7.2.1": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/bU0FMHNhGGUzK06jvxSPQ/y7s21-patch-notes",
    "7.2.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/3QHRUp1wCuYkvBO6Je3vks/y7s22-patch-notes",
    "7.3.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/3JpgtLQda8bguEszwc463t/y7s3-brutal-swarm-patch-notes-addendum",
    "7.3.1": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/6MFGlAr4DsazNMQTdo3OWg/y7s31-patch-notes",
    "7.3.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/35shNBmvLhISODLtrkHuho/y7s32-patch-notes",
    "7.3.3": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/5ocCvLzVrsNA8ijFZ9br5a/y7s33-patch-notes",
    "7.4.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/3B6S7OndSJ5XmWZQ2Se49R/y7s4-solar-raid-patch-notes-addendum",
    "7.4.1": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/40AMYojKZDvQfTO5j0W5rZ/y7s41-patch-notes",
    "7.4.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/5W4Tn6l3RvzhbnKDYBMDTl/y7s42-patch-notes",
    "8.1.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/1xLJqGTce4nquXpg4cZYDC/y8s1-commanding-force-patch-notes-addendum",
    "8.1.1": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/y68BmuBkDaaIkoOPZEk4c/y8s11-patch-notes",
    "8.1.2": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/HTkVw1mAg7DuA2ZKWCKe0/y8s12-patch-notes",
    "8.2.0": "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/news-updates/6a5uYfFF2CsJh1fjXSWrzK/y8s2-operation-dread-factor-patch-notes-addendum",
}

FILE_NAME = "counter_for_version.json"


if __name__ == "__main__":

    word = "FIX"
    counter_for_version = {}

    is_file = isfile(FILE_NAME)
    if is_file:
        with open(FILE_NAME, "r") as file:
            old_counter = json.load(file)

    for version in tqdm(patch_notes_urls.keys(), unit="version"):
        if old_counter.get(version):
            counter_for_version[version] = old_counter[version]
        else:
            req = get(patch_notes_urls[version], headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            counter_for_version[version] = len(findall(word, soup.get_text().upper()))

    with open(FILE_NAME, "w") as file:
        json.dump(counter_for_version, file)
