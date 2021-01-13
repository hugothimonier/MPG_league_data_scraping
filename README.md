## Scrapping data from your MPG League 

This repo allows you to scrape data from a league in which you participate.

### Clone repo

```bash
$ git clone https://github.com/hugothimonier/MPG_league_data_scrapping.git
$ cd MPG_league_data_scrapping/
```

### Requirements

```bash
$ conda create --name mpgscrap
$ conda activate mpgscrap
$ conda install --force-reinstall -y -q --name py37 -c conda-forge --file requirements.txt
```
### Usage

To scrape data of league named '©':

```python
mpg_scraper = MPG_Scrapper.MpgScrapper(user=*username*, pwd=*password*, nb_gw=18, nb_gamers=10, nb_seasons_played=1, user_team_name=*your team name*)
data = mpg_scrapper.get_league_data(league_name='MPG league')
```

### Main functions

#### Compute league's ranking without bonus :

```python
game_scores, points, goal_average, vic_number, draw_number, los_number, series, goal_conceded, goal_scored = mpg_scrapper.MPG_statistics.ranking_wo_bonus(dataframe=data)
```
#### Compute league's ranking without home bonus :

```python
game_scores, points, goal_average, vic_number, draw_number, los_number, series, goal_conceded, goal_scored = mpg_scrapper.MPG_statistics.ranking_wo_bonus(dataframe=data, no_bonus='home bonus')
```
#### Get image ranking based on recomputed ranking :

```python
mpg_scrapper.get_ranking_image(points, vic_number, draw_number, los_number, series, goal_average, goal_conceded, goal_scored, league_name='League Name', out_img_name='new_ranking')
```
#### Example of such generated image :

##### Original ranking 
<p align="center">
  <img src="https://github.com/hugothimonier/MPG_league_data_scrapping/blob/master/ranking.png" alt="Original Ranking" height = '100%' width ='100%' /> 
</p>

##### Recomputed ranking 

<p align="center">
<img src="https://github.com/hugothimonier/MPG_league_data_scrapping/blob/master/ranking_after.png" alt="Recomputed Ranking" height = '100%' width ='100%' />
  </p>
