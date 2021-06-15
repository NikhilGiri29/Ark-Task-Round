# Make a copy of this file
# and Add a class called AI Agent 

import sys
from random import randrange
from typing import List
import numpy as np
from gym_tictactoe.envs.tictactoe_env import TicTacToeEnv, after_action_state, check_game_status, agent_by_mark

world = np.zeros((3,3,3))
ALoc = [-9,-9,-9]

def is_empty(world):
    flag  = True
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if(world[i][j][k] !=0):
                    flag = False
    return flag

def is_full(world):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if(world[i][j][k] ==0):
                    return  False
    return True


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
        if is_empty(world):
            block = randrange(3)
            row  = randrange(3)
            col  = randrange(3)
            action = str(block) + str(col) + str (row)
            world[int(block)][int(row)][int(col)] = int(self.mark)
            return self.mark + action
        else:
            a  = findBestMove(int(self.mark))
            print("A is  : ", a)
            world[int(ALoc[0])][int(ALoc[1])][int(ALoc[2])] = int(self.mark)
            action = str(ALoc[0]) + str(ALoc[2]) + str (ALoc[1])
        return self.mark + action
   

def minimax(level, player_mark : int, is_max : bool, alpha, beta):
    global world
    #if level > 5 : 
        #return 0
   #print(level)
    opponent_mark = 2/player_mark
    #check if the previous move ended the game
    state = check_game_status(world)
    if state != -1:
        if is_max : ai_mark = player_mark 
        else : ai_mark = opponent_mark

        if state == ai_mark :
            #print("Well this is awkward")
            return 100 -(level*10)
        if state == 2/ai_mark :
            return -100 + (level*10)

    if is_full(world) and state == -1 :
        return 0   #board full , there is a tie
    if level > 2 : 
        return 0
    if is_max:
        value = -1000
        for i in range(3):
            for j in range(3):
                for k in range(3) : 
                    if world [i,j,k] ==0:
                        world[i,j,k] = player_mark
                        value = max(value,minimax(level+1,opponent_mark,False,alpha,beta))
                        alpha = max(alpha,value)
                        world[i,j,k] = 0

                        if beta < alpha:
                            break

    else: 
        value = 1000
        for i in range(3):
            for j in range(3):
                for k in range(3) : 
                    if world [i,j,k] ==0:
                        world[i,j,k] = player_mark
                        value = min(value,minimax(level+1,opponent_mark,True,alpha,beta))
                        beta = min(beta,value)
                        world[i,j,k] = 0
                        if beta < alpha:
                            break
    return value


def findBestMove(player_mark) :
    global world
    best_move = -10000
    global ALoc

    for i in range(3):
        for j in range(3):
            for k in range(3) :
                if (world[i,j,k] == 0) :
                    world[i,j,k] = player_mark
                    value = minimax(0, (2/player_mark), False, -1000000,1000000)
                
                    world[i,j,k] = 0

                    if (value > best_move) :               
                        ALoc = [i,j,k]
                        best_move = value
    return best_move

 
agents = [HumanAgent('1'),AI('2')]



def play():
    global world
    global ava_actions

    env = TicTacToeEnv()
    
    global agents 

    episode = 0
    done = False
    while not done:
        marko = str(env.show_turn())
        agent = agent_by_mark(agents, marko)
        print(agent.mark)
        ava_actions = env.available_actions()
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