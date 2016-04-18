# !usr/bin/python
# -*- coding: utf-8 -*-

# Author: Chun Zheng
# Assignment: Massey Brackets
# Lang: Python 2.7 Class: Artificial Intelligence
# (?°?°)?? ??? table flipping emoji to represent my
# hatred for this lab.
import itertools
import os
import json
import sys
import numpy as np
import copy

from pprint import pprint
from sys import stdin

class Massey(object):


    # Initialize Function
	def __init__(self):
		self.ranks = {}
		self.stat_mod = {}
		self.max_base = 2
		self.start = 0
		self.test_set = 200
		self.M = {}
		self.Y = {}
		self.B = {}
		self.stats = ["pts","shooting","dreb", "ast", "stl", "blk","def_ef", "off_ef", "oreb" ]
		self.test_games = []
		self.teams = []
		self.data = None

    # This will read the Json
    # The loop will also append all the team names
    # The cast set() then deletes any extras
	def team_matrix(self, json_file):

		if(os.path.isfile(json_file)):
			with open(json_file) as data_file:
				self.data = json.load(data_file)
				for i in self.data:
					self.teams.append(i["home"]["team"])
					self.teams.append(i["away"]["team"])

			self.teams = set(self.teams)
			self.teams = list(self.teams)

		for key in self.stats:
        # Makes an identity matrix and then makes them all twos
			self.M[key] = np.identity(len(self.teams))
        # According to the pdf, using a 2 makes it more
        # believable?
			self.M[key][self.M[key] > 0] = 2
			self.Y[key] = [0] * len(self.teams)
			self.Y[key] = np.array(self.Y[key])

	def play_games(self):
        # reused from Massey.py
		count = 0
		for datem in self.data[0:(len(self.data) - self.test_set)]:
		
		
			'''
			if datem['notes']:
				if "MEN'S BASKETBALL" in datem['notes']:
					self.test_games.append(datem) 
					continue
			'''
		
			home_team = datem["home"]["team"]
			away_team = datem["away"]["team"]
			home_index = self.teams.index(home_team)
			away_index = self.teams.index(away_team)
			error = False
            # increments/decrements according
            # to how the datem is played
			try:
				away_pos = datem['away']['fga'] + datem['away']['to'] + 0.475* datem['away']['fta']
				home_pos = datem['home']['fga'] + datem['home']['to'] + 0.475* datem['home']['fta']
				if away_pos == 0 or home_pos == 0:
					error = True
			except KeyError:
					error = True
			
			
            # accounts for wins, but...
            # there was no instruction for ties?
			for key in self.stats:
				try: 
					if key == "shooting":
						equation = (datem['home']['fgm'] / datem['home']['fga']) - (datem['away']['fgm'] / datem['away']['fga'])
						if equation > 0:
							self.Y[key][home_index] += 1
							self.Y[key][away_index] -= 1
						else:
							self.Y[key][home_index] -= 1
							self.Y[key][away_index] += 1
				
					elif key == "def_ef" and  not error:
						equation = (datem['away']['pts']/away_pos) - (datem['home']['pts']/home_pos)
						if equation > 0:
							self.Y[key][home_index] += 1
							self.Y[key][away_index] -= 1
						else:
							self.Y[key][home_index] -= 1
							self.Y[key][away_index] += 1
					elif key == "off_ef":
						equation = (datem['home']['pts']/(datem['home']['fga'] + .4 * datem['home']['fta'] - 1.07 * (datem['home']['oreb']/(datem['home']['reb'])) *(datem['home']['fga'] - datem['home']['fgm']) +datem['home']['to'])) - (datem['away']['pts']/(datem['away']['fga'] + .4 * datem['away']['fta'] - 1.07 * (datem['away']['oreb']/(datem['away']['reb'])) *(datem['away']['fga'] - datem['away']['fgm']) +datem['away']['to']))
						if equation > 0:
							self.Y[key][home_index] += 1
							self.Y[key][away_index] -= 1
						else:
							self.Y[key][home_index] -= 1
							self.Y[key][away_index] += 1
					else:
						if datem['home'][key] > datem['away'][key]:
							self.Y[key][home_index] += 1
							self.Y[key][away_index] -= 1
						else:
							self.Y[key][home_index] -= 1
							self.Y[key][away_index] += 1
							
					self.M[key][away_index][away_index] += 1
					self.M[key][home_index][home_index] += 1
					self.M[key][home_index][away_index] -= 1
					self.M[key][away_index][home_index] -= 1
				except (KeyError,ZeroDivisionError): 
					continue

			for i in range(len(self.Y[key])):
				self.Y[key][i] = 1 + float(self.Y[key][i])/2
			
		# self.Y[key][:] = [1 + float(x)/2 for x in self.Y[key]]
		# Ben Adams helped me with this formula
		# I couldn't figure how to apply this operation
		# throughout numpy matrix so i created a new one.
		self.B = map(lambda x: 1 + (float(x)/2), self.Y[key])
		self.B = np.array(self.B)

	def test(self):
		count = 0

		for game in self.data[-self.test_set:]:
			prediction = self.predict_winner(game) 
			#print (prediction)
			
			if game['home']['pts'] > game['away']['pts']:
				actual_winner = game['home']['team']
			else:
				actual_winner = game['away']['team']
			
			if (prediction == actual_winner):
			#	print ("right")
				count += 1
			#print (prediction,actual_winner)
		#print (count)
	
		percent_right = count/(self.test_set)
	
		return percent_right
		
	def cmp_teams(self,team1,team2,rating,stat):
		difference = ((rating[stat][team1] - rating[stat][team2]) / ((rating[stat][team1] + rating[stat][team2])/2))
				#print (difference)
		return difference
    
	def predict_winner(self,game):
		
		t1 = self.teams.index(game['home']['team'])
		t2 = self.teams.index(game['away']['team'])
			
		matchup = 0
		#print(game['home']['team'],self.ranks[key][t1],game['away']['team'],self.ranks[key][t2])	
		#matchup = self.ranks[key][t1] - self.ranks[key][t2]
		for i,stat in enumerate(self.stats):
			matchup += (self.stat_mod[i]/self.max_base) * self.cmp_teams(t1,t2,self.ranks,stat)
			
		
	
		if matchup > 0:
			return game['home']['team']
		else:
			return game['away']['team']
	
	

	def rank_teams(self,key):
		#print ("m:",self.M[key])
		#print (np.array(self.B))
		#print ("B:",self.B)
        # Dr. Parry's code given
		self.ranks[key] = np.linalg.lstsq(self.M[key], self.Y[key])[0]
		self.teams_and_ranks = {} 
		count = 0
        # Pairs each team with their rank number
		for i in self.teams: 
			self.teams_and_ranks[self.ranks[key][count]] = i 
			count += 1

        # have to sort in reverse order in numpy
		#self.ranks[key] = -np.sort(-self.ranks[key])

        #prints the numbered rank next to the team name
		num = 1
		for i in self.ranks[key][0:10]:
			#print ('%s %s %.6f' %(num, self.teams_and_ranks[i], i))
			num += 1

			
			
			


