from matplotlib import pyplot as plt
import json
from counter import FILE_NAME


if __name__ == "__main__":

    with open(FILE_NAME, "r") as file:
        counter = json.load(file)

    x = counter.keys()
    y = counter.values()

    fig, ax = plt.subplots()
    ax.tick_params(axis='x', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=20)
    ax.bar(x, y)

    plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
    plt.show()
