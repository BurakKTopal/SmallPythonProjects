import pygame as p
from GameState import *

WIDTH = HEIGHT = 600
MAX_FPS = 5
GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
DIMENSION = WIDTH / GRID_SIZE

snake = Snake(GRID_SIZE, WIDTH, HEIGHT)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    drawSnake(screen, snake)
    drawFruit(screen, snake)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                input('the game ended!')

            # Check for key presses to change direction
            if e.type == p.KEYDOWN:
                if e.key == p.K_UP and snake.snake_direction != (0, 1):
                    snake.snake_direction = (0, -1)
                elif e.key == p.K_DOWN and snake.snake_direction != (0, -1):
                    snake.snake_direction = (0, 1)
                elif e.key == p.K_LEFT and snake.snake_direction != (1, 0):
                    snake.snake_direction = (-1, 0)
                elif e.key == p.K_RIGHT and snake.snake_direction != (-1, 0):
                    snake.snake_direction = (1, 0)

        if snake.snakeEats():
            snake.food = (random.randint(1, DIMENSION - 2), random.randint(1, DIMENSION - 2))
        else:
            snake.snakeMovements()

        drawGameState(screen, snake)

        if snake.snakeTouchesWalls() or snake.snakeTouchesSnake():
            print('You had a score of: ', snake.points)
            input('Press enter to close the game')
            running = False

        clock.tick(MAX_FPS)
        p.display.flip()


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
            # border
            if row == 0 or row == DIMENSION - 1:
                square = p.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                border_width = 2
                p.draw.rect(screen, "black", square, border_width)
            elif col == 0 or col == DIMENSION - 1:
                square = p.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                border_width = 2
                p.draw.rect(screen, "black", square, border_width)

            else:
                square = p.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                border_width = 1
                p.draw.rect(screen, "gray", square, border_width)


def drawSnake(screen, snake):
    for index in range(len(snake.segments)):
        segment = snake.segments[index]
        if index == len(snake.segments) - 1:
            p.draw.rect(screen, "black", (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        else:
            square = p.draw.rect(screen, "green",
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            border_width = 1
            p.draw.rect(screen, "black", square, border_width)


def drawFruit(screen, snake):
    p.draw.rect(screen, "red", (snake.food[0] * GRID_SIZE, snake.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    return


if __name__ == '__main__':
    main()