files = ["2013.json","2014.json","2015.json","new_2016.json"]
first = True
sucessful_mods = []
for file in files:
	temp_success = []
	#cat = input("file you want to read?: ")
	brackets = Massey()
	brackets.team_matrix(file)
	brackets.play_games()
	for keyz in brackets.stats:
		#print (keyz)
		brackets.rank_teams(keyz)
	for i,stat in enumerate(brackets.stats):
			brackets.stat_mod[i] = brackets.start
	max_per = .6
	max_stats = len(brackets.stats)
	count = 0
	best_option = 0
	if (first):
		first = False
		perms = [x for x in itertools.product(range(brackets.start,(brackets.max_base + 1)),repeat = len(brackets.stat_mod))] # if sum(x) == brackets.max_base
		#print (perms)
		for perm in perms:
			count+=1
			if count % 100 == 0:
				print (count/len(perms), "% done")
			for i in range(max_stats):
				brackets.stat_mod[i] = perm[i]
			result = brackets.test()	
			if result > best_option:
				best_option = result
				print (best_option )
			if result > max_per:
					my_copy = copy.deepcopy(brackets.stat_mod)
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
				brackets.stat_mod[int(mod)] = pt[mod]
	
			result = brackets.test()	
				
			if result > best_option:
				best_option = result
				print (best_option )
		
			if result > max_per:
				best_option 
				#print (per_list)
				per_list.append(result)
				my_copy = copy.deepcopy(brackets.stat_mod)
				copy_list = copy.deepcopy(per_list)
				#print (copy_list)
				temp_success.append((copy_list,my_copy))
		sucessful_mods = copy.deepcopy(temp_success)		
	print (sucessful_mods)		
with open("data_totals9.json", 'w+') as f:
		f.write("\n")
		json.dump(sucessful_mods, f)
		f.write("\n")
		json.dump(brackets.stats)

