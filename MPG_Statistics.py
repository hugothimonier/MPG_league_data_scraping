import sys, argparse, os, time

from numpy import mean



class MPG_Statistics():


    def __init__(self):
        pass


    def goal_MPG_nobonus(self, position, grade, bonus_player, opponent_player_grades, home=True, att_bonus_def=None, def_bonus_def=None):

        opponent_player_grades_d = []
        opponent_player_grades_m = []
        opponent_player_grades_a = []
        opponent_player_grades_g = 0

        grade = float(grade)

        for key in opponent_player_grades.keys():
            if opponent_player_grades[key][-1]=='G':
               opponent_player_grades_g += float(opponent_player_grades[key][1])
            if opponent_player_grades[key][-1]=='D':
                opponent_player_grades_d.append(float(opponent_player_grades[key][1]))
            if opponent_player_grades[key][-1]=='M':
                opponent_player_grades_m.append(float(opponent_player_grades[key][1]))
            if opponent_player_grades[key][-1]=='A':
                opponent_player_grades_a.append(float(opponent_player_grades[key][1]))

        avg_def = float(mean(opponent_player_grades_d))
        avg_mid = float(mean(opponent_player_grades_m))
        avg_att = float(mean(opponent_player_grades_a))

        if def_bonus_def=='4DEF':
            avg_def += 0.5
        if def_bonus_def=='5DEF':
            avg_def += 1

        if bonus_player < 0:
        	grade += float(bonus_player)

        if position == 'D':
            if att_bonus_def == '4DEF':
                grade += 0.5
            if att_bonus_def == '5DEF':
                grade += 1
            if (grade > avg_att) or (grade == avg_att and home):
                grade -= 1
            else :
                return False

            if (grade > avg_mid) or (grade == avg_mid and home):
                grade -= 0.5
            else :
                return False

            if (grade > avg_def) or (grade == avg_def and home):
                grade -= 0.5
            else :
                return False

            if (grade > opponent_player_grades_g) or (grade == opponent_player_grades_g and home):
                return True
            else:
                return False

        if position == 'M':

            if (grade > avg_mid) or (grade == avg_mid and home):
                grade -= 1
            else :
                return False

            if (grade > avg_def) or (grade == avg_def and home):
                grade -= 0.5
            else :
                return False

            if (grade > opponent_player_grades_g) or (grade == opponent_player_grades_g and home):
                return True
            else:
                return False


        if position == 'A':

            if (grade > avg_def) or (grade == avg_def and home):
                grade -= 1
            else :
                return False

            if (grade > opponent_player_grades_g) or (grade == opponent_player_grades_g and home):
                return True
            else:
                return False


    def goal_MPG_nohomebonus(self, position, grade, opponent_player_grades):

        opponent_player_grades_d = []
        opponent_player_grades_m = []
        opponent_player_grades_a = []
        opponent_player_grades_g = 0

        grade = float(grade)

        for key in opponent_player_grades.keys():
            if opponent_player_grades[key][3]=='G':
               opponent_player_grades_g += float(opponent_player_grades[key][1])
            if opponent_player_grades[key][3]=='D':
                opponent_player_grades_d.append(float(opponent_player_grades[key][1]))
            if opponent_player_grades[key][3]=='M':
                opponent_player_grades_m.append(float(opponent_player_grades[key][1]))
            if opponent_player_grades[key][3]=='A':
                opponent_player_grades_a.append(float(opponent_player_grades[key][1]))

        avg_def = float(mean(opponent_player_grades_d))
        avg_mid = float(mean(opponent_player_grades_m))
        avg_att = float(mean(opponent_player_grades_a))

        if position == 'D':
            if (grade > avg_att) :
                grade -= 1
            else :
                return False

            if (grade > avg_mid) :
                grade -= 0.5
            else :
                return False

            if (grade > avg_def) :
                grade -= 0.5
            else :
                return False

            if (grade > opponent_player_grades_g) :
                return True
            else:
                return False

        if position == 'M':

            if (grade > avg_mid) :
                grade -= 1
            else :
                return False

            if (grade > avg_def) or (grade == avg_def and home):
                grade -= 0.5
            else :
                return False

            if (grade > opponent_player_grades_g):
                return True
            else:
                return False


        if position == 'A':

            if (grade > avg_def) :
                grade -= 1
            else :
                return False

            if (grade > opponent_player_grades_g) :
                return True
            else:
                return False

    def rebuilt_team_wo_redchp(self, rates, formation):

        defense = [*range(1, int(formation[0])+1)]
        midfield = [*range(int(formation[0])+1, int(formation[0])+ int(formation[1])+1)]
        attack = [*range(int(formation[0])+int(formation[1])+1, 11)]
        to_del = None 
        for player in rates.keys() :
            if 'excluded by Chapron Rouge' in rates[player]:
                position = rates[player][-2]
                if position == 'D':
                    for idx, player in enumerate(rates.keys()):
                        if (idx in defense) and ('Rotaldo' in player):
                            to_del = player
                            break
                if position == 'M':
                    for idx, player in enumerate(rates.keys()):
                        if (idx in midfield) and ('Rotaldo' in player):
                            to_del = player
                            break
                if position == 'A':
                    for idx, player in enumerate(rates.keys()):
                        if (idx in attack) and ('Rotaldo' in player):
                            to_del = player
                            break
        if type(to_del) != type(None):
            del rates[to_del]
        return None


    def recompute_game_score_nobonus(self, home_rates, away_rates, home_goal, away_goal, home_bonus, away_bonus,
        home_formation, away_formation):
        '''
        recompute the score of a game without the bonus (except tonton pat)
        @args:
            {dict} home_rates : rates of home team
            {dict} away_rates : rates of away team 
            {list} home_goal : list of home scorers
            {list} away_rates : list of away scorers 
            {str} home_bonus : home bonus
            {str} away_bonus : away bonus
            {int} home_rotaldo : number of home rotaldo
            {int} away_rotaldo : number of away rotaldo
            {str} formation : composition of team
        @returns:
            {list}, {list} goal scorers and score
        '''

        if 'La valise à nanard' in home_bonus :
            for idx, scorer in enumerate(away_goal) :
                if 'Canceled by la valise à nanard' in scorer :
                    scorer = [el for el in scorer if el != 'Canceled by la valise à nanard']
                    away_goal[idx] = scorer

        if 'La valise à nanard' in away_bonus :
            for idx, scorer in enumerate(home_goal) :
                if 'Canceled by la valise à nanard' in scorer :
                    scorer = [el for el in scorer if el != 'Canceled by la valise à nanard']
                    home_goal[idx] = scorer

        if any('Chapron rouge' in sublist for sublist in home_bonus) or any('Chapron rouge' in sublist for sublist in away_bonus):
            self.rebuilt_team_wo_redchp(home_rates, home_formation)
            self.rebuilt_team_wo_redchp(away_rates, away_formation)
        
        home_goal_wo_MPG = [goal for goal in home_goal if 'But MPG' not in goal]
        away_goal_wo_MPG = [goal for goal in away_goal if 'But MPG' not in goal]

        home_def_bonus = None
        away_def_bonus = None
        for i in range(len(home_bonus)):
            if ('4DEF' == home_bonus[i]) or ('5DEF' == home_bonus[i]):
                home_def_bonus = home_bonus[i]
        for i in range(len(away_bonus)):
            if ('4DEF' == away_bonus[i]) or ('5DEF' == away_bonus[i]):
                away_def_bonus = away_bonus[i]
        
        for player in home_rates.keys():
            if home_rates[player][-1]!='G':
                mpg_goal = self.goal_MPG_nohomebonus(position=home_rates[player][-1], grade=float(home_rates[player][1]), bonus_player=float(home_rates[player][2]),
                 opponent_player_grades=away_rates, att_bonus_def=home_def_bonus, def_bonus_def=away_def_bonus)
                if mpg_goal and int(home_rates[player][0])==0:
                    home_goal_wo_MPG.append([player, 'MPG no bonus'])
                if 'excluded by Chapron Rouge' in home_rates[player]:
                    if int(home_rates[player][0])>0:
                        home_goal_wo_MPG.append([player, 'un-excluded goal'])

        for player in away_rates.keys():
            if away_rates[player][-1]!='G':
                mpg_goal = self.goal_MPG_nohomebonus(position=away_rates[player][-1], grade=away_rates[player][1], bonus_player=float(away_rates[player][2]),
                 opponent_player_grades=home_rates, home=False, att_bonus_def=away_def_bonus, def_bonus_def=home_def_bonus)
                if mpg_goal and int(away_rates[player][0])==0:
                    away_goal_wo_MPG.append([player, 'MPG no bonus'])
                if 'excluded by Chapron Rouge' in away_rates[player]:
                    if int(away_rates[player][0])>0:
                        away_goal_wo_MPG.append([player, 'un-excluded goal'])

        return home_goal_wo_MPG, away_goal_wo_MPG

    def recompute_game_score_nohomebonus(self, home_rates, away_rates, home_goal, away_goal, home_bonus, away_bonus,
        home_formation, away_formation):
        '''
        recompute the score of a game without the bonus (except tonton pat)
        @args:
            {dict} home_rates : rates of home team
            {dict} away_rates : rates of away team 
            {list} home_goal : list of home scorers
            {list} away_rates : list of away scorers 
            {str} home_bonus : home bonus
            {str} away_bonus : away bonus
            {int} home_rotaldo : number of home rotaldo
            {int} away_rotaldo : number of away rotaldo
            {str} formation : composition of team
        @returns:
            {list}, {list} goal scorers and score
        '''
        
        #remove MPG Goals, will be replaced by recomputed MPG goals without home bonus
        home_goal_wo_MPG = [goal for goal in home_goal if 'But MPG' not in goal]
        away_goal_wo_MPG = [goal for goal in away_goal if 'But MPG' not in goal]
        
        for player in home_rates.keys():
            if home_rates[player][-1]!='G':
                mpg_goal = self.goal_MPG_nohomebonus(position=home_rates[player][-1], grade=float(home_rates[player][1]), opponent_player_grades=away_rates)
                if mpg_goal and int(home_rates[player][0])==0:
                    home_goal_wo_MPG.append([player, 'MPG no bonus'])

        for player in away_rates.keys():
            if away_rates[player][-1]!='G':
                mpg_goal = self.goal_MPG_nohomebonus(position=away_rates[player][-1], grade=away_rates[player][1], opponent_player_grades=home_rates)
                if mpg_goal and int(away_rates[player][0])==0:
                    away_goal_wo_MPG.append([player, 'MPG no bonus'])

        return home_goal_wo_MPG, away_goal_wo_MPG


    def ranking_wo_bonus(self, dataframe, no_bonus='all'):
        '''
        returns ranking without MPG bonus except for Tonton Pat since we do not dispose of bench ranking
        @args :
            {pandas.DataFrame} dataframe : data in the form of the one scrapped
            {str} no_bonus : whether to remove all bonus, or only home bonus
        @returns :
            {dict, OrderedDict} game results, league ranking
        '''

        assert no_bonus == 'all' or no_bonus=='home bonus'

        points = dict()
        goal_average = dict()
        vic_number = dict()
        los_number = dict()
        draw_number = dict()
        game_scores = dict()
        series = dict()
        goal_scored = dict()
        goal_conceded = dict()
        teams = list(dataframe['team_home'].unique())
        
        for team in teams:
            points[team] = 0
            goal_average[team] = 0
            vic_number[team] = 0
            los_number[team] = 0
            draw_number[team] = 0
            series[team] = []
            goal_scored[team] = 0
            goal_conceded[team] = 0

        for i in range(len(dataframe)):

            home_team_name = dataframe['team_home'][i]
            away_team_name = dataframe['team_away'][i]

            home_goal = dataframe['scorer home'][i]
            away_goal = dataframe['scorer away'][i]

            bonus_home = dataframe['bonus home'][i]
            bonus_away = dataframe['bonus away'][i]

            home_grades = dataframe['player_grades home'][i]
            away_grades = dataframe['player_grades away'][i]

            home_composition = dataframe['formation home'][i]
            away_composition = dataframe['formation away'][i]

            if no_bonus=='all':

                home_scorers_nobonus, away_scorers_nobonus = self.recompute_game_score_nobonus(home_rates=home_grades, away_rates=away_grades,
                                                                                           home_goal=home_goal, away_goal=away_goal,
                                                                                           home_bonus=bonus_home, away_bonus=bonus_away,
                                                                                           home_formation=home_composition, away_formation=away_composition)

            if no_bonus=='home bonus':

            	home_scorers_nobonus, away_scorers_nobonus = self.recompute_game_score_nohomebonus(home_rates=home_grades, away_rates=away_grades,
                                                                                           home_goal=home_goal, away_goal=away_goal,
                                                                                           home_bonus=bonus_home, away_bonus=bonus_away,
                                                                                           home_formation=home_composition, away_formation=away_composition)


            number_of_home_goals = 0
            number_of_away_goals = 0

            for scorer in home_scorers_nobonus:
                if type(scorer)==str:
                    number_of_home_goals += 1
                if (len(scorer)==2) and (scorer[-1] == 'Canceled by la valise à nanard'):
                	continue
                if (len(scorer)==2) and ('Canceled by la valise à nanard' in scorer):
                    if 'Canceled by la valise à nanard' in scorer[0]:
                        number_of_away_goals += int(scorer[-1]) - 1
                if (len(scorer)==2) and (scorer[-1] == 'MPG no bonus'):
                    number_of_home_goals += 1
                if (len(scorer)==2) and (('Canceled by keeper' not in scorer) and (scorer[-1] != 'MPG no bonus') and ('Canceled by la valise à nanard' not in scorer)):
                    number_of_home_goals += int(scorer[-1])
                if (len(scorer)==2) and ('Canceled by keeper' in scorer):
                    if 'Canceled by keeper' in scorer[0]:
                        number_of_home_goals += int(scorer[-1]) - 1


            for scorer in away_scorers_nobonus:
                if type(scorer)==str:
                    number_of_away_goals += 1
                if (len(scorer)==2) and (scorer[-1] == 'MPG no bonus'):
                	number_of_away_goals += 1
                if (len(scorer)==2) and (scorer[-1] == 'Canceled by la valise à nanard'):
                	continue
                if (len(scorer)==2) and ('Canceled by la valise à nanard' in scorer):
                    if 'Canceled by la valise à nanard' in scorer[0]:
                        number_of_away_goals += int(scorer[-1]) - 1
                if (len(scorer)==2) and (('Canceled by keeper' not in scorer) and (scorer[-1] != 'MPG no bonus') and ('Canceled by la valise à nanard' not in scorer)):
                    number_of_away_goals += int(scorer[-1])
                if (len(scorer)==2) and ('Canceled by keeper' in scorer):
                    if 'Canceled by keeper' in scorer[0]:
                        number_of_away_goals += int(scorer[-1]) - 1

            home_points = 0
            away_points = 0
            goal_dif = number_of_home_goals - number_of_away_goals
            goal_scored[home_team_name] += number_of_home_goals
            goal_scored[away_team_name] += number_of_away_goals
            goal_conceded[home_team_name] += number_of_away_goals
            goal_conceded[away_team_name] += number_of_home_goals

            if goal_dif > 0 :
                home_points += 3
                vic_number[home_team_name] += 1
                los_number[away_team_name] += 1
                #goal_average[home_team_name] += goal_dif
                #goal_average[away_team_name] -= goal_dif
                series[home_team_name].append('V')
                series[away_team_name].append('L')

            if goal_dif == 0 :
                home_points += 1
                away_points += 1
                draw_number[home_team_name] += 1
                draw_number[away_team_name] += 1
                series[home_team_name].append('D')
                series[away_team_name].append('D')

            if goal_dif < 0 :
                away_points += 3
                vic_number[away_team_name] += 1
                los_number[home_team_name] += 1
                #goal_average[home_team_name] -= goal_dif
                #goal_average[away_team_name] += goal_dif
                series[home_team_name].append('L')
                series[away_team_name].append('V')


            game_scores[home_team_name + ' - ' + away_team_name] = [number_of_home_goals,number_of_away_goals]
            points[home_team_name] += home_points
            points[away_team_name] += away_points 

        for team in teams :
        	goal_average[team] = goal_scored[team] - goal_conceded[team]

        return game_scores, points, goal_average, vic_number, draw_number, los_number, series, goal_conceded, goal_scored


   # def player_goal_number(self, dataframe):


    def MPG_goalscorer_avg_rate(self, dataframe, return_all=False, return_figure=False):
        '''
        Get average rate of MPG goal scorer per team
        @args :
            {pandas.DataFrame} dataframe : dataframe with column names corresponding to the ones obtained after using get_league_data
        @returns :
            {dict} keys Team Name, values mean mpg rate for MPG scorer and number of MPG goals
                 if return_all :
                 	two supplementary dictionnary differenciating home and away MPG goals
        '''

        user_list_mpg_home = dict()
        user_list_mpg_away = dict()
        user_list_mpg = dict()
        for user in data['team_home'].unique():
            mpg_scorer_rates_home = []
            mpg_scorer_rates_away = []
            for idx in list(data[data['team_home']==user].index.values):
                if len(data[data['team_home']==user].loc[idx]['scorer home'])>0:
                    for scorer in data.loc[idx]['scorer home']:
                        if type(scorer) == list :
                            if 'But MPG' in scorer :
                                mpg_scorer_rates_home.append(data[data['team_home']==user].loc[idx]['player_grades home'][scorer[0]])
            for idx in list(data[data['team_away']==user].index.values):
                if len(data[data['team_away']==user].loc[idx]['scorer away'])>0:
                    for scorer in data[data['team_away']==user].loc[idx]['scorer away']:
                        if type(scorer) == list :
                            if 'But MPG' in scorer :
                                mpg_scorer_rates_away.append(data[data['team_away']==user].loc[idx]['player_grades away'][scorer[0]])
            user_list_mpg_home[user] = mpg_scorer_rates_home
            user_list_mpg_away[user] = mpg_scorer_rates_away
            user_list_mpg[user] = mpg_scorer_rates_home + mpg_scorer_rates_away

            for element in mpg_scorer_rates_home :
                for j in range(len(element)-1):
                    if element[j] == b'':
                        element[j] = element[1]
                    element[j] = float(element[j])
            for element in mpg_scorer_rates_away :
                for j in range(len(element)-1):
                    if element[j] == b'':
                        element[j] = element[1]
                    element[j] = float(element[j])
        user_mpg_means = dict()
        user_mpg_means_home = dict()
        user_mpg_means_away = dict()
        for user in user_list_mpg.keys():
            mean_mpg = np.mean([el[:-1] for el in user_list_mpg[user]], axis=0)
            mean_mpg_home = np.mean([el[:-1] for el in user_list_mpg_home[user]], axis=0)
            mean_mpg_away = np.mean([el[:-1] for el in user_list_mpg_away[user]], axis=0)
            user_mpg_means[user] = [mean_mpg, len(user_list_mpg[user])]
            user_mpg_means_home[user] = [mean_mpg_home, len(user_list_mpg_home[user])]
            user_mpg_means_home[user] = [mean_mpg_away, len(user_list_mpg_away[user])]

        if not return_all:
            return user_mpg_means
        else :
	        return user_mpg_means, user_mpg_means_home, user_mpg_means_home


    def avg_def_rate_MPGgoal(self, dataframe):


        user_list_mpg_home = dict()
        user_list_mpg_away = dict()
        user_list_mpg = dict()
        for user in data['team_home'].unique():
            mpg_DEF_rates_home = []
            mpg_DEF_rates_away = []
            for idx in list(data[data['team_home']==user].index.values):
                if len(data[data['team_home']==user].loc[idx]['scorer home'])>0:
                    for scorer in data.loc[idx]['scorer home']:
                        if type(scorer) == list :
                            if 'But MPG' in scorer :
                                def_game = list()
                                for player in data[data['team_home']==user].loc[idx]['player_grades away'].keys():
                                    if data[data['team_home']==user].loc[idx]['player_grades away'][player][-1]=='D':
                                        def_game.append(data[data['team_home']==user].loc[idx]['player_grades away'][player]) 
                                mpg_DEF_rates_home.append(def_game)
            for idx in list(data[data['team_away']==user].index.values):
                if len(data[data['team_away']==user].loc[idx]['scorer away'])>0:
                    for scorer in data[data['team_away']==user].loc[idx]['scorer away']:
                        if type(scorer) == list :
                            if 'But MPG' in scorer :
                                def_game = []
                                for player in data[data['team_away']==user].loc[idx]['player_grades home'].keys():
                                    if data[data['team_away']==user].loc[idx]['player_grades home'][player][-1]=='D':
                                        def_game.append(data[data['team_away']==user].loc[idx]['player_grades home'][player])
                                mpg_DEF_rates_away.append(def_game)
            user_list_mpg_home[user] = mpg_DEF_rates_home
            user_list_mpg_away[user] = mpg_DEF_rates_away
            user_list_mpg[user] = mpg_DEF_rates_home + mpg_DEF_rates_away


        new_user_list = dict()
        mean_user_list = dict()
        for user in user_list_mpg.keys():
            user_list_new = []
            mean_user_list_new = []
            for defense in user_list_mpg[user]:
                new_def = []
                for el in defense :
                    new_el = []
                    for x in el[:-1]:
                        if x == b'':
                            x = el[1]
                        new_el.append(float(x))
                    new_def.append(new_el)
                mean_new_def = np.mean(new_def, axis=0)
                mean_user_list_new.append(mean_new_def[-1])
                user_list_new.append(new_def)
            mean_user_list[user] = mean_user_list_new
            new_user_list[user] = user_list_new

        avg_mean_def_user = dict()
        for user in mean_user_list.keys():
            avg_mean_def_user[user] = np.mean(mean_user_list[user])

        return avg_mean_def_user


    def avg_def_rate(self, dataframe, return_per_composition=False):

        user_list_def_global = dict()
        user_list_def_global_3 = dict()
        user_list_def_global_4 = dict()
        user_list_def_global_5 = dict()
        for user in data['team_home'].unique():
            mpg_DEF_rates_home = []
            mpg_DEF_rates_home_3 = []
            mpg_DEF_rates_home_4 = []
            mpg_DEF_rates_home_5 = []
            mpg_DEF_rates_away = []
            mpg_DEF_rates_away_3 = []
            mpg_DEF_rates_away_4 = []
            mpg_DEF_rates_away_5 = []
            for idx in list(data[data['team_home']==user].index.values):
                def_game = list()
                for player in data[data['team_home']==user].loc[idx]['player_grades away'].keys():
                    if data[data['team_home']==user].loc[idx]['player_grades away'][player][-1]=='D':
                        def_game.append(data[data['team_home']==user].loc[idx]['player_grades away'][player])
                mpg_DEF_rates_home.append(def_game)
                if len(def_game)==3:
                    mpg_DEF_rates_home_3.append(def_game)
                if len(def_game)==4:
                    mpg_DEF_rates_home_4.append(def_game)
                if len(def_game)==5:
                    mpg_DEF_rates_home_5.append(def_game)
            for idx in list(data[data['team_away']==user].index.values):
                def_game = []
                for player in data[data['team_away']==user].loc[idx]['player_grades home'].keys():
                    if data[data['team_away']==user].loc[idx]['player_grades home'][player][-1]=='D':
                        def_game.append(data[data['team_away']==user].loc[idx]['player_grades home'][player])
                mpg_DEF_rates_away.append(def_game)
                if len(def_game)==3:
                    mpg_DEF_rates_away_3.append(def_game)
                if len(def_game)==4:
                    mpg_DEF_rates_away_4.append(def_game)
                if len(def_game)==5:
                    mpg_DEF_rates_away_5.append(def_game)
            user_list_def_global[user] = mpg_DEF_rates_home + mpg_DEF_rates_away
            user_list_def_global_3[user] = mpg_DEF_rates_home_3 + mpg_DEF_rates_away_3
            user_list_def_global_4[user] = mpg_DEF_rates_home_4 + mpg_DEF_rates_away_4
            user_list_def_global_5[user] = mpg_DEF_rates_home_5 + mpg_DEF_rates_away_5

        new_user_list_def_global = dict()
        mean_user_list_def_global = dict()
        for user in user_list_mpg.keys():
            user_list_new = []
            mean_user_list_new = []
            for defense in user_list_def_global[user]:
                new_def = []
                for el in defense :
                    new_el = []
                    for x in el[:-1]:
                        if x == b'':
                            x = el[1]
                        new_el.append(float(x))
                    new_def.append(new_el)
                mean_new_def = np.mean(new_def, axis=0)
                mean_user_list_new.append(mean_new_def[-1])
                user_list_new.append(new_def)
            mean_user_list_def_global[user] = mean_user_list_new
            new_user_list_def_global[user] = user_list_new    
        avg_mean_def_user_all_game = dict()
        for user in mean_user_list.keys():
            avg_mean_def_user_all_game[user] = np.mean(mean_user_list_def_global[user]) 


        if return_per_composition:
        	## 3DEF
            new_user_list_def_global_3 = dict()
            mean_user_list_def_global_3 = dict()
            for user in user_list_mpg.keys():
                user_list_new = []
                mean_user_list_new = []
                for defense in user_list_def_global_3[user]:
                    new_def = []
                    for el in defense :
                        new_el = []
                        for x in el[:-1]:
                            if x == b'':
                                x = el[1]
                            new_el.append(float(x))
                        new_def.append(new_el)
                    mean_new_def = np.mean(new_def, axis=0)
                    mean_user_list_new.append(mean_new_def[-1])
                    user_list_new.append(new_def)
                mean_user_list_def_global_3[user] = mean_user_list_new
                new_user_list_def_global_3[user] = user_list_new  
            avg_mean_def_user_all_game_3 = dict()
            for user in mean_user_list.keys():
                avg_mean_def_user_all_game_3[user] = np.mean(mean_user_list_def_global_3[user])

            ## 4DEF
            new_user_list_def_global_4 = dict()
            mean_user_list_def_global_4 = dict()
            for user in user_list_mpg.keys():
                user_list_new = []
                mean_user_list_new = []
                for defense in user_list_def_global_4[user]:
                    new_def = []
                    for el in defense :
                        new_el = []
                        for x in el[:-1]:
                            if x == b'':
                                x = el[1]
                            new_el.append(float(x))
                        new_def.append(new_el)
                    mean_new_def = np.mean(new_def, axis=0)
                    mean_user_list_new.append(mean_new_def[-1])
                    user_list_new.append(new_def)
                mean_user_list_def_global_4[user] = mean_user_list_new
                new_user_list_def_global_4[user] = user_list_new  
            avg_mean_def_user_all_game_4 = dict()
            for user in mean_user_list.keys():
                avg_mean_def_user_all_game_4[user] = np.mean(mean_user_list_def_global_4[user])


            ## 5DEF
            new_user_list_def_global_5 = dict()
            mean_user_list_def_global_5 = dict()
            for user in user_list_mpg.keys():
                user_list_new = []
                mean_user_list_new = []
                for defense in user_list_def_global_5[user]:
                    new_def = []
                    for el in defense :
                        new_el = []
                        for x in el[:-1]:
                            if x == b'':
                                x = el[1]
                            new_el.append(float(x))
                        new_def.append(new_el)
                    mean_new_def = np.mean(new_def, axis=0)
                    mean_user_list_new.append(mean_new_def[-1])
                    user_list_new.append(new_def)
                mean_user_list_def_global_5[user] = mean_user_list_new
                new_user_list_def_global_5[user] = user_list_new  
            avg_mean_def_user_all_game_5 = dict()
            for user in mean_user_list.keys():
                avg_mean_def_user_all_game_5[user] = np.mean(mean_user_list_def_global_5[user])

            return avg_mean_def_user_all_game, avg_mean_def_user_all_game_3, avg_mean_def_user_all_game_4, avg_mean_def_user_all_game_5
        else:
            return avg_mean_def_user_all_game
