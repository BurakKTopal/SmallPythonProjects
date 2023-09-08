import pygame as p

WIDTH = HEIGHT = 600

MAX_FPS = 10
GRID_SIZE = 50
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
DIMENSION = WIDTH / GRID_SIZE
IMAGES = {}
IMAGES["SnakeHead"] = p.transform.scale(p.image.load("Images/SnakeHead.png"), (GRID_SIZE, GRID_SIZE))
IMAGES["SnakeHeadDead"] = p.transform.scale(p.image.load("Images/SnakeHeadDead.png"), (GRID_SIZE, GRID_SIZE))

def drawGameState(screen, snake):
    # Background of the board
    screen.fill(p.Color("white"))

    # Drawing the grid
    drawGrid(screen)

    # Drawing the fruit
    drawFruit(screen, snake)

    # Drawing the snake
    drawSnake(screen, snake)


def drawGrid(screen):
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE):

            square = p.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            border_width = 1
            p.draw.rect(screen, "gray", square, border_width)


def drawSnake(screen, snake):
    for index in range(len(snake.segments)):
        segment = snake.segments[index]
        if index == len(snake.segments) - 1:
            if snake.died:
                snake_head_direction = {(0, 0): 0, (-1, 0): 90, (1, 0): -90, (0, -1): 0, (0, 1): 180}
                screen.blit(p.transform.rotate(IMAGES["SnakeHeadDead"], snake_head_direction[snake.snake_direction]),
                            p.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            else:
                snake_head_direction = {(0, 0) : 0, (-1, 0): 90, (1, 0): -90, (0, -1): 0, (0, 1): 180}
                screen.blit(p.transform.rotate(IMAGES["SnakeHead"],snake_head_direction[snake.snake_direction]), p.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        else:
            square = p.draw.rect(screen, "#76a512",
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            border_width = 1
            p.draw.rect(screen, "darkgreen", square, border_width)


def drawFruit(screen, snake):
    p.draw.rect(screen, "red", (snake.food[0] * GRID_SIZE, snake.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    return

