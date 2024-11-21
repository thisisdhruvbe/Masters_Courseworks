VIDEO PRESENTATION link:
https://www.youtube.com/watch?v=_ACbtuY10ec


This repository contains the Python scripts for a Q-learning based autonomous agent designed to play and master the Snake game. Each script serves a specific role, from managing the game environment to implementing the Q-learning algorithm, automating experiments, and visualizing results. The project demonstrates how reinforcement learning techniques can be applied to a classic game, offering insights into AI training dynamics and decision-making processes

1. Snake.py
Functionality:
    -Manages the Snake game logic including snake movements, food generation, and collision detection.
    -Updates game state and renders the game board.
2. QLearning_new.py
Functionality:
    -Implements the Q-learning algorithm for the Snake game.
    -Manages the Q-table for storing and updating Q-values.
    -Facilitates decision-making and visualizes learning progress.
3. experiments.py
Functionality:
    -Automates multiple game simulations with varying Q-learning parameters.
    -Records game performance data (scores, snake length) into a CSV file for analysis.
4. plot_experiments.py
Functionality:
    -Reads performance data from the CSV file.
    -Generates visualizations using matplotlib to illustrate learning effectiveness across different settings


