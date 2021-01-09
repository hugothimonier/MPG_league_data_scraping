from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from explicit import waiter, XPATH

from urllib.request import Request, urlopen
from urllib.error import HTTPError

from PIL import Image

from bs4 import BeautifulSoup
from sys import exit
import pandas as pd
from numpy import mean

from tqdm import tqdm
from collections import OrderedDict

import sys, argparse, os, time

import MPG_Statistics

width, height = (952,550)
LEFT = width - 70
RIGHT = width - 9
DOTS_LOCATION = [(24,33),(79,88),(134,143),(189,198),(244,253),(299,308),(354,363),(409,418),(464,473),(519,528)]

class MPG_Scrapper():

    def __init__(self, user, pwd, nb_gw, nb_gamers, user_team_name):

        self.user = user
        self.pwd = pwd
        self.nb_gw = nb_gw
        self.nb_gamers = nb_gamers
        self.driver = webdriver.Chrome()
        self.url = 'https://mpg.football/?type=login'
        self.MPG_statistics = MPG_Statistics.MPG_Statistics()
        self.user_team_name = user_team_name
        #self.MPG_image = MPG_Image.MPG_Image()

    def open_page(self, url=None):

        if not url:
            url = self.url
        self.driver.get(url)

        return None

    def connect(self):

        emailElement =  self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/div[2]/div[2]/div/form/div[1]/div/input')
        passwordElement = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/div[2]/div[2]/div/form/div[2]/div/input')

        emailElement.send_keys(self.user)
        passwordElement.send_keys(self.pwd)
        passwordElement.send_keys(Keys.ENTER)

        return None

    def find_league_href(self, name=None):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        league = soup.find_all("a", text=name)
        for val in league:
            href = val.get('href')

        return href

    def find_users(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        teams = soup.find_all("div", class_="index__team___2teXs")
        teams_in_game = []
        for team in teams :
            team = str(team)
            start = team.find('CrD\">') + len('CrD\">')
            end = team.find('</span>')
            team = team[start:end]
            print(team)
            teams_in_game.append(team)

        return teams_in_game

    def get_ranking_from_points(self, points):

        teams = list(points.keys())
        ranking = sorted(teams, key=points.get, reverse=True)

        return ranking

    def find_targetman_idx(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.find_all('div', class_='index__bodyStyle___h4xYl')
        for idx, element in enumerate(elements) :
            if 'index__root___12BYS index__targetManCroped___wTzNy index__padder___2MA83' in str(element):
                return idx

    def generate_img_series(self, series, color='white'):
    
        red = Image.open('./dots/{}/red.png'.format(color))
        green = Image.open('./dots/{}/green.png'.format(color))
        grey = Image.open('./dots/{}/grey.png'.format(color))
        inter = Image.open('./dots/{}/inter.png'.format(color))
        out_image = Image.new('RGB', (61,9))
        last_five = series[-5:]
        x = 0
        for i in range(5):
            if last_five[i]=='V':
                out_image.paste(green, (x,0))
                x += 9
                out_image.paste(inter, (x, 0))
                x += 4
            if last_five[i]=='L':
                out_image.paste(red, (x,0))
                x += 9
                out_image.paste(inter, (x, 0))
                x += 4
            if last_five[i]=='D':
                out_image.paste(grey, (x,0))
                x += 9
                out_image.paste(inter, (x, 0))
                x += 4
    
        return out_image               

    def get_ranking_image(self, points, vic_number, goal_average, draw_number, los_number, series, goal_conceded, goal_scored, league_name=None):

        self.open_page()
        self.driver.implicitly_wait(10)
        self.connect()
        time.sleep(5)

        href = self.find_league_href(name=league_name)
        ranking_url = 'https://mpg.football' + href.replace('wall', 'ranking/detail')

        self.open_page(url=ranking_url)
        self.driver.maximize_window()
        ele = self.driver.find_element_by_tag_name('body')
        total_height = ele.size["height"]+1000


        time.sleep(2)

        self.driver.set_window_size(1920+500, total_height) 
        rankingElement =  self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[2]/div/div/div/div/div/div/div[3]')
        location = rankingElement.location
        size = rankingElement.size

        ranking = self.get_ranking_from_points(points)
        print(ranking)
        target_man = self.find_targetman_idx()

        Team_to_user = dict()
        Team_to_jersey = dict()

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_elements = soup.find_all('div',class_='index__bodyStyle___h4xYl')
        for idx, element in enumerate(all_elements):
            if idx < target_man or idx > target_man :
                team_name_ = element.find('a', attrs={'class':'index__root___12BYS index__playerTitleTextStyle___1r9ga index__padder___2MA83'}).text
                user_cor = element.find('div', attrs={'class':'index__playerSubtitleTextStyle___3N6uc'}).text
                Team_to_user[team_name_] = user_cor

            if idx == target_man:
                team_name_ = element.find('a', attrs={'class':'index__root___12BYS index__targetManCroped___wTzNy index__padder___2MA83'}).text
                user_cor = element.find('div', attrs={'class':'index__playerSubtitleTextStyle___3N6uc'}).text
                Team_to_user[team_name_] = user_cor

        for idx, team_name in enumerate(ranking):
            if idx < target_man :
                self.driver.execute_script("document.getElementsByClassName('index__root___12BYS index__playerTitleTextStyle___1r9ga index__padder___2MA83')[{}].innerHTML = '{}';".format(str(idx), team_name))
                self.driver.execute_script("document.getElementsByClassName('index__playerSubtitleTextStyle___3N6uc')[{}].innerHTML = '{}';".format(str(idx), Team_to_user[team_name]))
                self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textBold___14jFv')[{}].innerHTML = '{}';".format(str(idx), str(points[team_name])))
                time.sleep(1)
            if idx == target_man :
                self.driver.execute_script("document.getElementsByClassName('index__root___12BYS index__targetManCroped___wTzNy index__padder___2MA83')[{}].innerHTML = '{}';".format(str(0), team_name))
                self.driver.execute_script("document.getElementsByClassName('index__playerSubtitleTextStyle___3N6uc')[{}].innerHTML = '{}';".format(str(idx), Team_to_user[team_name]))
                self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textBold___14jFv')[{}].innerHTML = '{}';".format(str(idx), str(points[team_name])))
            if idx > target_man :
                self.driver.execute_script("document.getElementsByClassName('index__root___12BYS index__playerTitleTextStyle___1r9ga index__padder___2MA83')[{}].innerHTML = '{}';".format(str(idx-1), team_name))
                self.driver.execute_script("document.getElementsByClassName('index__playerSubtitleTextStyle___3N6uc')[{}].innerHTML = '{}';".format(str(idx), Team_to_user[team_name]))
                self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textBold___14jFv')[{}].innerHTML = '{}';".format(str(idx), str(points[team_name])))
                time.sleep(1)

            self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textDesign___ZYGit')[{}].innerHTML = '{}';".format(9+7*idx, vic_number[team_name]))
            self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textDesign___ZYGit')[{}].innerHTML = '{}';".format(10+7*idx, draw_number[team_name]))
            self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textDesign___ZYGit')[{}].innerHTML = '{}';".format(11+7*idx, los_number[team_name]))
            self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textDesign___ZYGit')[{}].innerHTML = '{}';".format(12+7*idx, goal_scored[team_name]))
            self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textDesign___ZYGit')[{}].innerHTML = '{}';".format(13+7*idx, goal_conceded[team_name]))
            self.driver.execute_script("document.getElementsByClassName('index__centerColumn___10x1Y index__textDesign___ZYGit')[{}].innerHTML = '{}';".format(14+7*idx, goal_average[team_name]))

        self.driver.save_screenshot("./pageImage.png")

        self.driver.quit()

        x = location['x'];
        y = location['y'];
        width = location['x']+size['width'];
        height = location['y']+size['height'];
        im = Image.open('pageImage.png')
        im2 = im.crop((int(x), int(y), int(width), int(height)))
        im2.save('ranking_before.png')

        grey_location = ranking.index(self.user_team_name)

        for i in range(self.nb_gamers):
            color = 'grey' if i==grey_location else 'white'
            dot_series = self.generate_img_series(series[ranking[i]], color=color)
            im.paste(dot_series, (LEFT,DOTS_LOCATION[i][0]))
        im2.save('ranking_after.png')

    def find_score(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        buts = soup.find_all("div", class_="index__score___300rq animated slideInUp")
        scores = []
        for but in buts :
            but = str(but)
            start = but.find('slideInUp\">') + len('slideInUp\">')
            end = but.find('</')
            print(int(but[start:end]))
            scores.append(int(but[start:end]))

        return scores

    def find_formation(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        formation_home = soup.find_all("div", class_="pitch pitch-horizontal pitch-top")
        formation_away = soup.find_all("div", class_="pitch pitch-horizontal pitch-bottom")
        formations = []
        for formation in formation_home:
            formations.append(formation.get('data-formation'))
        for formation in formation_away:
            formations.append(formation.get('data-formation'))
        print(formations)

        return formations

    def find_bonus(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        bonus_blocs = soup.find_all("div", class_="index__bonusBloc___pae9P")
        bonus_home = []
        bonus_away = []

        if len(bonus_blocs) ==0:
        	return 'No bonus', 'No bonus'

        if len(str(bonus_blocs[0]).split('3C7cm\">')) == 1:
            bonus_home.append('No bonus')
        elif len(str(bonus_blocs[0]).split('3C7cm\">')) == 2:
            bonus_home.append(str(bonus_blocs[0]).split('3C7cm\">')[-1].split('</')[0])
        else :
            bonus_home.append(str(bonus_blocs[0]).split('3C7cm\">')[-2].split('</')[0])
            bonus_home.append(str(bonus_blocs[0]).split('3C7cm\">')[-1].split('</')[0])

        if len(str(bonus_blocs[1]).split('3C7cm\">')) == 1:
            bonus_away.append('No bonus')
        elif len(str(bonus_blocs[1]).split('3C7cm\">')) == 2:
            bonus_away.append(str(bonus_blocs[1]).split('3C7cm\">')[-1].split('</')[0])
        else :
            bonus_away.append(str(bonus_blocs[1]).split('3C7cm\">')[-2].split('</')[0])
            bonus_away.append(str(bonus_blocs[1]).split('3C7cm\">')[-1].split('</')[0])

        if 'Chapron rouge' in bonus_home :
            bonus_home.remove('Chapron rouge')
            chap = bonus_blocs[0].find_all('div', class_='index__bonusNameChapron___247kV')
            player_removed = chap[0].renderContents()
            #start = str(bonus_blocs[0]).find('247kV\"><br>') + len('247kV\"><br>')
            #end = str(bonus_blocs[0]).find('</')
            bonus_home.append(['Chapron rouge', str(player_removed).replace('<br/>','')])

        if 'Chapron rouge' in bonus_away :
            bonus_away.remove('Chapron rouge')
            chap = bonus_blocs[1].find_all('div', class_='index__bonusNameChapron___247kV')
            player_removed = chap[0].renderContents()
            #start = str(bonus_blocs[1]).find('247kV\"><br>') + len('247kV\"><br>')
            #end = str(bonus_blocs[1]).find('</')
            bonus_away.append(['Chapron rouge', str(player_removed).replace('<br/>','')])

        if 'Uber Eats' in bonus_home :
            bonus_home.remove('Uber Eats')
            start = str(bonus_blocs[0]).find('LDtud\"><br/>') + len('LDtud\"><br/>')
            end = str(bonus_blocs[0]).find('</div>')
            bonus_home.append(['Uber Eats', str(bonus_blocs[0])[start:end]])

        if 'Uber Eats' in bonus_away :
            bonus_away.remove('Uber Eats')
            start = str(bonus_blocs[1]).find('LDtud\"><br/>') + len('LDtud\"><br/>')
            end = str(bonus_blocs[1]).find('</div>')
            bonus_away.append(['Uber Eats', str(bonus_blocs[1])[start:end]])

        print(bonus_home, bonus_away)
        if 'Tonton pat\'' in bonus_home:
        	bonus_home = 'Tonton pat'
        if "Tonton pat\'" in bonus_away:
        	bonus_away = 'Tonton pat'
        return bonus_home, bonus_away

    def find_scorer(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        scorers_raw_home = soup.find_all("div", class_="index__scorersHome___1a6V9")
        scorers_raw_away = soup.find_all("div", class_="index__scorersAway___TQBET")

        scorer_list_home = []
        scorer_list_away = []

        for scorer_home in scorers_raw_home:
            for scorer in scorers_raw_home:
                divs = scorer.find_all('div', class_=None)
            for div in divs :
                scorer = div.find_all("span", class_="index__scorer___1gWL9")
                start = str(scorer).find("1gWL9\">") + len("1gWL9\">")
                end = str(scorer).find("</span>")
                number_of_goals = len(div.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6"))
                if 'cancel_keeper_goal' in str(div):
                    scorer = [str(scorer)[start:end].replace(u'\xa0', u''), 'Canceled by keeper']
                elif 'index__ball___39Bld index__mpg___uUgmt index__root___2XTpz jss6' in str(div):
                    scorer = [str(scorer)[start:end].replace(u'\xa0', u''), 'But MPG']
                if type(scorer)!=list:
                    scorer = str(scorer)[start:end].replace(u'\xa0', u'')
                if "index__nanard5M___LDOv1" in scorer :
                	scorer = [scorer.split('<small')[0], 'Canceled by la valise à nanard']
                if number_of_goals > 1 :
                    scorer = [scorer, str(number_of_goals)]
                scorer_list_home.append(scorer)

        for scorer_home in scorers_raw_away:
            for scorer in scorers_raw_away:
                divs = scorer.find_all('div', class_=None)
            for div in divs :
                scorer = div.find_all("span", class_="index__scorer___1gWL9")
                start = str(scorer).find("1gWL9\">") + len("1gWL9\">")
                end = str(scorer).find("</span>")
                number_of_goals = len(div.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6"))
                if 'cancel_keeper_goal' in str(div):
                    scorer = [str(scorer)[start:end].replace(u'\xa0', u''), 'Canceled by keeper']
                if 'index__ball___39Bld index__mpg___uUgmt index__root___2XTpz jss6' in str(div):
                    scorer = [str(scorer)[start:end].replace(u'\xa0', u''), 'But MPG']
                if type(scorer)!=list:
                    scorer = str(scorer)[start:end].replace(u'\xa0', u'')
                if "index__nanard5M___LDOv1" in scorer :
                    scorer = [scorer.split('<small')[0], 'Canceled by la valise à nanard']
                if number_of_goals > 1 :
                    scorer = [scorer, str(number_of_goals)]
                scorer_list_away.append(scorer)
        print(scorer_list_home, scorer_list_away)

        return scorer_list_home, scorer_list_away

    def find_players_grade(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        home_rotaldo = 0
        away_rotaldo = 0

        results_home = soup.find_all('div', class_="index__resultsHome___3FXvp")
        results_away = soup.find_all('div', class_="index__resultsAway___20Ty5")
        players_home = dict()
        players_away = dict()

        for table in results_home:
            table_home = table.find_all('table')
        for table in results_away:
            table_away = table.find_all('table')

        for tab_entry in table_home:
            table_home = tab_entry.find_all('tbody')
        for tab_entry in table_away:
    	    table_away = tab_entry.find_all('tbody')

        for tbody in table_home[1:]:
            details = tbody.find_all('td', class_="index__column___18Jlk index__player___2S1sy index__playerResult___1_qRK")
            if len(details)>1:
                details = details[1]

            start = str(details).find("1_qRK\">") + len("1_qRK\">")
            end = str(details).find("<div class=\"index__root___35Ve6 index__goal___1P2o7\">")
            name = str(details)[start:end]

            if 'index__ball___39Bld index__mpg___uUgmt index__root___2XTpz jss6' in str(details):
                goals = ['1', 'MPG']
            if 'cancel_keeper_goal' in str(details):
                goals = [str(len(tbody.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6"))), 'Canceled by keeper']

            goals = str(len(tbody.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6")))
            if goals == 0 :
            	goals = str(len(tbody.find_all("span", class_="index__ball___39Bld index__mpg___uUgmt index__root___2XTpz jss6")))

            note = tbody.find_all('td', class_="index__rating___3aKs0")[0].renderContents() if len(tbody.find_all('td', class_="index__rating___3aKs0"))==1 else tbody.find_all('td', class_="index__rating___3aKs0")[1].renderContents() 
            bonus = tbody.find_all('td', class_="index__bonus___3iE2K")[0].renderContents() if len(tbody.find_all('td', class_="index__bonus___3iE2K"))==1 else tbody.find_all('td', class_="index__bonus___3iE2K")[1].renderContents()
            if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u")) > 0 :
                final_note = tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u")[0].renderContents() if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u"))==1 else tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u")[1].renderContents()
            if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur")) > 0 :
                final_note = tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur")[0].renderContents() if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur"))==1 else tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur")[1].renderContents()
            if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD")) > 0 :
                final_note = tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD")[0].renderContents() if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD"))==1 else tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD")[1].renderContents()
            
            if final_note == b'':
                final_note = str(float(note) + float(bonus))

            if name == 'Rotaldo':
                home_rotaldo += 1
                name == 'Rotaldo-' + str(home_rotaldo)
            players_home[name] = [goals, note, bonus, final_note]


        for tbody in table_away[1:]:
            details = tbody.find_all('td', class_="index__column___18Jlk index__player___2S1sy index__playerResult___1_qRK")
            if len(details)>1:
                details = details[1]

            start = str(details).find("1_qRK\">") + len("1_qRK\">")
            end = str(details).find("<div class=\"index__root___35Ve6 index__goal___1P2o7\">")
            name = str(details)[start:end]

            if 'index__ball___39Bld index__mpg___uUgmt index__root___2XTpz jss6' in str(details):
                goals = ['1', 'MPG']
            if 'cancel_keeper_goal' in str(details):
                goals = [str(len(tbody.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6"))), 'Canceled by keeper']

            goals = str(len(tbody.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6")))
            note = tbody.find_all('td', class_="index__rating___3aKs0")[0].renderContents() if len(tbody.find_all('td', class_="index__rating___3aKs0"))==1 else tbody.find_all('td', class_="index__rating___3aKs0")[1].renderContents() 
            bonus = tbody.find_all('td', class_="index__bonus___3iE2K")[0].renderContents() if len(tbody.find_all('td', class_="index__bonus___3iE2K"))==1 else tbody.find_all('td', class_="index__bonus___3iE2K")[1].renderContents()
            if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u")) > 0 :
                final_note = tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u")[0].renderContents() if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u"))==1 else tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u")[1].renderContents()
            if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur")) > 0 :
                final_note = tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur")[0].renderContents() if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur"))==1 else tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMax___2iFur")[1].renderContents()
            if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD")) > 0 :
                final_note = tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD")[0].renderContents() if len(tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD"))==1 else tbody.find_all('td', class_="index__column___18Jlk index__final___3Z8fz index__finalResult___1RG2u index__finalMin___15hJD")[1].renderContents()
            
            if final_note == b'':
                final_note = str(float(note) + float(bonus))

            if name == 'Rotaldo':
                away_rotaldo += 1
                name == 'Rotaldo-' + str(away_rotaldo)
            players_away[name] = [goals, note, bonus, final_note]

        return players_home, players_away

    def find_player_grade(self, player_name, formation, home=True):

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        defense = [*range(1, int(formation[0])+1)]
        midfield = [*range(int(formation[0])+1, int(formation[0])+ int(formation[1])+1)]
        attack = [*range(int(formation[0])+int(formation[1])+1, 11)]
        
        if home :
            results = soup.find_all('div', class_="index__resultsHome___3FXvp")
        if not home :
            results = soup.find_all('div', class_="index__resultsAway___20Ty5")

        for table in results:
            table = table.find_all('table')

        for tab_entry in table:
            table = tab_entry.find_all('tbody')

        for tbody in table[1:]:
            details = tbody.find_all('td', class_="index__column___18Jlk index__player___2S1sy index__playerResult___1_qRK")

            for idx, x in enumerate(tbody.find_all('td',class_="index__column___18Jlk index__number___1WoJM")):
            	if idx == 0 :
            	    index_tab = float(x.renderContents()) - 1

            if index_tab in defense :
                position = 'D'
            if index_tab in midfield :
                position = 'M'
            if index_tab in attack :
                position = 'A'

            for idx, detail in enumerate(details):
                if str(player_name) in str(detail):
                    goals = str(len(tbody.find_all("span", class_="index__ball___39Bld index__root___2XTpz jss6")))
                    note = tbody.find_all('td', class_="index__rating___3aKs0")[idx].renderContents()
                    bonus = tbody.find_all('td', class_="index__bonus___3iE2K")[idx].renderContents() 
                    print(note, bonus)
                    final_note = str(float(note) + float(bonus))
                    home = True

                    return [goals, note, bonus, final_note, position]



    def get_league_data(self, league_name=None):

        '''
        retreave league data from name
        @args:
            {str} league_name : name of league to scrap data from
        @returns:
            {pandas.DataFrame} dataframe containing for each row data on several key variables such as :
                              {str} 'team_home' : name of home team 
                              {str} 'team_away' : name of away team 
                              {str} 'GW' : game week 
                              {str} 'score'
                              {str} 'winner' : winner of the game 
                              {int} 'goal home' : number of home goals
                              {int} 'goal away' : number of away goals
                              {str} 'formation home' : home team formation 
                              {str} 'formation away' : away team formation
                              {str} 'bonus home' : bonus chosen by home team 
                              {str} 'bonus away' : bonus chosen by away team
                              {list} 'scorer home' : list of home scorers, 'But MPG' if MPG Goal, if list contains list of player name + int, int represents number of goals
                              {list} 'scorer away' : list of away scorers ...etc
                              {dict} 'player_grades home' : dictionnary with keys home players name and values a list containing (i) number of goals, (ii) rate without bonus, (iii) bonus value and (iv) rate with bonus
                              {dict} 'player_grades away' : dictionnary with keys away players name ... etc
        '''

        columns = ['team_home', 'team_away', 'GW', 'score', 'winner', 'goal home', 'goal away',
        'formation home', 'formation away', 'bonus home', 'bonus away', 'scorer home', 'scorer away',
        'player_grades home', 'player_grades away']
        data_general = pd.DataFrame(columns=columns)

        assert league_name==league_name, 'Name of League cannot be None you donkey'
        self.open_page()
        self.driver.implicitly_wait(10)
        self.connect()
        time.sleep(5)

        href = self.find_league_href(name=league_name)

        league_url = 'https://mpg.football' + href.replace('wall', 'results')

        nb_match = int(self.nb_gamers/2)

        for i in range(1, self.nb_gw+1):
            for j in range(1, nb_match+1):
                print('Journée {}, match {}'.format(i,j))
                match_url = league_url + '/detail/{}_{}_{}'.format(nb_match, i, j)
                self.open_page(url=match_url)
                time.sleep(2)
                users = self.find_users()

                score = self.find_score()
                dif = score[0] - score[1]

                if dif == 0:
                    winner = 'draw'
                if dif > 0 :
                    winner = 'home'
                if dif < 0 :
                    winner = 'away'

                formation = self.find_formation()
                bonus_home, bonus_away = self.find_bonus()
                scorer_home, scorer_away = self.find_scorer()
                player_grades_home, player_grades_away = self.find_players_grade()
                self.add_position(player_grades_home, formation[0])
                self.add_position(player_grades_away, formation[1])
                if any('Chapron rouge' in sublist for sublist in bonus_home):
                    for bonus in bonus_home:
                        if 'Chapron rouge' in bonus :
                            player_name = bonus[1].replace('b\'','')
                            player_name = player_name.replace('\'','')
                    excluded_player_home = self.find_player_grade(player_name, formation[0], home=True)
                    excluded_player_away = self.find_player_grade(player_name, formation[1], home=False)
                    print(excluded_player_home, excluded_player_away)
                    if type(excluded_player_home) is not type(None):
                        excluded_player_home.append('excluded by Chapron Rouge')
                        player_grades_home[player_name] = excluded_player_home
                    if type(excluded_player_away) is not type(None):
                        excluded_player_away.append('excluded by Chapron Rouge')
                        player_grades_away[player_name] = excluded_player_away

                if any('Chapron rouge' in sublist for sublist in bonus_away):
                    for bonus in bonus_away:
                        if 'Chapron rouge' in bonus :
                            player_name = bonus[1].replace('b\'','')
                            player_name = player_name.replace('\'','')
                    excluded_player_home = self.find_player_grade(player_name, formation[0], home=True)
                    excluded_player_away = self.find_player_grade(player_name, formation[1], home=False)
                    print(excluded_player_home, excluded_player_away)
                    if type(excluded_player_home) is not type(None):
                        excluded_player_home.append('excluded by Chapron Rouge')
                        player_grades_home[player_name] = excluded_player_home
                    if type(excluded_player_away) is not type(None):
                        excluded_player_away.append('excluded by Chapron Rouge')
                        player_grades_away[player_name] = excluded_player_away
                time.sleep(5)
                game_data = pd.DataFrame(columns=columns)

                data_general.loc[len(data_general)] = [users[0], users[1], i, score, winner, score[0], score[1], formation[0], formation[1],
                 bonus_home, bonus_away, scorer_home, scorer_away, player_grades_home, player_grades_away] 

        return data_general 


    def add_position(self, player_grades, formation):

        defense = [*range(1, int(formation[0])+1)]
        midfield = [*range(int(formation[0])+1, int(formation[0])+ int(formation[1])+1)]
        attack = [*range(int(formation[0])+int(formation[1])+1, 11)]

        for idx, key in enumerate(player_grades.keys()):
            if idx==0 :
                player_grades.setdefault(key, []).append('G')
            if idx in defense:
                player_grades.setdefault(key, []).append('D')
            if idx in midfield:
                player_grades.setdefault(key, []).append('M')
            if idx in attack:
                player_grades.setdefault(key, []).append('A')

        return None 













    
    