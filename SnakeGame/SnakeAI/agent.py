import torch
import numpy as np
from collections import deque
from Model import linear_QNet, QTrainer
from Visualisation import *
from Helper import *
from GameState import *

WIDTH = HEIGHT = 600

MAX_FPS = 20
GRID_SIZE = 50
MAX_MEMORY = 100_000
BATCH_SIZE = 1000  # this is the sample size
LR = 0.001  # Learning rate

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # if memory exceeds maxlen, then automatic popleft()
        self.model = linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, learning_rate=LR, gamma=self.gamma)

        pass

    def get_state(self, snake):
        danger_up, danger_down, danger_left, danger_right, food_up, food_down, food_left, food_right = 0, 0, 0, 0, 0, 0, 0, 0
        move_up, move_down, move_left, move_right = 0,0,0,0
        head = snake.segments[-1]
        point_l = (head[0] - 1, head[1])
        point_r = (head[0] + 1, head[1])
        point_u = (head[0], head[1] - 1)
        point_d = (head[0], head[1] + 1)

        if point_u[1] < 1:
            danger_up = 1
        if point_d[1] >= snake.dimension - 1:
            danger_down = 1
        if point_l[0] < 1:
            danger_left = 1
        if point_r[0] >= snake.dimension - 1:
            danger_right = 1

        dx = snake.food[0] - head[0]
        dy = snake.food[1] - head[1]
        if dy <= 0:
            food_up = 1
        elif dy > 0:
            food_down = 1
        if dx < 0:
            food_left = 1
        elif dx > 0:
            food_right = 1
        if snake.snake_direction == (0, -1):
            move_up = 1
        elif snake.snake_direction == (0, 1):
            move_down = 1
        elif snake.snake_direction == (-1, 0):
            move_left = 1
        elif snake.snake_direction == (1, 0):
            move_right = 1
        return np.array([danger_up, danger_down, danger_left, danger_right, food_up, food_down, food_left, food_right,
                move_up, move_down, move_left, move_right], dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        """

        :param state: configuration of current game state
        :param action: Move snake made
        :param reward: reward the snake got from the played move
        :param next_state: the configuration after the action is played
        :param game_over: True if game ends, False if not
        :return:
        """
        self.memory.append((state, action, reward, next_state, game_over))
        return

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    # def get_action(self, state, snake):
    #     direction = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}
    #     # random moves: exploration <-> exploitation
    #     self.epsilon = 80 - self.number_of_games
    #     final_move = [0, 0, 0,0]
    #     if random.randint(0, 200) < self.epsilon:
    #         move = random.randint(0, 3)
    #         final_move[move] = 1
    #
    #     else:
    #         state0 = torch.tensor(state, dtype=torch.float)
    #         prediction = self.model(state0)  # prediction is the Q-value
    #         move = torch.argmax(prediction).item()
    #         final_move[move] = 1
    #     # snake.move = final_move
    #     # snake.move_index = move
    #     snake.snake_direction = direction[move]
    #
    #     return final_move

    def get_action(self, state, snake):
        direction = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}
        # random moves: exploration <-> exploitation
        self.epsilon = 80 - self.number_of_games
        possible_moves = [0, 1, 2, 3]  # Initialize with all possible moves
        final_move = [0, 0, 0, 0]

        # Calculate the opposite direction of the current direction
        opposite_direction = (-snake.snake_direction[0], -snake.snake_direction[1])

        # Remove the opposite direction from the possible moves to avoid self-collision
        if opposite_direction in direction.values():
            possible_moves.remove(list(direction.keys())[list(direction.values()).index(opposite_direction)])

        if random.randint(0, 200) < self.epsilon:
            move = random.choice(possible_moves)  # Choose a random valid move
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) # Get Q-values
            valid_predictions = [prediction.tolist()[i] for i in possible_moves]
            move = possible_moves[valid_predictions.index(max(valid_predictions))]
            final_move[move] = 1

        snake.snake_direction = direction[move]

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    mean_score = 0
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))


    record = 0
    agent = Agent()
    snake = Snake(GRID_SIZE, WIDTH, HEIGHT)
    drawSnake(screen, snake)
    drawFruit(screen, snake)

    while True:
        state_old = agent.get_state(snake)  # get old state

        final_move = agent.get_action(state_old, snake)  # get final move
        reward, game_over, score = snake.makeMove()

        state_new = agent.get_state(snake)

        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)  # train short memory

        agent.remember(state_old, final_move, reward, state_new, game_over)
        drawGameState(screen, snake)
        if game_over:
            # experienced play
            snake.reset()
            agent.number_of_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()

            plot_scores.append(score)
            mean_score = (mean_score*(agent.number_of_games - 1) + score)/agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            print('Generation', agent.number_of_games, 'Score: ', score, 'Record: ', record)
            print('----------------------------------------------')
            # plot_scores.append(score)
            # total_score += plot_mean_scores
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    train()
