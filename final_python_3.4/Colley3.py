# !usr/bin/python
# -*- coding: utf-8 -*-

# Author: Chun Zheng
# Assignment: Massey Brackets
# Lang: Python 2.7 Class: Artificial Intelligence
# (╯°□°)╯︵ ┻━┻ table flipping emoji to represent my
# hatred for this lab.

import os
import json
import sys
import numpy as np

from pprint import pprint
from sys import stdin

class Massey(object):


    # Initialize Function
	def __init__(self):
		self.test_set = 300
		self.M = []
		self.Y = []
		self.B = []
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

        # Makes an identity matrix and then makes them all twos
		self.M = np.identity(len(self.teams))
        # According to the pdf, using a 2 makes it more
        # believable?
		self.M[self.M > 0] = 2
		self.Y = [0] * len(self.teams)
		self.Y = np.array(self.Y)

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

            # increments/decrements according
            # to how the game is played
			self.M[away_index][away_index] += 1
			self.M[home_index][home_index] += 1
			self.M[home_index][away_index] -= 1
			self.M[away_index][home_index] -= 1
            # accounts for wins, but...
            # there was no instruction for ties?
			try:  
				if datem['home']['blk'] > datem['away']['blk']:
					self.Y[home_index] += 1
					self.Y[away_index] -= 1
				elif datem['away']['blk'] > datem['home']['blk']:
					self.Y[home_index] -= 1
					self.Y[away_index] += 1
				if datem['home']['oreb'] > datem['away']['oreb']:
					self.Y[home_index] += 1
					self.Y[away_index] -= 1
				elif datem['away']['oreb'] > datem['home']['oreb']:
					self.Y[home_index] -= 1
					self.Y[away_index] += 1
			except KeyError: 
				continue

		for i in range(len(self.Y)):
			self.Y[i] = 1 + float(self.Y[i])/2
			
		# self.Y[:] = [1 + float(x)/2 for x in self.Y]
		# Ben Adams helped me with this formula
		# I couldn't figure how to apply this operation
		# throughout numpy matrix so i created a new one.
		self.B = map(lambda x: 1 + (float(x)/2), self.Y)
		self.B = np.array(self.B)

	def test(self):
		count = 0

		for game in self.data[-self.test_set:]:
			prediction = self.predict_winner(game) 

			if game['home']['pts'] > game['away']['pts']:
				actual_winner = game['home']['team']
			else:
				actual_winner = game['away']['team']
			
			if (prediction == actual_winner):
				count += 1
	
	
		percent_right = count/(self.test_set)
	
		return percent_right
	
    
	def predict_winner(self,game):
		
		t1 = self.teams.index(game['home']['team'])
		t2 = self.teams.index(game['away']['team'])
			


		matchup = self.ranks[t1] - self.ranks[t2]
	
		if matchup > 0:
			return game['home']['team']
		else:
			return game['away']['team']
	


	def rank_teams(self):
		print ("m:",self.M)
		print (np.array(self.B))
		print ("B:",self.B)
        # Dr. Parry's code given
		self.ranks = np.linalg.lstsq(self.M, self.Y)[0]
		self.teams_and_ranks = {} 
		count = 0
        # Pairs each team with their rank number
		for i in self.teams: 
			self.teams_and_ranks[self.ranks[count]] = i 
			count += 1

        # have to sort in reverse order in numpy
		#self.ranks = -np.sort(-self.ranks)

        #prints the numbered rank next to the team name
		num = 1
		for i in self.ranks:
			#print ('%s %s %.6f' %(num, self.teams_and_ranks[i], i))
			num += 1


cat = input("file you want to read?: ")
brackets = Massey()
brackets.team_matrix(cat)
brackets.play_games()
brackets.rank_teams()
print(brackets.test())
