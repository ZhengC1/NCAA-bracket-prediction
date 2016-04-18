
import copy
import itertools
import numpy as np
import json
import sys
display_keys = ["pts","shooting", "dreb", "ast", "stl", "blk","def_ef", "off_ef","oreb" ] #["freethrow","shooting", "dreb", "ast", "stl", "oreb", "to", "reb",  "pts", "blk", "pf", ]   #["pts","shooting", "ast", "stl", "blk","def_ef", "off_ef", ]
teams = {}
inv_teams = {}
stat_mod = {}
inv_stat_mod = {}
max_base = 10
start = 0
test_set = 0

	
    # creates a dictionary of the teams from data
def get_teams(data):
	for game in data:
		teams.setdefault(game['home']['team'], len(teams))
	inv_teams = {v: k for k, v in teams.items()}
	


def main(args):

	files = ["2013.json","2014.json","2015.json"]

	first = True
	sucessful_mods = []
	for file in files:
		test_games = []
		temp_success = []
    # opens file, loads data from games
	

	
		with open(file) as data_file:
			games = json.load(data_file)
	#games,games_test = model(data)
	
		get_teams(games)
		# creates the m matrix(games * teams)
		m = {}
		r = {}
		y = {}
		num_y = {}   
		num_m = {}
		for key in display_keys:
			y[key] = []
			r[key] = []
			m[key] = []
		
		equation = {}
		max_games = len(games)
		
		for i,game in enumerate(games[0:(len(games)-test_set)]):
			
			if game['notes']:
				if "MEN'S BASKETBALL" in game['notes']:
					test_games.append(game) 
					continue
			
			
			error = False
			row = [0] * len(teams)
			row[teams[game['home']['team']]] = 1
			row[teams[game['away']['team']]] = -1
			try:
				away_pos = game['away']['fga'] + game['away']['to'] + 0.475* game['away']['fta']
				home_pos = game['home']['fga'] + game['home']['to'] + 0.475* game['home']['fta']
				if away_pos == 0 or home_pos == 0:
					error = True
			except KeyError:
					error = True
					
		
			for key in display_keys:
				try:
					if key == "shooting":
						equation[key] = (game['home']['fgm'] / game['home']['fga']) - (game['away']['fgm'] / game['away']['fga'])
					elif key == "3shooting":
						equation[key] = (game['home']['3pm'] / game['home']['3pa']) - (game['away']['3pm'] / game['away']['3pa'])
					elif key == "freethrow":
						try:
							equation[key] = (game['home']['ftm'] / game['home']['fta']) - (game['away']['ftm'] / game['away']['fta'])
						except ZeroDivisionError:
							pass
					elif key == "def_ef" and  not error:
						equation[key] = (game['away']['pts']/away_pos) - (game['home']['pts']/home_pos)
					elif key == "off_ef":
						equation[key] = (game['home']['pts']/(game['home']['fga'] + .4 * game['home']['fta'] - 1.07 * (game['home']['oreb']/(game['home']['reb'])) *(game['home']['fga'] - game['home']['fgm']) +game['home']['to'])) - (game['away']['pts']/(game['away']['fga'] + .4 * game['away']['fta'] - 1.07 * (game['away']['oreb']/(game['away']['reb'])) *(game['away']['fga'] - game['away']['fgm']) +game['away']['to']))
					else:
						equation[key] = game['home'][key] - game['away'][key]	
				except (KeyError, ZeroDivisionError):
					pass

				
			for key in display_keys: 
				'''
				weight = .25
				if (i/max_games > .25):
					weight = .5
				elif (i/max_games > .5):
					weight = .75
				elif (i/max_games > .75):
					weight = 1
					'''
				try:
					final = equation[key]
					y[key].append(final)
					m[key].append(row)
				except KeyError:
					pass
		
		for key in display_keys:
			m[key].append([1] * len(teams))		
	
	
	# Calcuates matrix for each different stat
		for key in display_keys:	
			try:
				y[key].append(0)
				num_m[key] = np.array(m[key])
				num_y[key] = np.array(y[key])
				print(len(num_m),len(num_y[key]))
				r[key] = np.linalg.lstsq(num_m[key], num_y[key])[0]
			except KeyError:
				print ("error")
			
	

    # adds homecourt advantage
    # A - B + h = Sa - Sb
    # Add column of 1s to m for homecourt advantage * A B C H = y
		for key in display_keys:
			for row in m[key][:-1]:
				row.append(1)
			m[key][-1].append(0)
	
		num_m = np.array(m)
		num_y = np.array(y)
		results = []
	
		for i,stat in enumerate(display_keys):
			stat_mod[i] = start
			inv_stat_mod[i] = stat
	
		max_stats = len(display_keys)
		i = 0
		done = False
		count = 0
		max_per = .40
		best_option = 0
		if (first):
			first = False
			perms = [x for x in itertools.product(range(start,(max_base + 1)),repeat = len(stat_mod)) if sum(x) == max_base ] # if sum(x) == max_base
		#print (perms)
			for perm in perms:
				count+=1
				if count % 100 == 0:
					print (count/len(perms), "% done")
				for i in range(max_stats):
					stat_mod[i] = perm[i]
				result = test(test_games,r)	
				if result > best_option:
					best_option = result
					print (best_option )
				if result > max_per:
					my_copy = copy.deepcopy(stat_mod)
					per_list = []
					per_list.append(result)
					copy_list = copy.deepcopy(per_list)
					sucessful_mods.append((copy_list,my_copy))
		else:
			for j in range(0,len(sucessful_mods)):
				xd = range(2)
				if (len(sucessful_mods) > 1):
					per_list,pt = sucessful_mods[j]
				else:
					per_list,pt = sucessful_mods[0]
				for mod in pt:
					stat_mod[int(mod)] = pt[mod]
	
				result = test(test_games,r)	
				
				if result > best_option:
					best_option = result
					print (best_option )
		
				if result > max_per:
					best_option 
				#print (per_list)
					per_list.append(result)
					my_copy = copy.deepcopy(stat_mod)
					copy_list = copy.deepcopy(per_list)
					#print (copy_list)
					temp_success.append((copy_list,my_copy))
			sucessful_mods = copy.deepcopy(temp_success)		
		#print (sucessful_mods)		

	with open("report_avg.json", 'w+') as f:
		f.write("\n")
		json.dump(sucessful_mods, f)



def test(games_test,ratings):
	count = 0
	#print ("Testing on ",len(games_test))
	for game in games_test:
		prediction = predict_winner(game,ratings) 

		if game['home']['pts'] > game['away']['pts']:
			actual_winner = game['home']['team']
		else:
			actual_winner = game['away']['team']
			
		if (prediction == actual_winner):
			count += 1
	
	
	percent_right = count/(len(games_test))
	
	return percent_right 
	
		
		
def predict_winner(game,r):
	t1 = teams[game['home']['team']]
	t2 = teams[game['away']['team']]
	matchup = 0
	
	for i,stat in enumerate(display_keys):
		matchup += (stat_mod[i]/max_base) * cmp_teams(t1,t2,r,stat)
	if matchup > 0:
		return game['home']['team']
	else:
		return game['away']['team']
	
	
def cmp_teams(team1,team2,rating,stat):
	difference = ((rating[stat][team1] - rating[stat][team2]) / ((rating[stat][team1] + rating[stat][team2])/2))
				#print (difference)
	return difference


		
if __name__ == '__main__':
	main(sys.argv)
