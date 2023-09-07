import random
class Snake:
    def __init__(self, grid_size, window_width, window_height):
        self.grid_size = grid_size
        self.points = 0
        self.dimension = window_height/grid_size
        self.window_width = window_width
        self.window_height = window_height
        self.snake_direction = (0, 0)
        self.segments = [(self.dimension//2, self.dimension//2)]
        self.food = (random.randint(1, self.dimension-2), random.randint(1, self.dimension-2))

    def snakeEats(self):
        head_x = self.segments[-1][0]
        head_y = self.segments[-1][1]
        if (head_x + self.snake_direction[0], head_y+self.snake_direction[1]) == self.food:
            self.segments.append(self.food)
            self.points += 1
            return True
        return False

    def snakeMovements(self):
        print(self.segments)
        # Adding new head
        self.segments.append((self.segments[-1][0] + self.snake_direction[0], self.segments[-1][1] + self.snake_direction[1]))

        # Deleting tail
        self.segments.pop(0)

    def snakeTouchesWalls(self):
        if self.segments[-1][0] < 1 or self.segments[-1][0] >= self.dimension-1:
            return True
        elif self.segments[-1][1] < 1 or self.segments[-1][1] >= self.dimension-1:
            return True
        return False

    def snakeTouchesSnake(self):
        if self.segments[-1] in self.segments[:-1]:
            return True
        return False
