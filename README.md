## Scrapping data from your MPG League 

This repo allows you to scrape data from a league in which you participate.

### Clone repo

```bash
$ git clone https://github.com/hugothimonier/MPG_league_data_scrapping.git
$ cd MPG_league_data_scrapping/
```

## Requirements

#### set environment

```bash
$ conda create --name mpgscrap
$ conda activate mpgscrap
$ pip3 install -r requirements.txt
```
#### Chromedriver

One must also install Chromedriver. (https://chromedriver.chromium.org/). Note that for Chromedriver to operate, one needs Google Chrome to be installed.

For MacOS it is available via ``brew`` through the following command :
```bash
$ brew install chromedrive
```

### Usage

To scrape data of league named 'MPG League', and save it as a json file: 

```bash
$ cd MPG_league_data_scrapping/
$ python scrape.py -user '*YOUR_USERNAME*' -pwd '*YOUR_PASSWORD*' -nb_gw *NUMBER_OF_GAMES_PLAYED* -nb_teams *NUMBER_OF_TEAMS_IN_LEAGUE* -nb_seasons *NB_OF_SEASONS_PLAYED* -team_name '*YOUR_TEAM_NAME*' -league_name '*LEAGUE_NAME*' -json_file '*JSON_FILE_NAME*'
```

### Main functions

Other functionalities are available, among which :

#### Compute league's ranking without bonus :

```python
out = mpg_scraper.MPG_statistics.ranking_wo_bonus(dataframe=data)
```
#### Compute league's ranking without home bonus :

```python
out = mpg_scraper.MPG_statistics.ranking_wo_bonus(dataframe=data, no_bonus="home bonus")
```
#### Get image ranking based on recomputed ranking :

```python
mpg_scraper.get_ranking_image(points, win_number, draw_number, los_number, series, goal_average, goal_conceded, goal_scored, league_name="MPG League", out_img_name="new_ranking")
```
#### Example of such generated image :

##### Original ranking 
<p align="center">
  <img src="https://github.com/hugothimonier/MPG_league_data_scrapping/blob/master/example_imgs/ranking_before.png" alt="Original Ranking" height = '100%' width ='100%' /> 
</p>

##### Recomputed ranking 

<p align="center">
<img src="https://github.com/hugothimonier/MPG_league_data_scrapping/blob/master/example_imgs/ranking_after.png" alt="Recomputed Ranking" height = '100%' width ='100%' />
  </p>
