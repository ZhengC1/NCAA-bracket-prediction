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

        self.M = []
        self.Y = []
        self.B = []
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
        for datem in self.data:
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
            except KeyError: 
                continue

        # self.Y[:] = [1 + float(x)/2 for x in self.Y]
        # Ben Adams helped me with this formula
        # I couldn't figure how to apply this operation
        # throughout numpy matrix so i created a new one.
        self.B = map(lambda x: 1 + (float(x)/2), self.Y)
        self.B = np.array(self.B)


    def rank_teams(self):

        # Dr. Parry's code given
        self.ranks = np.linalg.lstsq(self.M, self.B)[0]
        self.teams_and_ranks = {} 
        count = 0
        # Pairs each team with their rank number
        for i in self.teams: 
            self.teams_and_ranks[self.ranks[count]] = i 
            count += 1

        # have to sort in reverse order in numpy
        self.ranks = -np.sort(-self.ranks)

        #prints the numbered rank next to the team name
        num = 1
        for i in self.ranks:
            print '%s %s %.6f' %(num, self.teams_and_ranks[i], i)
            num += 1


cat = raw_input("file you want to read?: ")
brackets = Massey()
brackets.team_matrix(cat)
brackets.play_games()
brackets.rank_teams()
