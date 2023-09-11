import pygame as p
from GameState import *
WIDTH = 600
HEIGHT = 400

MAX_FPS = 10
IMAGES = {}
IMAGES["Board_1"] = p.transform.scale(p.image.load("PongAI/VisualsAndPlotting/IMAGES/Board_1_black.png"), (120, 10))
IMAGES["Board_2"] = p.transform.scale(p.image.load("PongAI/VisualsAndPlotting/IMAGES/Board_2_black.png"), (120, 10))

gamestate = Game(WIDTH, HEIGHT)

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    drawGameState(screen, gamestate)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                input('the game ended!')
            if e.type == p.KEYDOWN:
                # Check for key presses to change direction
                if e.key == p.K_LEFT:
                    gamestate.board_player_one_direction = -gamestate.board_speed

                if e.key == p.K_RIGHT:
                    gamestate.board_player_one_direction = gamestate.board_speed

                if e.key == p.K_q:
                    gamestate.board_player_two_direction = -gamestate.board_speed

                if e.key == p.K_d:
                    gamestate.board_player_two_direction = gamestate.board_speed




        gamestate.boardMovement()
        gamestate.ballMovement()

        if gamestate.gameOver():
            input("game ended!")
            running = False
        drawGameState(screen, gamestate)
        clock.tick(MAX_FPS)
        p.display.flip()
p.quit()





def drawGameState(screen, gamestate):
    screen.fill(p.Color("white"))
    drawBoards(screen, gamestate)
    drawBall(screen, gamestate)

def drawBoards(screen, gamestate):
    board_one = IMAGES["Board_1"].get_rect()
    # Set the figure's initial position
    board_one.x = gamestate.board_player_one[0] - gamestate.board_width/2
    board_one.y = gamestate.board_player_one[1] - gamestate.board_height/2
    screen.blit(IMAGES["Board_1"], board_one)

    board_two = IMAGES["Board_2"].get_rect()
    # Set the figure's initial position
    board_two.x = gamestate.board_player_two[0] - gamestate.board_width/2
    board_two.y = gamestate.board_player_two[1] - gamestate.board_height/2
    screen.blit(IMAGES["Board_2"], board_two)


def drawBall(screen, gamestate):
    p.draw.circle(screen, "red", (gamestate.ball[0], gamestate.ball[1]), 7)
    return


if __name__ == '__main__':
    main()