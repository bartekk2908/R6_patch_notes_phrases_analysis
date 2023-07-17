# Analysis of specified phrases at Rainbow Six: Siege patch notes pages


## Description

The project is about visualizing distribution of specified phrases
at every Rainbow Six: Siege patch notes page.

The idea comes from Rainbow Six: Siege being famous for having a lot of issues and bugs so I was curious how many fixes are being made every update. 

The data of webpages was scrapped with Python's [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) module
and is stored in `webpages_content.json` file.
Urls have been collected manually from [Ubisoft's page](https://www.ubisoft.com/)
and are stored in `urls.txt` file as ''version_number url'' pairs. 
Unfortunately I wasn't able to find patch notes pages for first two years of game
so the first version is __3.1.1__.

The charts are made with Python's [MatPlotLib](https://matplotlib.org/) module.
Colors that represent each season are specified in `colors.txt` file as ''version_number color'' pairs.

Version number format is following: [year].[season_of_year].[number_of_patch_in_season]


## Example

Last version in example: __8.2.3__

Chart for every version of game:

![fix_chart_v](./charts/fixed_chart_v.png)

Chart for every season of game:

![fix_chart_s](./charts/fixed_chart_s.png)

For more examples see `charts` directory.


## Usage

### Setup

To use it clone this repository via `git clone <url_of_this_repo>` command in Git Bash
and create virtual environment in directory of cloned repo.\
Then install packages specified in `requirements.txt` file.


### Getting distribution

Run `counter.py` file to get distribution of given phrase.\
You can specify phrase by changing value of `word` argument.\
You can also decide to download again entire content of webpages
by changing `saved_webpages_content` argument to __False__ (scrapping should take about 2-3 minutes).\
If in `urls.txt` file there is specified version of game that hasn't been scrapped yet,
it will be scrapped automatically.\
Distributions will be saved in `distributions` directory as `.json` files.


### Creating chart

Run `chart.py` file to generate chart of distribution of given phrase.\
You can specify phrase by changing value of `word` argument.\
You can decide if you want to generate chart of distribution for every version or for every season
by changing `sum_to_seasons` argument's value.\
Charts will be saved in `charts` directory as `.png` files.
