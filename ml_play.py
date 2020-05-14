"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm


predictpos=(0,0)#(scene_info["ball"][0]+scene_info["ball_speed"][0],scene_info["ball"][1]+scene_info["ball_speed]"][1])
currspeed=(0,0)#scene_info["ball_speed"]
currframe=0#scene_info["frame"]
opponentpos=(0,0)

blocker1=(0,0)
blocker2=(0,0)
blockerdirect=0

def ml_loop(side: str):
    #to let all function can use the variable
    global predictpos
    global currspeed
    global currframe
    global opponentpos

    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    def vadd(a,b):
        return (a[0]+b[0],a[1]+b[1])
    def vsub(a,b):
        return (a[0]-b[0],a[1]-b[1])
    def vscale(s,a):
        return tuple(s*x for x in a)

    def speed_up(currspeed):
        if currspeed[0]>0 and currspeed[1]>0:
            return vadd(currspeed,(1,1))
        elif currspeed[0]>0 and currspeed[1]<0:
            return vadd(currspeed,(1,-1))
        elif currspeed[0]<0 and currspeed[1]>0:
            return vadd(currspeed,(-1,1))
        elif currspeed[0]<0 and currspeed[1]<0:
            return vadd(currspeed,(-1,-1))
        else:
            return currspeed
    global blocker1
    global blocker2
    global blockerdirect
    def blocker_pos(frame):
        global blocker1
        global blocker2
        global blockerdirect
        if frame<=2:
            return scene_info["blocker"]
        remind=frame%72
        bposx=blocker1[0]+(remind-1)*blockerdirect
        while(bposx>180 or bposx<0):
            if bposx>180:
                bposx=360-bposx
            if bposx<0:
                bposx=-bposx
        if side=="1P":
            print(side+" at frame "+str(frame)+" with pos "+str(bposx))
        return bposx

    
    """
    predictpos=(0,0)#(scene_info["ball"][0]+scene_info["ball_speed"][0],scene_info["ball"][1]+scene_info["ball_speed]"][1])
    currspeed=(0,0)#scene_info["ball_speed"]
    currframe=0#scene_info["frame"]
    opponentpos=(0,0)
    """

    def predict_path():
        global predictpos
        global currframe
        global currspeed
        global opponentpos
        
        if currspeed[0]==0 or currspeed[1]==0:
            print("speed of one direct is still 0")
            return
        """
        predictpos=(scene_info["ball"][0]+scene_info["ball_speed"][0],scene_info["ball"][1]+scene_info["ball_speed]"][1])
        currspeed=scene_info["ball_speed"]
        currframe=scene_info["frame"]
        opponentpos=(0,0) 
        """
        printmessage=False
        while predictpos[1]<415:
            if side=="1P" and printmessage:
                print(side+" predict:"+str(predictpos))
                print(side+" opponent"+str(opponentpos))
            if predictpos[1]>=240 and currspeed[1]<0:  
                # Ball is leaving but not pass the blocker
                if side=="1P" and printmessage:
                    print(side+"start of situation 1")
                lentoblocker=-(predictpos[1]-261)//currspeed[1]
                    #261 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-(predictpos[0]+5))//currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)//currspeed[0]
                lentocollide=min(lentoside,lentoblocker)
                
                if (lentocollide+currframe)//100>currframe//100:
                    #speed up before collide
                    predictpos=vadd(predictpos,vscale(int((int(currframe//100)+1)*100-currframe),currspeed))
                    currframe=(currframe//100+1)*100
                    currspeed=speed_up(currspeed)
                    if side=="1P" and printmessage:
                        print(side+"situation 1 with speed up")
                    continue
                else:
                    if lentoside<lentoblocker:
                        predictpos=vadd(predictpos,vscale((lentoside+1),currspeed))
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>195:
                            predictpos=(195,predictpos[1])
                        if predictpos[0]<0:
                            predictpos=(0,predictpos[1])
                        currspeed=(-currspeed[0],currspeed[1])
                        currframe=currframe+lentoside+1
                        if side=="1P" and printmessage:
                            print(side+"situation 1 with hit side")
                        continue
                    else:
                        if lentoblocker>0:
                            currframe=currframe+lentoblocker
                            predictpos=vadd(predictpos,vscale((lentoblocker),currspeed))
                            if predictpos[0]>195:
                                predictpos=(195,predictpos[1])
                            if predictpos[0]<0:
                                predictpos=(0,predictpos[1])
                        blocker_x=blocker_pos(currframe)
                        blocker_y=240
                        #it will collide in next frame so it need a width range
                        while predictpos[1]>=240 and predictpos[1]<=260-currspeed[1]:
                            #guess the next position with check in next loop
                            predictpos=vadd(predictpos,currspeed)
                            if predictpos[0]>200:
                                predictpos=(200,predictpos[1])
                            if predictpos[0]<0:
                                predictpos=(0,predictpos[1])
                            currframe+=1
                            if currframe%100==0:
                                currspeed=speed_up(currspeed)

                            if predictpos[0]>blocker_x and predictpos[0]<blocker_x+30:
                                #modify if collide into blocker
                                deepy=blocker_y+20-predictpos[1]
                                if currspeed[0]>0:
                                    deepx=(predictpos[0]+5)-blocker_x
                                    if deepx==deepy:
                                        predictpos=(blocker_x,blocker_y+20)
                                        currspeed=vscale(-1,currspeed)
                                        break
                                        #bounce back
                                    if deepx>deepy:
                                        predictpos=(predictpos[0],blocker_y+20)
                                        currspeed=(currspeed[0],-currspeed[1])
                                        break
                                        #bounce back
                                    if deepx<deepy:
                                        predictpos=(blocker_x,predictpos[1])
                                        currspeed=(-currspeed[0],currspeed[1])
                                        continue
                                else:
                                    deepx=blocker_x+30-predictpos[0]
                                    if deepx==deepy:
                                        predictpos=(blocker_x+30,blocker_y+20)
                                        currspeed=vscale(-1,currspeed)
                                        break
                                    if deepx>deepy:
                                        predictpos=(predictpos[0],blocker_y+20)
                                        currspeed=(currspeed[0],-currspeed[1])
                                        break
                                    if deepx<deepy:
                                        predictpos=(blocker_x+30,predictpos[1])
                                        currspeed=(-currspeed[0],currspeed[1])
                                        continue
                if side=="1P" and printmessage:
                    print(side+"end of situation 1")
            if (predictpos[1]+5)<=260 and currspeed[1]>0:
                #ball is coming but haven't pass the blocker
                if side=="1P" and printmessage:
                    print(side+"start of situation 2")
                lentoblocker=(239-(predictpos[1]+5))//currspeed[1]
                #239 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-(predictpos[0]+5))//currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)//currspeed[0]
                lentocollide=min(lentoside,lentoblocker)
                
                if (lentocollide+currframe)//100>currframe/100:
                    #speed up before collide
                    predictpos=vadd(predictpos,vscale(int((int(currframe/100)+1)*100-currframe),currspeed))
                    currframe=(currframe//100+1)*100
                    currspeed=speed_up(currspeed)
                    if side=="1P" and printmessage:
                        print(side+"situation 2 with speed up"+str(currframe)+" "+str(lentocollide))
                    continue
                else:
                    if lentoside<lentoblocker:
                        predictpos=vadd(predictpos,vscale((lentoside+1),currspeed))
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>195:
                            predictpos=(195,predictpos[1])
                        if predictpos[0]<0:
                            predictpos=(0,predictpos[1])
                        currspeed=(-currspeed[0],currspeed[1])
                        currframe=currframe+lentoside+1
                        if side=="1P" and printmessage:
                            print(side+"situation 2 with hit side")
                        continue
                    else:
                        if lentoblocker>0:
                            currframe=currframe+lentoblocker
                            predictpos=vadd(predictpos,vscale((lentoblocker),currspeed))
                            if predictpos[0]>195:
                                predictpos=(195,predictpos[1])
                            if predictpos[0]<0:
                                predictpos=(0,predictpos[1])
                        blocker_x=blocker_pos(currframe)
                        blocker_y=240
                        #it will collide in next frame so it need a width range
                        while (predictpos[1]+5)>=240-currspeed[1] and (predictpos[1]+5)<=260:
                            #guess the next position with check in next loop
                            predictpos=vadd(predictpos,currspeed)
                            if predictpos[0]>195:
                                predictpos=(195,predictpos[1])
                            if predictpos[0]<0:
                                predictpos=(0,predictpos[1])
                            currframe+=1
                            if currframe%100==0:
                                currspeed=speed_up(currspeed)

                            if predictpos[0]>blocker_x and predictpos[0]<blocker_x+30:
                                #modify if collide into blocker
                                deepy=blocker_y+20-predictpos[1]
                                if currspeed[0]>0:
                                    deepx=(predictpos[0]+5)-blocker_x
                                    if deepx==deepy:
                                        predictpos=(blocker_x,blocker_y+20)
                                        currspeed=vscale(-1,currspeed)
                                        break
                                        #bounce back
                                    if deepx>deepy:
                                        predictpos=(predictpos[0],blocker_y+20)
                                        currspeed=(currspeed[0],-currspeed[1])
                                        break
                                        #bounce back
                                    if deepx<deepy:
                                        predictpos=(blocker_x,predictpos[1])
                                        currspeed=(-currspeed[0],currspeed[1])
                                        continue
                                else:
                                    deepx=blocker_x+30-predictpos[0]
                                    if deepx==deepy:
                                        predictpos=(blocker_x+30,blocker_y+20)
                                        currspeed=vscale(-1,currspeed)
                                        break
                                    if deepx>deepy:
                                        predictpos=(predictpos[0],blocker_y+20)
                                        currspeed=(currspeed[0],-currspeed[1])
                                        break
                                    if deepx<deepy:
                                        predictpos=(blocker_x+30,predictpos[1])
                                        currspeed=(-currspeed[0],currspeed[1])
                                        continue
                if side=="1P" and printmessage:
                    print(side+"end of situation 2")
            if (predictpos[1]+5)>260 and currspeed[1]>0:
                #ball is coming and pass the blocker
                if side=="1P" and printmessage:
                    print(side+"start of situation 3")
                lentoboard=(419-(predictpos[1]+5))//currspeed[1]
                #419 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-(predictpos[0]+5))//currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)//currspeed[0]
                lentocollide=min(lentoside,lentoboard)
                
                if (lentocollide+currframe)//100>currframe//100:
                    #speed up before collide
                    predictpos=vadd(predictpos,vscale(int((int(currframe//100)+1)*100-currframe),currspeed))
                    currframe=(currframe//100+1)*100
                    currspeed=speed_up(currspeed)
                    if side=="1P" and printmessage:
                        print(side+"situation 3 with speed up"+str(currframe)+str(lentocollide))
                    continue
                else:
                    if lentoside<lentoboard:
                        predictpos=vadd(predictpos,vscale((lentoside+1),currspeed))
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>195:
                            predictpos=(195,predictpos[1])
                        if predictpos[0]<0:
                            predictpos=(0,predictpos[1])
                        currspeed=(-currspeed[0],currspeed[1])
                        currframe=currframe+lentoside+1
                        if side=="1P" and printmessage:
                            print("situation 3 with hit side")
                        continue
                    else:
                        predictpos=vadd(predictpos,vscale(lentoboard,currspeed))
                        if currspeed[0]>0:
                            predictpos=(predictpos[0]+(415-predictpos[1]),420)
                        else:
                            predictpos=(predictpos[0]-(415-predictpos[1]),420)
                        continue
                        #finish the prediction so predictpos won't be changed latter
                        if lentoside==lentoboard:
                            if predictpos[0]>195:
                                predictpos=(195,predictpos[1])
                            if predictpos[0]<0:
                                predictpos=(0,predictpos[1])
                            currspeed=(-currspeed[0],currspeed[1])
                            #check side squeeze if it also hit side
                        currframe=currframe+lentoboard
            if (predictpos[1]<240 and currspeed[1]<0):
                #ball is leaving and pass the blocker
                if side=="1P" and printmessage:
                    print(side+"start of situation 4")
                lentoboard=-(predictpos[1]-81)//currspeed[1]
                #81 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-(predictpos[0]+5))//currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)//currspeed[0]
                lentocollide=min(lentoside,lentoboard)
                
                if (lentocollide+currframe)//100>currframe//100:
                    #speed up before collide
                    predictpos=vadd(predictpos,vscale(int((int(currframe//100)+1)*100-currframe),currspeed))
                    currframe=(currframe//100+1)*100
                    currspeed=speed_up(currspeed)
                    continue
                else:
                    if lentoside<lentoboard:
                        predictpos=vadd(predictpos,vscale((lentoside+1),currspeed))
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>195:
                            predictpos=(195,predictpos[1])
                        if predictpos[0]<0:
                            predictpos=(0,predictpos[1])
                        currspeed=(-currspeed[0],currspeed[1])
                        currframe=currframe+lentoside+1
                        continue
                    else:
                        predictpos=vadd(predictpos,vscale(lentoboard,currspeed))
                        if currspeed[0]>0:
                            opponentpos=(predictpos[0]+(predictpos[1]-80),80)
                        else:
                            opponentpos=(predictpos[0]-(predictpos[1]-80),80)
                        currspeed=(currspeed[0],-currspeed[1])
                        #suppost its velocity is k(+-1,+-1)
                        if lentoside==lentoboard:
                            if predictpos[0]>195:
                                predictpos=(195,predictpos[1])
                            if predictpos[0]<0:
                                predictpos=(0,predictpos[1])
                            currspeed=(-currspeed[0],currspeed[1])
                            #check side squeeze if it also hit side
                        currframe=currframe+lentoboard
                if side=="1P" and printmessage:
                    print("end ot situation 4")
    #predict end function end

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        
        
        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        if ball_served:
            if scene_info["frame"]==1:
                blocker1=scene_info["blocker"]
            elif scene_info["frame"]==2:
                blocker2=scene_info["blocker"]
                blockerdirect=blocker2[0]-blocker1[0]
        
            if side == "2P":
                scene_info["ball"]=(scene_info["ball"][0],500-scene_info["ball"][1])
                scene_info["ball_speed"]=(scene_info["ball_speed"][0],-scene_info["ball_speed"][1])
                temp=scene_info["platform_1P"]
                scene_info["platform_1P"]=scene_info["platform_2P"]
                scene_info["platform_2P"]=temp

            #default predict_path function parameter
            predictpos=(scene_info["ball"][0]+scene_info["ball_speed"][0],scene_info["ball"][1]+scene_info["ball_speed"][1])
            currspeed=scene_info["ball_speed"]
            currframe=scene_info["frame"]
            opponentpos=(0,0)
            if side=="1P":
                print("start predict")
                print("speed="+str(currspeed))
                print("currframe="+str(currframe))
            predict_path()
            if side=="1P":
                print("finish predict--------------------------------------------")
                print("predictpos="+str(predictpos))
                print("opponenpos="+str(opponentpos))
                print("currentpos="+str(scene_info["ball"]))
                print("currframe="+str(currframe))
            #if scene_info["ball"][1]+scene_info["ball_speed"]<420 or scene_info["platform_1P"][0]>predictpos[0]-5 or scene_info["platform_1P"][0]<predictpos[0]+30:
                #without consider how to cut    
            if scene_info["platform_1P"][0]>predictpos[0]-5:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            elif scene_info["platform_1P"][0]<predictpos[0]-20:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            #else:
            
        
        """
        predictpos=(scene_info["ball"][0]+scene_info["ball_speed"][0],scene_info["ball"][1]+scene_info["ball_speed]"][1])
        currspeed=scene_info["ball_speed"]
        currframe=scene_info["frame"]
        opponentpos=(0,0)        
        while predictpos[1]<419:
            if predictpos[1]<420 and predictpos[1]>=240:  
                # Ball is leaving but not pass the blocker

                lentoblocker=-(predictpos[1]-261)/currspeed[1]
                    #261 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-predictpos[0])/currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)/currspeed[0]
                lentocollide=min(lentoside,lentoblocker)
                
                if (lentocollide+frame)/100>frame/100:
                    #speed up before collide
                    predictpos=predictpos+((currframe/100+1)*100-currframe)*currspeed
                    currframe=(frame/100+1)*100
                    currspeed=currspeed+[1,1]
                    continue
                else:
                    if lentoside<lentoblocker:
                        predictpos=predictpos+(lentoside+1)*currspeed
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>200:
                            predictpos=200
                        if predictpos[0]<0:
                            predictpos=0
                        currspeed[0]=-currspeed[0]
                        currframe=currframe+lentoside+1
                        continue
                    else:
                        if lentoblocker>0:
                            currframe=currframe+lentoblocker
                            predictpos=predictpos+(lentoblocker)*currspeed
                            if predictpos[0]>200:
                                predictpos[0]=200
                            if predictpos[0]<0:
                                predictpos[0]=0
                            blocker_x=blocker_pos(currframe)
                            blocker_y=240
                        #it will collide in next frame so it need a width range
                        while predictpos[1]>=240 and predictpos[1]<=260-currspeed[1]:
                            #guess the next position with check in next loop
                            predictpos=predictpos+currspeed
                            if predictpos[0]>200:
                                predictpos[0]=200
                            if predictpos[0]<0:
                                predictpos[0]=0
                            currframe+=1
                            if currframe%100=0:
                                currspeed=currspeed+[1,1]

                            if predictpos[0]>blocker_x and predictpos[0]<blocker_x+30:
                                #modify if collide into blocker
                                deepy=blocker_y+20-predictpos[1]
                                if currspeed[0]>0:
                                    deepx=predictpos[0]-blocker_x
                                    if deepx==deepy:
                                        predictpos[0]=blocker_x
                                        predictpos[1]=blocker_y+20
                                        currspeed=-currspeed
                                        break
                                        #bounce back
                                    if deepx>deepy:
                                        predictpos[1]=blocker_y+20
                                        currspeed[1]=-currspeed[1]
                                        break
                                        #bounce back
                                    if deepx<deepy:
                                        predictpos[0]=blocker_x
                                        currspeed[0]=-currspeed[0]
                                        continue
                                else:
                                    deepx=blocker_x+30-predictpos[0]
                                    if deepx==deepy:
                                        predictpos[0]=blocker_x+30
                                        predictpos[1]=blocker_y+20
                                        currspeed=-currspeed
                                        break
                                    if deepx>deepy:
                                        predictpos[1]=blocker_y+20
                                        currspeed[1]=-currspeed[1]
                                        break
                                    if deepx<deepy:
                                        predictpos[0]=blocker_x+30
                                        currspeed[0]=-currspeed[0]
                                        continue
            if predictpos[1]<=260 and currspeed[1]>0:
                #ball is coming but haven't pass the blocker
                lentoblocker=(239-predictpos[1])/currspeed[1]
                #239 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-predictpos[0])/currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)/currspeed[0]
                lentocollide=min(lentoside,lentoblocker)
                
                if (lentocollide+frame)/100>frame/100:
                    #speed up before collide
                    predictpos=predictpos+((currframe/100+1)*100-currframe)*currspeed
                    currframe=(frame/100+1)*100
                    currspeed=currspeed+[1,1]
                    continue
                else:
                    if lentoside<lentoblocker:
                        predictpos=predictpos+(lentoside+1)*currspeed
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>200:
                            predictpos=200
                        if predictpos[0]<0:
                            predictpos=0
                        currspeed[0]=-currspeed[0]
                        currframe=currframe+lentoside+1
                        continue
                    else:
                        if lentoblocker>0:
                            currframe=currframe+lentoblocker
                            predictpos=predictpos+(lentoblocker)*currspeed
                            if predictpos[0]>200:
                                predictpos[0]=200
                            if predictpos[0]<0:
                                predictpos[0]=0
                            blocker_x=blocker_pos(currframe)
                            blocker_y=240
                        #it will collide in next frame so it need a width range
                        while predictpos[1]>=240-currspeed[1] and predictpos[1]<=260:
                            #guess the next position with check in next loop
                            predictpos=predictpos+currspeed
                            if predictpos[0]>200:
                                predictpos[0]=200
                            if predictpos[0]<0:
                                predictpos[0]=0
                            currframe+=1
                            if currframe%100=0:
                                currspeed=currspeed+[1,1]

                            if predictpos[0]>blocker_x and predictpos[0]<blocker_x+30:
                                #modify if collide into blocker
                                deepy=blocker_y+20-predictpos[1]
                                if currspeed[0]>0:
                                    deepx=predictpos[0]-blocker_x
                                    if deepx==deepy:
                                        predictpos[0]=blocker_x
                                        predictpos[1]=blocker_y+20
                                        currspeed=-currspeed
                                        break
                                        #bounce back
                                    if deepx>deepy:
                                        predictpos[1]=blocker_y+20
                                        currspeed[1]=-currspeed[1]
                                        break
                                        #bounce back
                                    if deepx<deepy:
                                        predictpos[0]=blocker_x
                                        currspeed[0]=-currspeed[0]
                                        continue
                                else:
                                    deepx=blocker_x+30-predictpos[0]
                                    if deepx==deepy:
                                        predictpos[0]=blocker_x+30
                                        predictpos[1]=blocker_y+20
                                        currspeed=-currspeed
                                        break
                                    if deepx>deepy:
                                        predictpos[1]=blocker_y+20
                                        currspeed[1]=-currspeed[1]
                                        break
                                    if deepx<deepy:
                                        predictpos[0]=blocker_x+30
                                        currspeed[0]=-currspeed[0]
                                        continue
            if (predictpos[1]>260 and currspeed[1]>0):
                #ball is coming and pass the blocker
                lentoboard=(419-predictpos[1])/currspeed[1]
                #419 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-predictpos[0])/currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)/currspeed[0]
                lentocollide=min(lentoside,lentoboard)
                
                if (lentocollide+frame)/100>frame/100:
                    #speed up before collide
                    predictpos=predictpos+((currframe/100+1)*100-currframe)*currspeed
                    currframe=(frame/100+1)*100
                    currspeed=currspeed+[1,1]
                    continue
                else:
                    if lentoside<lentoboard:
                        predictpos=predictpos+(lentoside+1)*currspeed
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>200:
                            predictpos=200
                        if predictpos[0]<0:
                            predictpos=0
                        currspeed[0]=-currspeed[0]
                        currframe=currframe+lentoside+1
                        continue
                    else:
                        predictpos=predictpos+lentoboard*currspeed
                        if currspeed[0]>0:
                            predictpos[0]=predictpos[0]+(420-predictpos[1])
                        else:
                            predictpos[0]=predictpos[0]-(420-predictpos[1])
                        predictpos[1]=420
                        if lentoside==lentoboard:
                            if predictpos[0]>200:
                                predictpos=200
                            if predictpos[0]<0:
                                predictpos=0
                            currspeed[0]=-currspeed[0]
                            #check side squeeze if it also hit side
                        currframe=currframe+lentoboard
            if (predictpos[1]<240 and currspeed[1]<0):
                #ball is leaving and pass the blocker
                lentoboard=-(predictpos[1]-81)/currspeed[1]
                #81 because pos always +speed*(lentoblocker+1) even remind=0
                if currspeed[0]>0:
                    lentoside=(199-predictpos[0])/currspeed[0]
                    #199 because pos always +speed*(lentoside+1) even remind=0
                else:
                    lentoside=-(predictpos[0]-1)/currspeed[0]
                lentocollide=min(lentoside,lentoboard)
                
                if (lentocollide+frame)/100>frame/100:
                    #speed up before collide
                    predictpos=predictpos+((currframe/100+1)*100-currframe)*currspeed
                    currframe=(frame/100+1)*100
                    currspeed=currspeed+[1,1]
                    continue
                else:
                    if lentoside<lentoboard:
                        predictpos=predictpos+(lentoside+1)*currspeed
                        #plus 1 than ball will squeeze into wall
                        if predictpos[0]>200:
                            predictpos=200
                        if predictpos[0]<0:
                            predictpos=0
                        currspeed[0]=-currspeed[0]
                        currframe=currframe+lentoside+1
                        continue
                    else:
                        predictpos=predictpos+lentoboard*currspeed
                        if currspeed[0]>0:
                            opponentpos[0]=predictpos[0]+(420-predictpos[1])
                        else:
                            opponentpos[0]=predictpos[0]-(420-predictpos[1])
                        predictpos[1]=80
                        if lentoside==lentoboard:
                            if predictpos[0]>200:
                                predictpos=200
                            if predictpos[0]<0:
                                predictpos=0
                            currspeed[0]=-currspeed[0]
                            #check side squeeze if it also hit side
                        currframe=currframe+lentoboard
        """
        
        
        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        #else:
        #    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
