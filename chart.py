from matplotlib import pyplot as plt
import json
from numpy import nanmean
import os


charts_dir_name = "charts"
distributions_dir_name = "distributions"

BACKGROUND_COLOR = '#202343'
CHART_COLOR = 'white'

font_title = {'family': 'impact',
              'color':  CHART_COLOR,
              'weight': 'bold',
              'size': 28,
              }

font_labels = {'family': 'impact',
               'color':  CHART_COLOR,
               'weight': 'bold',
               'size': 13,
               }

font_legend = {'family': 'impact',
               'weight': 'bold',
               'size': 10,
               }


def version_colors(versions):
    seasons_colors = {}
    try:
        with open("colors_of_seasons.txt", "r") as file:
            for line in file:
                version, color = line.split(" ", 1)
                seasons_colors[version] = color[:-1]
    except FileNotFoundError:
        print(f"Can't find 'colors_of_seasons.txt' file.")

    colors = []
    for v in versions:
        if seasons_colors.get(v[:3]):
            colors.append(seasons_colors[v[:3]])
        else:
            colors.append(CHART_COLOR)
    return colors


def make_chart(word):
    file_name = f"{word}_distribution.json"

    try:
        with open(f"{distributions_dir_name}\\{file_name}", "r") as file:
            counter = json.load(file)
    except FileNotFoundError:
        if not os.path.exists(distributions_dir_name):
            print(f"Can't find '{distributions_dir_name}' directory.")
        else:
            print(f"Can't find JSON file of '{word}' phrase distribution."
                  f" Make sure that '{word}_distribution.json' file is in '{distributions_dir_name}' directory.")
        exit()

    x = counter.keys()
    y = counter.values()

    # background
    plt.figure(facecolor=BACKGROUND_COLOR, figsize=(20.0, 10.5))
    ax = plt.axes()
    ax.set_facecolor(BACKGROUND_COLOR)

    # axis labels
    ax.tick_params(axis='x', which='major', labelsize=7, colors=CHART_COLOR)
    ax.tick_params(axis='y', colors=CHART_COLOR)
    ax.yaxis.label.set_color(CHART_COLOR)
    ax.xaxis.label.set_color(CHART_COLOR)
    plt.setp(ax.get_xticklabels(), rotation=80, horizontalalignment='right')

    # borders of chart
    ax.spines['bottom'].set_color(CHART_COLOR)
    ax.spines['top'].set_color(BACKGROUND_COLOR)
    ax.spines['right'].set_color(BACKGROUND_COLOR)
    ax.spines['left'].set_color(CHART_COLOR)

    # title and x axis label
    plt.title(f"Number of \"{word.upper()}\" phrase in R6 patch notes", fontdict=font_title)
    plt.xlabel("patch", fontdict=font_labels)

    # horizontal grid
    plt.grid(visible=True, axis="y", alpha=0.1)

    # bars
    plt.bar(x, y, color=version_colors(x))

    # average of every version line
    plt.axhline(y=nanmean(list(y)), linestyle=":",
                color=CHART_COLOR, linewidth=1.5,
                label="every patch avg", alpha=0.3)
    # average of first versions of seasons
    plt.axhline(y=nanmean([list(y)[i] for i, k in enumerate(x) if k[-2:] == ".0"]),
                linestyle="--", color=CHART_COLOR, linewidth=1,
                label="first patches of seasons avg", alpha=0.3)

    # legend
    plt.legend(loc=(0.85, 0.87), labelcolor=CHART_COLOR, reverse=True, facecolor=BACKGROUND_COLOR, edgecolor=BACKGROUND_COLOR, prop=font_legend)

    # plt.show()

    # Create directory for PNG files if it doesn't exist
    if not os.path.exists(charts_dir_name):
        os.makedirs(charts_dir_name)

    plt.savefig(f"{charts_dir_name}\\{word}_chart.png", dpi=600)


if __name__ == "__main__":
    w = "fix"
    make_chart(w)
