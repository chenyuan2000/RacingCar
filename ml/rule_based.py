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
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.last_command = 0
        self.last_command2 = 0
        pass
    
    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
    | 10|  1 |  2 |  3 | 12|
    |   |    |  5 |    |   |
    | 11|  4 |  c |  6 | 13|
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
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

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if (self.last_command == 2) and (self.last_command2 == 2):
                        if x <= 45 and x >= -45 :      
                            if y > 0 and y < 300:
                                grid.add(2)
                                if y < 160:
                                    speed_ahead = car["velocity"]
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
                    elif (self.last_command == 1) and (self.last_command2 == 1):
                        if x <= 45 and x >= -45 :      
                            if y > 0 and y < 300:
                                grid.add(2)
                                if y < 160:
                                    speed_ahead = car["velocity"]
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
                                    speed_ahead = car["velocity"]
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
                    self.last_command2 = self.last_command
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            #if self.player_no == 0:
            #    print("1",grid)
                
            if len(grid) == 0:
                self.last_command = 0
                return ["SPEED"]
            else:
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        self.last_command = 0
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        self.last_command = 0
                        return ["SPEED", "MOVE_RIGHT"]
                    else :
                        self.last_command = 0
                        return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        if self.last_command == 1: # left first
                            if (4 not in grid) and (7 not in grid): # turn left 
                                self.last_command = 1
                                if self.car_vel <= speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    return ["BRAKE", "MOVE_LEFT"]
                            elif (6 not in grid) and (9 not in grid): # turn right
                                self.last_command = 2
                                if self.car_vel <= speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    return ["BRAKE", "MOVE_RIGHT"]
                            else : 
                                self.last_command = 0
                                if self.car_vel <= speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    return ["BRAKE"]
                        elif self.last_command == 2:
                            if (6 not in grid) and (9 not in grid): # turn right
                                self.last_command = 2
                                if self.car_vel <= speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    return ["BRAKE", "MOVE_RIGHT"]
                            elif (4 not in grid) and (7 not in grid): # turn left 
                                self.last_command = 1
                                if self.car_vel <= speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    return ["BRAKE", "MOVE_LEFT"]
                            else : 
                                self.last_command = 0
                                if self.car_vel <= speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    return ["BRAKE"]
                        
                    if self.last_command == 1 : # left first
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left 
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left
                            self.last_command = 1
                            return ["MOVE_LEFT"]    
                        if (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["MOVE_RIGHT"]
                    elif self.last_command == 2 :#right first
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left
                            self.last_command = 1
                            return ["MOVE_LEFT"] 
                    
                    if (10 not in grid) and (11 not in grid): # left first
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left 
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left
                            self.last_command = 1
                            return ["MOVE_LEFT"]    
                        if (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["MOVE_RIGHT"]
                    else:#right first
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            self.last_command = 2
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left
                            self.last_command = 1
                            return ["SPEED", "MOVE_LEFT"]
                        if (6 not in grid) and (9 not in grid): # turn right
                            self.last_command = 2
                            return ["MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left
                            self.last_command = 1
                            return ["MOVE_LEFT"]    

        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass