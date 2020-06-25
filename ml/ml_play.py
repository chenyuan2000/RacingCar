# -*- coding: utf-8 -*-
import pickle
import numpy as np
from os import path
import os 

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0 #initialization
        self.car_pos = (0,0)
        self.feature = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.last_command = 0
        with open(path.join(path.dirname(__file__), 'save', 'decisiontreemodel.pickle'), 'rb') as file: self.model = pickle.load(file)
        pass
    
    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        def check_grid():
            self.car_pos = scene_info[self.player]
            if scene_info["status"] != "ALIVE":
                return "RESET"
        
            if len(self.car_pos) == 0:
                self.car_pos = (0,0)

            grid = set()
            for i in range(len(scene_info["cars_info"])): # for all cars information in scene of one frame
                car = scene_info["cars_info"][i]
                if car["id"]==self.player_no: #player's car information
                    self.car_vel = car["velocity"] 
                else: # computer's cars information
                    if self.car_pos[0] <= 40: # left bound 
                        grid.add(1)
                        grid.add(4)
                        grid.add(7)
                        grid.add(10)
                        grid.add(11)
                    elif self.car_pos[0] >= 585: # right bound
                        grid.add(3)
                        grid.add(6)
                        grid.add(9)
                        grid.add(12)
                        grid.add(13)

                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position

                    if self.last_command == 2:
                        if x <= 45 and x >= -45 :      
                            if y > 0 and y < 300:
                                grid.add(2)
                                if y < 160:
                                    grid.add(5) 
                                elif y < 0 and y > -200:
                                    grid.add(8)
                        if x > -55 and x < -15 :
                            if y > 80 and y < 250:
                                grid.add(3)
                            elif y < -80 and y > -200:
                                grid.add(9)
                            elif y < 80 and y > -80:
                                grid.add(6)
                        if x > -115 and x < -55 :
                            if y > 80 and y < 250:
                                grid.add(12)
                            elif y < 80 and y > -80:
                                grid.add(13)
                        if x < 105 and x > 45:
                            if y > 80 and y < 250:
                                grid.add(1)
                            elif y < -80 and y > -200:
                                grid.add(7)
                            elif y < 80 and y > -80:
                                grid.add(4)
                        if x < 185 and x > 105:
                            if y > 80 and y < 250:
                                grid.add(10)
                            elif y < 80 and y > -80:
                                grid.add(11)
                    elif self.last_command == 1:
                        if x <= 45 and x >= -45 :      
                            if y > 0 and y < 300:
                                grid.add(2)
                                if y < 160:
                                    grid.add(5) 
                                elif y < 0 and y > -200:
                                    grid.add(8)
                        if x > -105 and x < -45 :
                            if y > 80 and y < 250:
                                grid.add(3)
                            elif y < -80 and y > -200:
                                grid.add(9)
                            elif y < 80 and y > -80:
                                grid.add(6)
                        if x > -185 and x < -105 :
                            if y > 80 and y < 250:
                                grid.add(12)
                            elif y < 80 and y > -80:
                                grid.add(13)
                        if x < 55 and x > 15:
                            if y > 80 and y < 250:
                                grid.add(1)
                            elif y < -80 and y > -200:
                                grid.add(7)
                            elif y < 80 and y > -80:
                                grid.add(4)
                        if x < 115 and x > 55:
                            if y > 80 and y < 250:
                                grid.add(10)
                            elif y < 80 and y > -80:
                                grid.add(11)
                    else:
                        if x <= 45 and x >= -45 :      
                            if y > 0 and y < 300:
                                grid.add(2)
                                if y < 160:
                                    grid.add(5) 
                                elif y < 0 and y > -200:
                                    grid.add(8)
                        if x > -90 and x < -45 :
                            if y > 80 and y < 250:
                                grid.add(3)
                            elif y < -80 and y > -200:
                                grid.add(9)
                            elif y < 80 and y > -80:
                                grid.add(6)
                        if x > -165 and x < -90 :
                            if y > 80 and y < 250:
                                grid.add(12)
                            elif y < 80 and y > -80:
                                grid.add(13)
                        if x < 90 and x > 45:
                            if y > 80 and y < 250:
                                grid.add(1)
                            elif y < -80 and y > -200:
                                grid.add(7)
                            elif y < 80 and y > -80:
                                grid.add(4)
                        if x < 165 and x > 90:
                            if y > 80 and y < 250:
                                grid.add(10)
                            elif y < 80 and y > -80:
                                grid.add(11)
            return move(grid = grid)
        
        def move(grid):

            grid_tolist = list(grid)
            grid_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for i in grid_tolist:
                grid_data[i-1] = 1 # change grid set into feature's data shape
            grid_data = np.array(grid_data).reshape(1,-1)
            self.feature = grid_data
            self.feature = np.array(self.feature)
            self.feature = self.feature.reshape((1,-1))
            y = self.model.predict(self.feature) 

            if y == 0:
                self.last_command = 0
                return ["SPEED"]
            if y == 1:
                self.last_command = 1
                return ["SPEED", "MOVE_LEFT"]
            if y == 2:
                self.last_command = 2
                return ["SPEED", "MOVE_RIGHT"]
            if y == 3:
                self.last_command = 0
                return ["BRAKE"]
            if y == 4:
                self.last_command = 1
                return ["BRAKE", "MOVE_LEFT"]
            if y == 5:
                self.last_command = 2
                return ["BRAKE", "MOVE_RIGHT"]
            if y == 6:
                self.last_command = 1
                return ["LEFT"]
            if y == 7:
                self.last_command = 2
                return ["RIGHT"]
        
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
