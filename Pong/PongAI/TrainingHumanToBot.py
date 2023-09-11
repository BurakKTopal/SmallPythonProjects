from PongAI.Agents.AgentOne import *
from PongAI.Agents.AgentTwo import *
from VisualsAndPlotting.Helper import *
from VisualsAndPlotting.Visuals import *
from GameState import *
import pygame as p

def train():
    """"
    Training...
    """
    plot_scores = []
    plot_mean_scores = []
    mean_score = 0
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))


    record = 0
    agent = Agent1()
    game = Game(WIDTH, HEIGHT)

    while True:
        # initializing move of player one and two:
        game.board_player_one_direction = 0
        game.board_player_two_direction = 0
        while game.player_two_to_move:
            for e in p.event.get():
                if e.type == p.QUIT:
                    input('the game ended!')
                if e.type == p.KEYDOWN:
                    # Check for key presses to change direction
                    if e.key == p.K_LEFT:
                        game.board_player_two_direction = -20
                        break
                    elif e.key == p.K_RIGHT:
                        game.board_player_two_direction = 20
                        break
            if game.gameOver():
                game.player_one_to_move = True
                game.player_two_to_move = False
                break
            elif game.bounceBallAgainstBoard() == 1:
                game.player_one_to_move = True
                game.player_two_to_move = False
                break
            else:
                drawGameState(screen, game)
                game.boardMovementHumanAsPlayerTwo()
                game.ballMovementWithAI()


            clock.tick(MAX_FPS)
            p.display.flip()

        while game.player_one_to_move:
            state_old = agent.get_state(game)  # get old state

            final_move = agent.get_action(state_old, game)  # get final move
            reward, game_over, score = game.makeMoveAIOne()
            state_new = agent.get_state(game)

            agent.train_short_memory(state_old, final_move, reward, state_new, game_over)  # train short memory

            agent.remember(state_old, final_move, reward, state_new, game_over)

            if game_over:
                # experienced play
                game.reset()
                agent.number_of_games += 1
                agent.train_long_memory()
                if score > record:
                    record = score
                    agent.model.save()

                plot_scores.append(score)
                mean_score = (mean_score * (agent.number_of_games - 1) + score) / agent.number_of_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores, [], [])
                print('Generation', agent.number_of_games, 'Score: ', score, 'Record: ', record)
                print('----------------------------------------------')
                break
            elif game.bounceBallAgainstBoard() == -1:
                game.player_one_to_move = False
                game.player_two_to_move = True
                drawGameState(screen, game)
                break
            else:
                game.ballMovementWithAI()
                drawGameState(screen, game)

            clock.tick(MAX_FPS)
            p.display.flip()

        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    train()
