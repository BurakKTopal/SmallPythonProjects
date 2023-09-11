import numpy as np
from collections import deque
from PongAI.Model import *
import random
WIDTH = 600
HEIGHT = 400


MAX_FPS = 20
GRID_SIZE = 50
MAX_MEMORY = 100_000
BATCH_SIZE = 1000  # this is the sample size
LR = 0.001  # Learning rate

class Agent2:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # if memory exceeds maxlen, then automatic popleft()
        self.model = linear_QNet(5, 256, 2)
        self.trainer = QTrainer(self.model, learning_rate=LR, gamma=self.gamma)
        pass

    def get_state(self, game):
        """"
        Representing state by ball position w.r.t. center of board, together with the movement of the board."""
        ball_left, ball_right, ball_straight = 0, 0, 0
        move_right, move_left, stationary = 0, 0, 0
        if game.board_player_two[0] < game.ball[0]:
            ball_right = 1
        elif game.board_player_two[0] > game.ball[0]:
            ball_left = 1
        else:
            ball_straight = 1

        if game.board_player_two == -game.board_speed:
            move_left = 1
        elif game.board_player_two == game.board_speed:
            move_right = 1
        return np.array([ball_straight, ball_left, ball_right, move_left, move_right], dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        """
        Adding moves to the memory
        """
        self.memory.append((state, action, reward, next_state, game_over))
        return

    def train_long_memory(self):
        """"
        Training for a certain sample size out of the memory
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        """"
        Training on the most recent data point.
        """
        self.trainer.train_step(state, action, reward, next_state, game_over)


    def get_action(self, state, game):
        """"
        Giving move out of model, together with a certain amount of randomness to find potential better tactic of play.
        """
        direction = [-game.board_speed, game.board_speed]
        # random moves: exploration <-> exploitation
        self.epsilon = 100 - self.number_of_games

        final_move = [0, 0]

        if random.randint(0, 220) < self.epsilon:
            move = random.randint(0, 1)  # Choose a random valid move
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)  # Get Q-values
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        game.board_player_two_direction = direction[move]
        return final_move

