# Make a copy of this file
# and Add a class called AI Agent 

import sys
from random import randrange
import numpy as np
from gym_tictactoe.envs.tictactoe_env import TicTacToeEnv, after_action_state, check_game_status, agent_by_mark

world = np.zeros((3,3))
ALoc = [-9,-9]

def is_empty(world):
    flag  = True
    for i in range(3):
        for j in range(3):
            if(world[i][j] !=0):
                flag = False
    return flag

def is_full(world):
    flag  = True
    for i in range(3):
        for j in range(3):
            if(world[i][j] ==0):
                flag = False
    return flag

def game_over(world,player_mark) :
   

    for row in range(3) :    
        if (world[row][0] == world[row][1] and world[row][1] == world[row][2] and world[row][0] != 0) :       
            if (world[row][0] == player_mark) :
                return 10
            else:
                return -10

    for col in range(3) :
      
        if (world[0][col] == world[1][col] and world[1][col] == world[2][col]  and world[0][col] != 0) :
         
            if (world[0][col] == player_mark) :
                return 10
            else:
                return -10
    
    if (world[0][0] == world[1][1] and world[1][1] == world[2][2]  and world[1][1] != 0) :
     
        if (world[0][0] == player_mark) :
            return 10
        else:
            return -10
 
    if (world[0][2] == world[1][1] and world[1][1] == world[2][0]  and world[1][1] != 0) :
     
        if (world[0][2] == player_mark) :
            return 10
        else:
            return -10

    return 0


class HumanAgent(object):
    global world
    
    def __init__(self, mark):
        self.mark = mark

    def act(self, ava_actions,world):
        while True:
            row  = input("Please Enter the row number(type q to quit):")
            if row == 'q':
                return None
            col  = input("Please Enter the column number(type q to quit):")
            if col == 'q':
                return None
            uloc = '0' + str(col) + str (row)
            world[int(row)][int(col)] = int(self.mark)
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
            row  = randrange(3)
            col  = randrange(3)
            action = '0' + str(col) + str (row)
            world[int(row)][int(col)] = int(self.mark)
            return self.mark + action
        else:
            a  = minimax(0,int(self.mark),True)
            print("A is  : ", a)
            world[int(ALoc[0])][int(ALoc[1])] = int(self.mark)
            action = '0' + str(ALoc[1]) + str (ALoc[0])
        return self.mark + action
    '''
    def minimax(self,world,level, player_mark : int, is_max : bool):
        global ALoc
        opponent_mark = 2/player_mark
        #check if the previous move ended the game
        if is_max : score = game_over(world,player_mark)
        else : score = game_over(world,opponent_mark)

        if score ==10 :
            return 100 -(level*10)
        if score ==-10 :
            return -100 + (level*10)

        if is_full(world):
            return 0   #board full , there is a tie
        value = 20
        if is_max:
            value = -10000000
            for i in range(3):
                for j in range(3):
                    if world [i,j] ==0:
                        world[i,j] = player_mark

                        x = AI.minimax(self,world,level+1,opponent_mark,False)
                        if x > value :
                            value = x
                            ALoc[0] , ALoc[1] = i,j

                        world[i,j] = 0
        
        else: 
            value = 10000000
            for i in range(3):
                for j in range(3):
                    if world [i,j] ==0:
                        world[i,j] = player_mark
                        x = AI.minimax(self,world,level+1,opponent_mark,True)
                        if x < value :
                            value = x
                            ALoc[0] , ALoc[1] = i,j
                        world[i,j] = 0
        return value
    '''
stats = np.zeros((3,3))

def minimax(level, player_mark : int, is_max : bool):
    global world
    global ALoc
    global stats
    
    level_count = []
    i_count=[]
    j_count= []
    opponent_mark = 2/player_mark
    #check if the previous move ended the game
    if is_max : score = game_over(world,player_mark)
    else : score = game_over(world,opponent_mark)

    if score ==10 :
        return 100 -(level*10)
    if score ==-10 :
        return -100 + (level*10)

    if is_full(world) and score ==0 :
        return 0   #board full , there is a tie
    
    if is_max:

        for i in range(3):
            for j in range(3):
                if world [i,j] ==0:
                    world[i,j] = player_mark
                    x = minimax(level+1,opponent_mark,False)
                    if level ==0:
                        stats[i,j] = x 
                    
                    level_count.append(x)
                    i_count.append(i)
                    j_count.append(j)
                    
                    world[i,j] = 0
        
    else: 
        
        for i in range(3):
            for j in range(3):
                if world [i,j] ==0:
                    world[i,j] = player_mark
                    x = minimax(level+1,opponent_mark,True)

                    level_count.append(x)
                    i_count.append(i)
                    j_count.append(j)
                    world[i,j] = 0

    print(level_count)
    if is_max:
        value = max(level_count)
        index = level_count.index(value)
        ALoc = [i_count[index],j_count[index]]
    else:
        value = min(level_count)
        index = level_count.index(value)
        ALoc = [i_count[index],j_count[index]]

    if level ==0:
        print("###")
        print(stats)

    return value

agents = [HumanAgent('1'),AI('2')]

def play():
    global world

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