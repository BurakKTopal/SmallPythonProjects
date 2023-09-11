from PongAI.Agents.AgentOne import *
from PongAI.Agents.AgentTwo import *
from VisualsAndPlotting.Helper import *
from VisualsAndPlotting.Visuals import *
from GameState import *
import pygame as p

def train():
    """
    Training...
    """
    plot_scores = []
    plot_mean_scores = []
    mean_score_2 = 0
    mean_score_1 = 0
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))


    record = 0
    agent1 = Agent1()
    agent2 = Agent2()
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
                    if e.key == p.K_a:
                        game.reset()
                        break


            state_old = agent2.get_state(game)  # get old state

            final_move = agent2.get_action(state_old, game)  # get final move
            reward, game_over, score_2 = game.makeMoveAITwo()
            state_new = agent2.get_state(game)

            agent2.train_short_memory(state_old, final_move, reward, state_new, game_over)  # train short memory

            agent2.remember(state_old, final_move, reward, state_new, game_over)

            if game_over:
                # experienced play
                game.reset()
                agent2.number_of_games += 1
                agent2.train_long_memory()
                if score_2 > record:
                    record = score_2
                    agent2.model.save()

                plot_scores.append(score_2)
                mean_score_2 = (mean_score_2 * (agent2.number_of_games - 1) + score_2) / agent2.number_of_games
                plot_mean_scores.append(mean_score_2)
                plot(plot_scores, plot_mean_scores)
                print('Generation', agent2.number_of_games, 'Score: ', score_2, 'Record: ', record)
                print('----------------------------------------------')
                break
            elif game.bounceBallAgainstBoard() == 1:
                game.ballMovement()
                game.player_one_to_move = True
                game.player_two_to_move = False
                break
            else:
                game.ballMovement()
                drawGameState(screen, game)

            clock.tick(MAX_FPS)
            p.display.flip()

        while game.player_one_to_move:
            for e in p.event.get():
                if e.type == p.QUIT:
                    input('the game ended!')
                if e.type == p.KEYDOWN:
                    # Check for key presses to change direction
                    if e.key == p.K_b:
                        game.reset()
                        break
            state_old = agent1.get_state(game)  # get old state

            final_move = agent1.get_action(state_old, game)  # get final move
            reward, game_over, score_1 = game.makeMoveAIOne()
            state_new = agent1.get_state(game)

            agent1.train_short_memory(state_old, final_move, reward, state_new, game_over)  # train short memory

            agent1.remember(state_old, final_move, reward, state_new, game_over)

            if game_over:
                # experienced play
                game.reset()
                agent1.number_of_games += 1
                agent1.train_long_memory()
                if score_1 > record:
                    record = score_1
                    agent1.model.save()

                plot_scores.append(score_1)
                mean_score_1 = (mean_score_1 * (agent1.number_of_games - 1) + score_1) / agent1.number_of_games
                plot_mean_scores.append(mean_score_1)
                plot(plot_scores, plot_mean_scores)
                print('Generation', agent1.number_of_games, 'Score: ', score_1, 'Record: ', record)
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
