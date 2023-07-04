from counter import *
from chart import *


if __name__ == "__main__":

    try:
        words = []
        with open("words.txt", "r") as file:
            for line in file:
                words.append(line[:-1])
    except FileNotFoundError:
        print(f"Can't find 'words.txt' file.")
        exit()

    for w in words:
        print(f"\nWord: {w}")
        count_word(w, saved_webpages_content=True, logs=False)
        for sts in [False, True]:
            make_chart(*get_distribution(w), w, sum_to_seasons=sts)
