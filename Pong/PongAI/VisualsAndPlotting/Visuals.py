import pygame as p
WIDTH = 200
HEIGHT = 200

MAX_FPS = 20
IMAGES = {}
IMAGES["Board_1_black"] = p.transform.scale(p.image.load("IMAGES/Board_1_black.png"), (120, 20))
IMAGES["Board_1_white"] = p.transform.scale(p.image.load("IMAGES/Board_1_white.png"), (120, 20))
IMAGES["Board_2_black"] = p.transform.scale(p.image.load("IMAGES/Board_2_black.png"), (120, 20))
IMAGES["Board_2_white"] = p.transform.scale(p.image.load("IMAGES/Board_2_white.png"), (120, 20))

def drawGameState(screen, gamestate):
    screen.fill(p.Color("black"))
    drawBoards(screen, gamestate)
    drawBall(screen, gamestate)

def drawBoards(screen, gamestate):
    board_one = IMAGES["Board_1_white"].get_rect()
    # Set the figure's initial position
    board_one.x = gamestate.board_player_one[0] - gamestate.board_width/2
    board_one.y = gamestate.board_player_one[1] - gamestate.board_height/2
    screen.blit(IMAGES["Board_1_white"], board_one)

    board_two = IMAGES["Board_2_white"].get_rect()
    # Set the figure's initial position
    board_two.x = gamestate.board_player_two[0] - gamestate.board_width/2
    board_two.y = gamestate.board_player_two[1] - gamestate.board_height/2
    screen.blit(IMAGES["Board_2_white"], board_two)


def drawBall(screen, gamestate):
    #p.draw.circle(screen, "red", (gamestate.ball[0], gamestate.ball[1]), 7)
    p.draw.circle(screen, "white", (gamestate.ball[0], gamestate.ball[1]), 5)
    return
