from re import findall
from requests import get
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import os


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

distributions_dir_name = "distributions"

patch_notes_urls = {}
with open("urls.txt", "r") as file:
    for line in file:
        version, url = line.split(" ", 1)
        patch_notes_urls[version] = url[:-1]


def count_word(word="fix"):
    counter_for_version = {}
    file_name = f"{word}_distribution.json"

    if not os.path.exists(distributions_dir_name):
        os.makedirs(distributions_dir_name)

    is_file = os.path.isfile(f"{distributions_dir_name}\\{file_name}")
    if is_file:
        with open(f"{distributions_dir_name}\\{file_name}", "r") as file:
            old_counter = json.load(file)
    else:
        old_counter = {}

    for version in tqdm(patch_notes_urls.keys(), unit="version"):
        if old_counter.get(version):
            counter_for_version[version] = old_counter[version]
        else:
            req = get(patch_notes_urls[version], headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            counter_for_version[version] = len(findall(word.lower(), soup.get_text().lower()))

    with open(f"{distributions_dir_name}\\{file_name}", "w") as file:
        json.dump(counter_for_version, file)


if __name__ == "__main__":
    w = "fix"
    count_word(w)
