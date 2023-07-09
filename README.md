# Analysis of specified phrases at ''Rainbow Six: Siege'' patch notes pages


## Description

The project is about visualizing distribution of specified phrases
at every ''Rainbow Six: Siege'' patch notes page.

The data of webpages was scrapped with Python's BeautifulSoup4 module
and is stored in `webpages_content.json` file.

Urls have been collected manually from Ubisoft's page
and are stored in `urls.txt` file as ''version_number url'' pairs. 

Colors for each season are specified in `colors.txt` file as ''version_number color'' pairs.


## Example

Last version in example: __8.2.2__

Chart for every version of game:

![fix_chart_v](./charts/fixed_chart_v.png)

Chart for every season of game:

![fix_chart_s](./charts/fixed_chart_s.png)

For more examples see `charts` directory.


## Usage

### Setup

To use it clone this repository via `git clone <url_of_this_repo>` command in Git Bash
and create virtual environment in its directory. Then install packages specified in `requirements.txt` file.


### Getting distribution

Run `counter.py` file to get distribution of given phrase.
You can specify phrase by changing value of `word` argument.
You can also decide to download again entire content of webpages
by changing `saved_webpages_content` argument to False.


### Creating chart




### Updating distributions and charts


