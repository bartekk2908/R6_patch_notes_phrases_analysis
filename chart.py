from matplotlib import pyplot as plt
import json
from counter import FILE_NAME
from numpy import nanmean


BACKGROUND_COLOR = '#202343'
CHART_COLOR = 'white'

font_title = {'family': 'serif',
              'color':  CHART_COLOR,
              'weight': 'bold',
              'size': 28,
              }

font_labels = {'family': 'serif',
               'color':  CHART_COLOR,
               'weight': 'bold',
               'size': 11,
               }

font_legend = {'family': 'serif',
               'weight': 'bold',
               'size': 8,
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

    # background
    plt.figure(facecolor=BACKGROUND_COLOR)
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
    plt.title("Number of \"FIX\" phrase in R6 patch notes", fontdict=font_title)
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

    plt.show()
