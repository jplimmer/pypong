# PyPong 🐍🏓

This is a version of the popular game Pong designed for two human players. It is built in Python using object-oriented programming.

<img src="images/pypong_demo.gif" width="70%">

## Contents
1. [Installation](#installation)
2. [Gameplay](#gameplay)
3. [Future development](#future-development)

## Installation
#### Using [environment.yml](environment.yml) (recommended)

1. Clone the repository and navigate to the project directory:
```
git clone https://github.com/jplimmer/pypong.git
cd pypong
```
2. Create conda environment from `environment.yml`:
```
conda env create -f environment.yml
```
3. Activate the environment and run the python file:
```
conda activate pypong
python pypong.py
```

## Gameplay
The screen is divided into 2 halves by a net, with Player 1's paddle on the far left and Player 2's paddle on the far right.

<img src="images/pypong_screenshot.png" width="70%">

At the start of each point the ball will begin moving from a random point on the net in a random direction. The ball will bounce off the top and bottom of the screen, and each player has to move their paddle to hit the ball back towards the opponent. If the ball goes off the left or right hand edge of the screen, the point is over.  

Each player has an up and down key to control their respective paddles. The paddles have 5 speed settings which can be adjusted with more presses of the direction key:
- Player 1 = W/S
- Player 2 = Up/Down

The winner is the first player to score 11 points (with a winning margin of 2).

## Future development
- Add angle variation after paddle hit. 
- Add user configuration options:
  - colour themes
  - winning score
  - reassign control keys
- Difficulty levels:
  - paddle size
  - ball speeds
- Add legend to display controls