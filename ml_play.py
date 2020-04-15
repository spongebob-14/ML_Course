"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import (
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """





    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    direct=(-7,-7)  
    directo=(-7,-7)    
    curro_ball=(93,395)  #current position
    curr_ball=(93,395)  
    prev_ball=(93+7,395+7)  #previous position
    pred_ball=(93,395)  #predict position
    pos_array=[]
    has_fine=0
    pred_position=(75,400)

    prev_brick_num=0

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        curro_ball=scene_info.ball
        

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if (scene_info.status == GameStatus.GAME_OVER or
            scene_info.status == GameStatus.GAME_PASS):
            # Do some stuff if needed
            ball_served = False

            direct=(-7,-7)  
            directo=(-7,-7)    
            curro_ball=(93,395)  #current position
            curr_ball=(93,395)  
            prev_ball=(93+7,395+7)  #previous position
            pred_ball=(93,395)  #predict position
            pos_array=[]
            has_fine=0
            pred_position=(75,400)

            prev_brick_num=0




            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            

            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            continue
        """
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        """
        print(scene_info.frame)
        print('current position=',end='')
        print(curro_ball)
        print('brick num=',end='')
        print(len(scene_info.bricks))
        # runtime

        #"""
        if abs(curro_ball[0]-prev_ball[0])>=10 or abs(curro_ball[1]-prev_ball[1])>=10: 
            # speed up case
            # if it's wrong(speed up and squeezed both happen)
            # it may be recover in next frame(?) 
            if curro_ball[0]-prev_ball[0]>0:
                directo=(10,directo[1])
            else:
                directo=(-10,directo[1])
            if curro_ball[1]-prev_ball[1]>0:
                directo=(directo[0],10)
            else:
                directo=(directo[0],-10)
        else:
            # been squeezed
            if curro_ball[0]!=prev_ball[0]+directo[0]:  
                directo=(-directo[0],directo[1])
            if curro_ball[1]!=prev_ball[1]+directo[1]:  
                directo=(directo[0],-directo[1])
        """
        directo=(curro_ball[0]-prev_ball[0],curro_ball[1]-prev_ball[1])
        """

        if len(pos_array)<1 or curro_ball==pos_array[len(pos_array)-1]: #move to the predict point
            #need new prediction
            #=(curro_ball[0]-prev_ball[0],curro_ball[1]-prev_ball[1])
        #if prev_brick_num!=len(scene_info.bricks):
            
            print('need new prediction')
            has_fine=0
            direct=directo  #direct inside loop is changed during predict
            curr_ball=curro_ball    #if it's a new prediction use new data

        print('predict direct=',end='')
        print(direct)
        
        

        while has_fine==0:
            """
            print(scene_info.frame,end='')
            print(curr_ball,end='')
            print(pred_ball,end='')
            if curr_ball[0]!=pred_ball[0] or curr_ball[1]!=pred_ball[1]:
                print("predict fall!!!")
            else:
                print("predict success")
            """
            if len(pos_array)>=1:
                # it must be data from previous frame if array is not empty
                # and the first one is the pevious position
                # clear it for better visualization
                pos_array.pop(0)

            for i in range(100):        #prevent predict to much in one frame
                

                pos_array.append(curr_ball)
                #if len=0 mean starting use curro
                #else it will use the last data in previous array
                #which has been save in previous loop

                h_c=0   
                v_c=0   #vertical changed or not

                pred_ball=(curr_ball[0]+direct[0],curr_ball[1]+direct[1])
                
                if pred_ball[0]<=0:
                    pred_ball=(0,pred_ball[1])
                    direct=(-direct[0],direct[1])
                    h_c=1
        
                if pred_ball[0]+5>=200:
                    pred_ball=(200-5,pred_ball[1])
                    direct=(-direct[0],direct[1])
                    h_c=1

                if pred_ball[1]<=0:
                    pred_ball=(pred_ball[0],0)
                    direct=(direct[0],-direct[1])
                    v_c=1
        
                if pred_ball[1]+5>=400:      # in case ball hit platform
                    pred_ball=(pred_ball[0],400-5)
                    direct=(direct[0],-direct[1])
                    v_c=1
                    curr_ball=pred_ball
                    pred_position=(pred_ball[0]-17.5,pred_position[1])
                    print('predict falling pos=',end='')
                    print(pred_ball)
                    print('predict array=')
                    print(pos_array[0:5])

                    pos_array=[]
                    #pos_array.append(pred_ball)

                    has_fine=1
                    break                   
                    #jump out the for loop
                    #leave pos_array empty
                    # can get new data when starting next predict 
        
        
                for brick_pos in scene_info.bricks:
                    if pred_ball[0]+5>brick_pos[0] and pred_ball[0]<brick_pos[0]+25 and pred_ball[1]+5>brick_pos[1] and pred_ball[1]<brick_pos[1]+10:
                        from_up=pred_ball[1]+5-brick_pos[1]
                        from_down=brick_pos[1]+10-pred_ball[1]
                        from_left=pred_ball[0]+5-brick_pos[0]
                        from_right=brick_pos[0]+25-pred_ball[0]
                        if direct[0]==-7 and direct[1]==-7:        #lu
                            if from_right<from_down:           #from right
                                pred_ball=(brick_pos[0]+25,pred_ball[1])
                                direct=(-direct[0],direct[1])
                            else:                              #from down
                                pred_ball=(pred_ball[0],brick_pos[1]+10)  
                                direct=(direct[0],-direct[1])  
                        elif direct[0]==7 and direct[1]==-7:  #ru
                            if from_left<from_down:            #from left
                                pred_ball=(brick_pos[0]-5,pred_ball[1])
                                direct=(-direct[0],direct[1])
 
                            else:                             #from down
                                pred_ball=(pred_ball[0],brick_pos[1]+10)  
                                direct=(direct[0],-direct[1])  
                        elif direct[0]==7 and direct[1]==7:   #rd
                            if from_left<from_up:              ##from left
                                pred_ball=(brick_pos[0]-5,pred_ball[1])
                                direct=(-direct[0],direct[1])
                            else:                              #from up
                                pred_ball=(pred_ball[0],brick_pos[1]-5)
                                direct=(direct[0],-direct[1])
                        elif direct[0]==-7 and direct[1]==7:   ##ld
                            if from_right<from_up:             #from right
                                pred_ball=(brick_pos[0]+25,pred_ball[1])
                                direct=(-direct[0],direct[1])
                            else:                              #from up
                                pred_ball=(pred_ball[0],brick_pos[1]-5)
                                direct=(direct[0],-direct[1])
                #prev_ball=curr_ball
                curr_ball=pred_ball

            if i>=50 and has_fine==0:
                print('predict array=')
                print(pos_array[0:5])
                print('too far to predict')
                break;  #while loop

        prev_brick_num=len(scene_info.bricks)
            #pos_array=[]
            #pos_array.append(curr_ball)
        prev_ball=curro_ball

        if has_fine==0 or scene_info.ball[1]>=395:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        elif scene_info.platform[0]>pred_position[0]+16:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif scene_info.platform[0]<pred_position[0]-16:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            
        # runtime