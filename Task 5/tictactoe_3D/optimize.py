# Make a copy of this file
# and Add a class called AI Agent 

import sys
from random import randrange
from typing import List
import numpy as np
from gym_tictactoe.envs.tictactoe_env import TicTacToeEnv, after_action_state, check_game_status, agent_by_mark

world = np.zeros((3,3,3))
ALoc = [-9,-9,-9]
ava_actions = []
env = TicTacToeEnv()

def is_full(world):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if(world[i][j][k] ==0):
                    return  False
    return True

def esti_point(a,b,c,player_mark):
    basic_point =0
    values = [a,b,c]
    for i in values:
        if i == player_mark:
            basic_point +=10
        elif i !=0 :
            basic_point -=10
    return basic_point

def estimate(world,player_mark):
    points = 0
    for b in range(3):
        
        for c in range(3):
            points += esti_point(world[b,0,c],world[b,1,c],world[b,2,c],player_mark)
            
        for r in range(3):
            points += esti_point(world[b,r,0],world[b,r,1],world[b,r,2],player_mark)

        points += esti_point(world[b, 0, 0],world[b, 1, 1], world[b, 2, 2], player_mark)
        

        points += esti_point(world[b, 0, 2],world[b, 1, 1],world[b, 2, 0], player_mark)

    for r in range(3):

        for c in range(3):
            points += esti_point(world[0,c, r],world[1,c, r], world[2,c ,r], player_mark)

        points += esti_point(world[0, 0,r],world[1, 1,r], world[2, 2,r], player_mark)

        points += esti_point(world[0, 2,r],world[1, 1,r],world[2, 0 ,r], player_mark)
    
    for c in range(3):

        points += esti_point(world[0,c, 0],world[1,c, 1], world[2,c ,2], player_mark)

        points += esti_point(world[0,r, 2],world[1,c, 1],world[2 ,c, 0], player_mark)


    points += esti_point(world[0, 0, 0], world[1, 1, 1],world[2, 2, 2], player_mark)
        
    points += esti_point(world[0, 2, 0], world[1, 1, 1],world[2, 0, 2], player_mark)
       
    points += esti_point(world[0, 0, 2], world[1, 1, 1],world[2, 2, 0], player_mark)
    
    points += esti_point(world[0, 2, 2], world[1, 1, 1],world[2, 0, 0], player_mark)
        
    return points


class HumanAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, ava_actions,world):
        while True:
            block= input("Please Enter the block(layer) number(type q to quit):")
            if block == 'q':
                return None
            row  = input("Please Enter the row number(type q to quit):")
            if row == 'q':
                return None
            col  = input("Please Enter the column number(type q to quit):")
            if col == 'q':
                return None
            uloc = str(block) + str(col) + str (row)
            world[int(block)][int(row)][int(col)] = int(self.mark)
            try:
                action = uloc
                if action not in ava_actions:
                    raise ValueError()
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return self.mark + action

class AI(object):
    global world
    def __init__(self,mark):
        self.mark = mark       

    def act(self, ava_actions,world):
        if len(ava_actions) >25:
            #if it is first or second turn
            #applying the forced move concept
            if(world[1,1,1] ==0):
                #check if the centre block is empty, if so then take that move
                world[1,1,1] =self.mark
                return self.mark + "111"
            else:
                #if centre is filled i.e the opponents first move is centre
                #then move at corner of block 0 and 1 is the optimal move
                block = randrange(2)*2
                row  = randrange(2)*2
                col  = randrange(2)*2
                action = str(block) + str(col) + str (row)
                world[int(block)][int(row)][int(col)] = int(self.mark)
                return self.mark + action
        else:
            a  = findBestMove(int(self.mark))
            world[int(ALoc[0])][int(ALoc[1])][int(ALoc[2])] = int(self.mark)
            action = str(ALoc[0]) + str(ALoc[2]) + str (ALoc[1])
        return self.mark + action
   

def minimax(level, player_mark : int, is_max : bool, alpha, beta):
    global world
    #print(level)
    opponent_mark = 2/player_mark
    #check if the previous move ended the game
    state = check_game_status(world)
    if state != -1:
        if is_max : ai_mark = player_mark 
        else : ai_mark = opponent_mark

        if state == ai_mark :
            #print("Well this is awkward")
            return 1000 -(level*10)
        if state == 2/ai_mark :
            return -1000 + (level*10)

    if is_full(world) and state == -1 :
        return 0   #board full , there is a tie
    if level > 2 : 
        if is_max : return estimate(world,player_mark)
        else : return estimate(world,opponent_mark)

    acto = TicTacToeEnv.available_actions(env, world)

    if is_max:
        value = -100000
        for _action in acto :    
            _loc = (list((_action)))
            i =(int)(_loc[0])
            j= (int)(_loc[1])
            k = (int)(_loc[2])

            world[i,j,k] = player_mark
            value = max(value,minimax(level+1,opponent_mark,False,alpha,beta))
            alpha = max(alpha,value)
            world[i,j,k] = 0

            if beta < alpha:
                break

    else: 
        value = 100000
        for _action in acto :    
            _loc = (list((_action)))
            i =(int)(_loc[0])
            j= (int)(_loc[1])
            k = (int)(_loc[2])
            
            world[i,j,k] = player_mark
            value = min(value,minimax(level+1,opponent_mark,True,alpha,beta))
            beta = min(beta,value)
            world[i,j,k] = 0
            if beta < alpha:
                break
    return value


def findBestMove(player_mark) :
    global ava_actions
    global world
    best_move = -10000
    global ALoc

    for _action in ava_actions :    
        _loc = (list((_action)))
        i =(int)(_loc[0])
        j= (int)(_loc[1])
        k = (int)(_loc[2])
        world[i,j,k] = player_mark
        value = minimax(0, (2/player_mark), False, -1000000,1000000)
    
        world[i,j,k] = 0

        if (value > best_move) :               
            ALoc = [i,j,k]
            best_move = value
    return best_move

 
agents = [AI('1'),AI('2')]



def play():
    global world
    global ava_actions
    global env
    
    global agents 

    episode = 0
    done = False
    while not done:
        marko = str(env.show_turn())
        agent = agent_by_mark(agents, marko)
        print(agent.mark)
        ava_actions = env.available_actions(world)
        action = agent.act(ava_actions,world)
        print(action)
        '''
        print("######################")
        print(world)
        print("######################")
        '''

        if action is None:
            sys.exit()

        state, reward, done, info = env.step(action)

        print()
        env.render()
        if done:
            env.show_result()
            break
    episode += 1


if __name__ == '__main__':
    play()