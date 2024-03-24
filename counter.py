from re import findall
from requests import get
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import os
from time import sleep


webpage_content_file_name = "webpages_content"

distributions_dir_name = "distributions"

patch_notes_urls = {}
try:
    with open("urls.txt", "r") as file:
        for line in file:
            version, url = line.split(" ", 1)
            patch_notes_urls[version] = url[:-1]
except FileNotFoundError:
    print(f"Can't find 'urls.txt' file.")


def count_word(word, saved_webpages_content=True, logs=True):
    counter_for_version = {}
    distribution_file_name = f"{word}_distribution.json"

    # Create directory for JSON files if it doesn't exist
    if not os.path.exists(distributions_dir_name):
        os.makedirs(distributions_dir_name)

    # Get already saved content of patch notes webpages
    is_file = os.path.isfile(f"{webpage_content_file_name}.json")
    if is_file and saved_webpages_content:
        with open(f"{webpage_content_file_name}.json", "r") as file:
            webpages_content = json.load(file)
    else:
        webpages_content = {}

    # Downloading content of webpages if needed
    print("Downloading content of webpages...") if logs else None
    sleep(0.1)
    for version in tqdm(patch_notes_urls.keys(), unit="version", disable=not logs):
        if not webpages_content.get(version):
            req = get(patch_notes_urls[version])
            soup = BeautifulSoup(req.content, 'html.parser')
            webpages_content[version] = soup.find_all("div", {"class": "updatesDetail__article__content"})[0].get_text()

    sleep(0.1)

    # Get count of word for each patch notes
    print("Counting phrases...") if logs else None
    sleep(0.1)
    for version in tqdm(patch_notes_urls.keys(), unit="version", disable=False if logs else True):
        counter_for_version[version] = len(findall(word.lower(), webpages_content[version].lower()))

    # Save new/updated webpages content to JSON file
    with open(f"{webpage_content_file_name}.json", "w") as file:
        json.dump(webpages_content, file)

    # Save counter to JSON file
    with open(f"{distributions_dir_name}\\{distribution_file_name}", "w") as file:
        json.dump(counter_for_version, file)


if __name__ == "__main__":
    w = "fixed"
    count_word(word=w, saved_webpages_content=True)
