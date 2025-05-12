from matplotlib import pyplot as plt
import json
from numpy import nanmean
import os


charts_dir_name = "charts"
distributions_dir_name = "distributions"
colors_file_name = "colors"

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
               'size': 14,
               }


def version_colors(versions):
    seasons_colors = {}
    try:
        with open(f"{colors_file_name}.txt", "r") as file:
            for line in file:
                version, color = line.split(" ", 1)
                seasons_colors[version] = color[:-1]
    except FileNotFoundError:
        print(f"Can't find '{colors_file_name}.txt' file.")

    colors = []
    for v in versions:
        season = '.'.join(v.split('.')[:2])
        if seasons_colors.get(season):
            colors.append(seasons_colors[season])
        else:
            colors.append(CHART_COLOR)
    return colors


def get_distribution(word):
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

    return list(counter.keys()), list(counter.values())


def sum_for_seasons_distribution(versions, values):
    seasons_distribution = {}
    for i in range(len(versions)):
        season = '.'.join(versions[i].split('.')[:2])
        if not seasons_distribution.get(season):
            seasons_distribution[season] = 0
        seasons_distribution[season] += values[i]

    return list(seasons_distribution.keys()), list(seasons_distribution.values())


def make_chart(x, y, word, sum_to_seasons=False):

    if sum_to_seasons:
        x, y = sum_for_seasons_distribution(x, y)

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
                label="overall avg", alpha=0.3)
    # average of first versions of seasons
    if not sum_to_seasons:
        plt.axhline(y=nanmean([list(y)[i] for i, k in enumerate(x) if k[-2:] == ".0"]),
                    linestyle="--", color=CHART_COLOR, linewidth=1,
                    label="first patches of seasons avg", alpha=0.3)

    # legend
    legend = plt.legend(loc=(0.85, 0.87), labelcolor=CHART_COLOR, reverse=True, facecolor=BACKGROUND_COLOR, edgecolor=BACKGROUND_COLOR,
               prop=font_legend, numpoints=1)

    # plt.show()

    # Create directory for PNG files if it doesn't exist
    if not os.path.exists(charts_dir_name):
        os.makedirs(charts_dir_name)

    if not sum_to_seasons:
        plt.savefig(f"{charts_dir_name}\\{word}_chart_v.png", dpi=600)
    else:
        plt.savefig(f"{charts_dir_name}\\{word}_chart_s.png", dpi=600)


if __name__ == "__main__":
    w = "fixed"
    make_chart(*get_distribution(word=w), word=w, sum_to_seasons=False)
