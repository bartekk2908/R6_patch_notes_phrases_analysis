from matplotlib import pyplot as plt
import json
from counter import FILE_NAME


BACKGROUND_COLOR = '#202343'

font_title = {'family': 'serif',
              'color':  'white',
              'weight': 'bold',
              'size': 28,
              }

font_labels = {'family': 'serif',
               'color':  'white',
               'weight': 'bold',
               'size': 11,
               }


def version_colors(versions):
    seasons_colors = {
        "3.1": "#ffc113",
        "3.2": "#949f39",
        "3.3": "#81a0c1",
        "3.4": "#aa854f",
        "4.1": "#d2005a",
        "4.2": "#304395",
        "4.3": "#156309",
        "4.4": "#089eb3",
        "5.1": "#946a97",
        "5.2": "#447d98",
        "5.3": "#6ca52f",
        "5.4": "#d14008",
        "6.1": "#ab0000",
        "6.2": "#009cbe",
        "6.3": "#f2a63b",
        "6.4": "#5e7531",
        "7.1": "#f2a63b",
        "7.2": "#7dcbb1",
        "7.3": "#d7ca4b",
        "7.4": "#c04126",
        "8.1": "#45abf3",
        "8.2": "#5342aa",
    }
    colors = []
    for v in versions:
        colors.append(seasons_colors[v[:3]])
    return colors


if __name__ == "__main__":

    with open(FILE_NAME, "r") as file:
        counter = json.load(file)

    x = counter.keys()
    y = counter.values()

    plt.figure(facecolor=BACKGROUND_COLOR)
    ax = plt.axes()
    ax.set_facecolor(BACKGROUND_COLOR)

    ax.tick_params(axis='x', which='major', labelsize=7, colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color(BACKGROUND_COLOR)
    ax.spines['right'].set_color(BACKGROUND_COLOR)
    ax.spines['left'].set_color('white')

    plt.title("Number of \"FIX\" phrase in R6 patch notes", fontdict=font_title)
    plt.xlabel("Version", fontdict=font_labels)

    plt.setp(ax.get_xticklabels(), rotation=80, horizontalalignment='right')

    plt.grid(visible=True, axis="y", alpha=0.1)

    plt.bar(x, y, color=version_colors(x))

    plt.show()
