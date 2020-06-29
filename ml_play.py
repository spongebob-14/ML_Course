# for midterm3
viberation=0
l_lowest=800
r_lowest=800
c_lowest=800
prefer=0
pre_lanes=0
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
        pass
    
    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] <= 65: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 565: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 35 and x >= -35 :      
                        if y > 0 and y < 200:
                            grid.add(2)
                            speed_ahead = car["velocity"]
                            bias=0
                            if self.car_vel-car["velocity"]>3:
                                bias=5
                            if self.car_vel-car["velocity"]>6:
                                bias=15
                            elif self.car_vel-car["velocity"]>10:
                                bias=25
                            else:
                                bias=0
                            if y < 130+bias:
                                
                                grid.add(5) 
                        elif y <= 0 and y > -100:
                            grid.add(8)
                    if x >= -70 and x < -35 :
                        if y > 100 and y < 200:
                            grid.add(3)
                        elif y < -70 and y > -100:
                            grid.add(9)
                        elif y <= 100 and y >= -70:
                            grid.add(6)
                    if x <= 70 and x > 35:
                        if y > 100 and y < 200:
                            grid.add(1)
                        elif y < -70 and y > -100:
                            grid.add(7)
                        elif y <= 100 and y >= -70:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            # if self.player_no == 0:
            #     print(grid)
            """
            if(self.car_vel<15):
                for i in range(1,10):
                    if(i in grid):
                        print("{}".format(i),end="")
                    else:
                        print("*",end="")
                    if(i%3==0):
                        print("")
                print("len={}".format(self.car_lane))
                print("pos=({},{})".format(self.car_pos[0],self.car_pos[1]))
            """    

            """
            global pre_lanes
            pl_bias=2
            if(70-pl_bias<self.car_pos[0] and self.car_pos[0]<70+pl_bias):
                self.lanes=pre_lanes
            if(140-pl_bias<self.car_pos[0] and self.car_pos[0]<140+pl_bias):
                self.lanes=pre_lanes
            if(210-pl_bias<self.car_pos[0] and self.car_pos[0]<210+pl_bias):
                self.lanes=pre_lanes
            if(280-pl_bias<self.car_pos[0] and self.car_pos[0]<280+pl_bias):
                self.lanes=pre_lanes
            if(350-pl_bias<self.car_pos[0] and self.car_pos[0]<350+pl_bias):
                self.lanes=pre_lanes
            if(420-pl_bias<self.car_pos[0] and self.car_pos[0]<420+pl_bias):
                self.lanes=pre_lanes
            if(490-pl_bias<self.car_pos[0] and self.car_pos[0]<490+pl_bias):
                self.lanes=pre_lanes
            if(560-pl_bias<self.car_pos[0] and self.car_pos[0]<560+pl_bias):
                self.lanes=pre_lanes
            pre_lanes=self.lanes
            """
            
            coin_prefer=-100
            for coin in scene_info["coins"]:
                if coin[1]<self.car_pos[1]+60 and coin[1]<self.car_pos[1]-40:
                    if(self.car_pos[0]-15<=coin[0] and coin[0]<=self.car_pos[0]+15):
                        coin_prefer=0
                    elif (self.car_pos[0]-15-35<coin[0] and coin[0]<self.car_pos[0]-15):
                        coin_prefer=-1
                    elif (self.car_pos[0]+15<coin[0] and coin[0]<self.car_pos[0]+15+35):
                        coin_prefer=1
            if(coin_prefer!=-100):
                if (5 in grid): # NEED to BRAKE
                        print("need to break")
                        r_avail=0
                        l_avail=0
                        if (4 not in grid): # turn left 
                            l_avail=1
                        if (6 not in grid): # turn right
                            r_avail=1
                        if coin_prefer==-1:
                            if l_avail==1:
                                print("move left 10")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    print("break 5")
                                    return ["BRAKE", "MOVE_LEFT"]
                            elif r_avail==1:
                                print("move right 10")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    print("break 4")
                                    return ["BRAKE", "MOVE_RIGHT"]
                            else:
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    print("break 1")
                                    return ["BRAKE"]
                        elif coin_prefer==1:
                            if r_avail==1:
                                print("move right 11")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    print("break 3")
                                    return ["BRAKE", "MOVE_RIGHT"]
                            elif l_avail==1:
                                print("move left 11")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    print("break 2")
                                    return ["BRAKE", "MOVE_LEFT"]
                            else:
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    print("break 1")
                                    return ["BRAKE"]
                        else:
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                print("break 1")
                                return ["BRAKE"]
                    #end of check break
                if(coin_prefer==0):
                    return ["SPEED"]
                elif (coin_prefer==-1) and (4 not in grid):
                    if (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        return ["MOVE_LEFT"]
                elif (coin_prefer==1) and (6 not in grid):
                    if(3 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["MOVE_RIGHT"]


            global l_lowest,r_lowest,c_lowest,prefer
            l_lowest=0
            r_lowest=0
            c_lowest=0
            prefer=100 #default value
            if self.car_lane==0:
                l_lowest=3000
            elif self.car_lane==8:
                r_lowest=3000
            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    car_lane=car["pos"][0]//70
                    if car_lane==self.car_lane-1 and car["pos"][1]<self.car_pos[1]:
                        if car["pos"][1]>l_lowest:
                            l_lowest=car["pos"][1]
                    if car_lane==self.car_lane and car["pos"][1]<self.car_pos[1]:
                        if car["pos"][1]>c_lowest:
                            c_lowest=car["pos"][1]
                    if car_lane==self.car_lane+1 and car["pos"][1]<self.car_pos[1]:
                        if car["pos"][1]>r_lowest:
                            r_lowest=car["pos"][1]
            if l_lowest<c_lowest and l_lowest<r_lowest:
                prefer=-1
            if r_lowest<l_lowest and r_lowest<c_lowest:
                prefer=1
            if c_lowest<l_lowest and c_lowest<r_lowest:
                prefer=0
            if(self.car_vel<15):
                print("{},{},{}".format(l_lowest,c_lowest,r_lowest))
            
            tolerance=2
            if (prefer!=100): #has only one perfer
                #(l_lowest!=c_lowest and c_lowest!= r_lowest and r_lowest!= l_lowest):
                
                
                #check break
                if (5 in grid): # NEED to BRAKE
                    print("need to break")
                    r_avail=0
                    l_avail=0
                    if (4 not in grid): # turn left 
                        l_avail=1
                    if (6 not in grid): # turn right
                        r_avail=1
                    if prefer==-1:
                        if l_avail==1:
                            print("move left 10")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                print("break 5")
                                return ["BRAKE", "MOVE_LEFT"]
                        elif r_avail==1:
                            print("move right 10")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                print("break 4")
                                return ["BRAKE", "MOVE_RIGHT"]
                        else:
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                print("break 1")
                                return ["BRAKE"]
                    elif prefer==1:
                        if r_avail==1:
                            print("move right 11")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                print("break 3")
                                return ["BRAKE", "MOVE_RIGHT"]
                        elif l_avail==1:
                            print("move left 11")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                print("break 2")
                                return ["BRAKE", "MOVE_LEFT"]
                        else:
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                print("break 1")
                                return ["BRAKE"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            return ["SPEED"]
                        else:
                            print("break 1")
                            return ["BRAKE"]
                #end of check break

                if prefer==1 and (6 not in grid):
                    if(3 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["MOVE_RIGHT"]
                elif prefer==-1 and (4 not in grid):
                    if (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        return ["MOVE_LEFT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["SPEED"]

            elif (l_lowest==r_lowest and r_lowest<=c_lowest):
                #all the same or l, r higher

                #check break
                if (5 in grid): # NEED to BRAKE
                    print("need to break")
                    r_avail=0
                    l_avail=0
                    if (4 not in grid): # turn left 
                        l_avail=1
                    if (6 not in grid): # turn right
                        r_avail=1
                    if self.car_pos[0]>315:
                        if l_avail==1:
                            print("move left 10")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                print("break 5")
                                return ["BRAKE", "MOVE_LEFT"]
                        elif r_avail==1:
                            print("move right 10")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                print("break 4")
                                return ["BRAKE", "MOVE_RIGHT"]
                        else:
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                print("break 1")
                                return ["BRAKE"]
                    elif (self.car_pos[0]<315):
                        if r_avail==1:
                            print("move right 11")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                print("break 3")
                                return ["BRAKE", "MOVE_RIGHT"]
                        elif l_avail==1:
                            print("move left 11")
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                print("break 2")
                                return ["BRAKE", "MOVE_LEFT"]
                        else:
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                print("break 1")
                                return ["BRAKE"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            return ["SPEED"]
                        else:
                            print("break 1")
                            return ["BRAKE"]
                #end of check break

                if self.car_lane<5 and (6 not in grid):
                    if (3 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["MOVE_RIGHT"]
                elif self.car_lane>4 and (4 not in grid):
                    if (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        return ["MOVE_LEFT"]
                elif (6 not in grid):
                    if (3 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["MOVE_RIGHT"]
                elif (4 not in grid):
                    if (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        return ["MOVE_LEFT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["SPEED"]
            
            elif (l_lowest==c_lowest):
                #l, c higher

                #check break
                # check left first!
                if (5 in grid): # NEED to BRAKE
                    print("need to break")
                    if (4 not in grid):
                        print("move left 10")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print("break 5")
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (6 not in grid):
                        print("move right 10")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print("break 4")
                            return ["BRAKE", "MOVE_RIGHT"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            return ["SPEED"]
                        else:
                            print("break 1")
                            return ["BRAKE"]
                #end of check break
                if (4 not in grid):
                    if(1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        return ["MOVE_LEFT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["SPEED"]

            elif (c_lowest==r_lowest):
                #r. c higher
                
                #check break
                #chec right first
                if (5 in grid): # NEED to BRAKE
                    print("need to break")
                    if (6 not in grid):
                        print("move right 11")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print("break 3")
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (4 not in grid):
                        print("move left 11")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print("break 2")
                            return ["BRAKE", "MOVE_LEFT"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            return ["SPEED"]
                        else:
                            print("break 1")
                            return ["BRAKE"]
                #end of check break
                if (6 not in grid):
                    if (3 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["MOVE_RIGHT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["SPEED"]

            else:
                print("something wrong!")

            print("not success return!!")

            if (5 in grid): # NEED to BRAKE
                print("need to break")
                r_avail=0
                l_avail=0
                if (4 not in grid): # turn left 
                    l_avail=1
                if (6 not in grid): # turn right
                    r_avail=1
                if self.car_pos[0]>315:
                    if l_avail==1:
                        print("move left 10")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print("break 5")
                            return ["BRAKE", "MOVE_LEFT"]
                    elif r_avail==1:
                        print("move right 10")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print("break 4")
                            return ["BRAKE", "MOVE_RIGHT"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            return ["SPEED"]
                        else:
                            print("break 1")
                            return ["BRAKE"]
                elif (self.car_pos[0]<315):
                    if r_avail==1:
                        print("move right 11")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print("break 3")
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif l_avail==1:
                        print("move left 11")
                        if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print("break 2")
                            return ["BRAKE", "MOVE_LEFT"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            return ["SPEED"]
                        else:
                            print("break 1")
                            return ["BRAKE"]
            
            
            if (l_lowest==r_lowest and r_lowest<=c_lowest):
                if self.car_lane<4 and (6 not in grid):
                    return ["SPEED", "MOVE_RIGHT"]
                elif self.car_lane>4 and (4 not in grid):
                    return ["SPEED", "MOVE_LEFT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["SPEED"]

            

            if (l_lowest==c_lowest or c_lowest==r_lowest or r_lowest==l_lowest):
                print("no prefer")                
                if len(grid) == 0 or (2 not in grid):
                    if self.car_lane<4 and (6 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    elif self.car_lane>4 and (4 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        print("need to break")
                        r_avail=0
                        l_avail=0
                        if (4 not in grid): # turn left 
                            l_avail=1
                            """
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                            """
                        if (6 not in grid): # turn right
                            r_avail=1
                        """
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                            
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                        """
                        if self.car_pos[0]>315:
                            if l_avail==1:
                                print("move left 10")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    print("break 5")
                                    return ["BRAKE", "MOVE_LEFT"]
                            elif r_avail==1:
                                print("move right 10")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    print("break 4")
                                    return ["BRAKE", "MOVE_RIGHT"]
                            else:
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    print("break 1")
                                    return ["BRAKE"]
                        elif (self.car_pos[0]<315):
                            if r_avail==1:
                                print("move right 11")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    print("break 3")
                                    return ["BRAKE", "MOVE_RIGHT"]
                            elif l_avail==1:
                                print("move left 11")
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    print("break 2")
                                    return ["BRAKE", "MOVE_LEFT"]
                            else:
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    print("break 1")
                                    return ["BRAKE"]


                    """
                    if (self.car_pos[0] < 60 ):
                        return ["SPEED", "MOVE_RIGHT"]
                    """

                    if self.car_pos[0]<210:
                        """
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            print("move right 1")
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            print("move left 1")
                            return ["SPEED", "MOVE_LEFT"]
                        el
                        """
                        if (3 not in grid) and (6 not in grid): # turn right
                            print("move right 2")
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (1 not in grid) and (4 not in grid): # turn left 
                            print("move left 2")
                            return ["SPEED", "MOVE_LEFT"]
                        elif (4 not in grid) and (7 not in grid): # turn left 
                            print("move left 3")
                            return ["MOVE_LEFT"]    
                        elif (6 not in grid) and (9 not in grid): # turn right
                            print("move right 3")
                            return ["MOVE_RIGHT"]
                    elif self.car_pos[0]>420:
                        """
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            print("move left 4")
                            return ["SPEED", "MOVE_LEFT"]
                        elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            print("move right 4")
                            return ["SPEED", "MOVE_RIGHT"]
                        el
                        """
                        if (1 not in grid) and (4 not in grid): # turn left 
                            print("move left 5")
                            return ["SPEED", "MOVE_LEFT"]
                        elif (3 not in grid) and (6 not in grid): # turn right
                            print("move right 5")
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (4 not in grid) and (7 not in grid): # turn left 
                            print("move left 6")
                            return ["MOVE_LEFT"]    
                        elif (6 not in grid) and (9 not in grid): # turn right
                            print("move right 6")
                            return ["MOVE_RIGHT"]
                    """
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        print("move left 7")
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        print("move right 7")
                        return ["SPEED", "MOVE_RIGHT"]
                    """
                    if (1 not in grid) and (4 not in grid): # turn left 
                        print("move left 8")
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        print("move right 8")
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid): # turn left 
                        print("move left 9")
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid): # turn right
                        print("move right 9")
                        return ["MOVE_RIGHT"]
                
            else:
                print("has prefer")
                if prefer==1 and (3 not in grid) and (6 not in grid):
                    return ["SPEED", "MOVE_RIGHT"]
                elif prefer==-1 and (1 not in grid) and (4 not in grid):
                    return ["SPEED", "MOVE_LEFT"]
                else:
                    print("regular 3")
                    if self.car_pos[0] > self.lanes[self.car_lane]-tolerance:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]+tolerance:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["SPEED"]

            ########################################

                    
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
