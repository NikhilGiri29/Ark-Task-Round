# 3D Tic Tac Toe Game in OpenAI Gym
The 3D version of Tic Tac Toe is implemented as an OpenAI's Gym environment.

## Complexity
The traditional (2D) Tic Tac Toe has a very small game space (3^9). In comparison, the 3D version in this repo has a much larger space which is in the order of 3^27 or 7.6 trillion states. This makes computer-based players using search and pruning techniques of the game space prohibitively expensive.

## Contributions
The repo is also open for pull requests and collaborations both in game development as well as learning.

## Dependencies
- Base dependency: `gym`.
- Plot-rendering dependencies: `numpy`, `matplotlib`.
- DQN learning dependencies: `tensorflow`, `numpy`.

## Installation
To install run:
```console
git clone https://github.com/Cypre55/gym-tictactoe3d.git
cd gym-tictactoe3d
pip install -e .
```

## Usage

Look at  `example.py` for skeleton code. 

Currently 1 type of environment with textual rendering.

### Textual rendering
To use textual rendering create environment as `tictactoe-v0` like so:
```python
import gym
import gym_tictactoe

def play_game(actions, step_fn=input):
  env = gym.make('tictactoe-v0')
  env.reset()
  
  # Play actions in action profile
  for action in actions:
    print(env.step(action))
    env.render()
    if step_fn:
      step_fn()
  return env

actions = ['1021', '2111', '1221', '2222', '1121']
_ = play_game(actions, None)
```
The output produced is:

```
Step 1:
- - -    - - -    - - -    
- - x    - - -    - - -    
- - -    - - -    - - -    

Step 2:
- - -    - - -    - - -    
- - x    - o -    - - -    
- - -    - - -    - - -    

Step 3:
- - -    - - -    - - -    
- - x    - o -    - - x    
- - -    - - -    - - -    

Step 4:
- - -    - - -    - - -    
- - x    - o -    - - x    
- - -    - - -    - - o    

Step 5:
- - -    - - -    - - -    
- - X    - o X    - - X    
- - -    - - -    - - o   
```
The winning sequence after gameplay: `(0,2,1), (1,2,1), (2,2,1)`.



