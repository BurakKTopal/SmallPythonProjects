import random


class Game:
    def __init__(self, window_width, window_height):
        self.board_speed = 20  # speed of the board movement

        self.player_one_to_move = False
        self.player_two_to_move = True

        self.n_bounces_player_two = 0  # number of bounces on the board
        self.n_bounces_player_one = 0  # number of bounces on the board

        self.player_one_lost = False
        self.player_two_lost = False

        # boards are going to be chosen 120 x 10
        self.board_height = 20
        self.board_width = 120

        # adding board edge physics
        self.board_edge = self.board_width / 20

        # coordinate of board, together with movement
        self.board_player_one = [window_width / 2, window_height - self.board_height]  # Coordinate center of board
        self.board_player_one_direction = 0

        self.board_player_two = [window_width / 2, self.board_height]  # Coordinate center of board
        self.board_player_two_direction = 0  # -board_speed: left, +board_speed right

        self.window_width = window_width
        self.window_height = window_height
        self.ball = [window_width / 2, window_height / 2]
        self.ball_speed_y = -15
        possible_velocities = [x for x in range(-12, 0)] + [x for x in range(1, 13)]
        self.ball_speed_x = random.choice(possible_velocities)

    def bounceBallAgainstBoard(self):
        """"
        Ball bounces against board, with edge physics
        """
        if self.ball[1] == self.board_player_two[1] and self.board_player_two[0] - self.board_width / 2 < self.ball[0]\
                < self.board_player_two[0] + self.board_width / 2:

            if self.board_player_two[0] - self.board_width / 2 + self.board_edge < self.ball[0] < self.board_player_two[
                0] + self.board_width / 2 - self.board_edge:
                self.ball_speed_y *= -1  # Balls bounces back vertically
                return 1

            elif self.board_player_two[0] - self.board_width / 2 <= self.ball[0] <= self.board_player_two[
                0] - self.board_width / 2 + self.board_edge:
                self.ball_speed_y, self.ball_speed_x = (self.ball_speed_x, self.ball_speed_y)
                return 1

            else:
                self.ball_speed_y, self.ball_speed_x = (-self.ball_speed_x, -self.ball_speed_y)
                return 1

        elif self.ball[1] == self.board_player_one[1] and self.board_player_one[0] - self.board_width / 2 < self.ball[
            0] < self.board_player_one[0] + self.board_width / 2:
            if self.board_player_one[0] - self.board_width / 2 + self.board_edge < self.ball[0] < self.board_player_one[
                0] + self.board_width / 2 - self.board_edge:
                self.ball_speed_y *= -1  # Balls bounces back vertically
                return -1  # Only true if balls hits against the second player's board!

            elif self.board_player_one[0] - self.board_width / 2 < self.ball[0] <= self.board_player_one[
                0] - self.board_width / 2 + self.board_edge:
                self.ball_speed_y, self.ball_speed_x = (-self.ball_speed_x, -self.ball_speed_y)
                return -1

            else:
                self.ball_speed_y, self.ball_speed_x = (self.ball_speed_x, self.ball_speed_y)
                return -1
        return 0

    def bounceBallAgainstWall(self):
        """"
        Ball bounces to walls, perfect elastic collision
        """
        if self.ball[0] <= 0 or self.ball[0] >= self.window_width:
            self.ball_speed_x *= -1
        return

    def gameOver(self):
        """"
        Game ends if ball goes behind one of the boards
        """
        if self.ball[1] <= -self.board_height:
            self.player_two_lost = True
            return True

        elif self.ball[1] >= self.window_height + self.board_height:
            self.player_one_lost = True
            return True
        return False

    def ballMovement(self):
        """"
        incorporating ball movement, for multiplayer purposes
        """
        self.bounceBallAgainstBoard()
        self.bounceBallAgainstWall()
        self.ball[0] += self.ball_speed_x
        self.ball[1] += self.ball_speed_y
        return

    def ballMovementWithAI(self):
        """"
        incorporating ball movement, for AI purposes; as the buonce against board is already done before the ball movement
        """
        self.bounceBallAgainstWall()
        self.ball[0] += self.ball_speed_x
        self.ball[1] += self.ball_speed_y
        return

    def boardMovement(self):
        """""
        board movement
        """
        if self.board_width / 2 == self.board_player_one[0] and self.board_player_one_direction < 0:
            pass

        elif self.board_player_one[
            0] == self.window_width - self.board_width / 2 and self.board_player_one_direction > 0:
            pass
        else:
            self.board_player_one[0] += self.board_player_one_direction

        if self.board_width / 2 == self.board_player_two[0] and self.board_player_two_direction < 0:
            pass

        elif self.board_player_two[
            0] == self.window_width - self.board_width / 2 and self.board_player_two_direction > 0:
            pass
        else:
            self.board_player_two[0] += self.board_player_two_direction

        return

    def boardMovementHumanAsPlayerTwo(self):
        """"
        board movement by human
        """
        if self.board_width / 2 == self.board_player_two[0] and self.board_player_two_direction < 0:
            return

        elif self.board_player_two[
            0] == self.window_width - self.board_width / 2 and self.board_player_two_direction > 0:
            return
        else:
            self.board_player_two[0] += self.board_player_two_direction

        return

    def makeMoveAITwo(self):
        """"
         move by AI as player one
         reward is 0 he wins game, because the player can play terrible, which would let think that the move was good.
         Reward is -20 if he loses a game
         Reward is 10 if the ball bounces on the board
         Reward is 0 else
         """
        if self.gameOver():
            if self.player_two_lost:
                reward = -20
                return reward, True, self.n_bounces_player_two
            elif self.player_one_lost:
                reward = 0
                return reward, True, self.n_bounces_player_two
        else:
            if self.bounceBallAgainstBoard() == 1:
                self.n_bounces_player_two += 1
                reward = 10
                return reward, False, self.n_bounces_player_two

            elif self.board_width / 2 == self.board_player_two[0] and self.board_player_two_direction < 0:
                reward = 0
                return reward, False, self.n_bounces_player_two

            elif self.board_player_two[
                0] == self.window_width - self.board_width / 2 and self.board_player_two_direction > 0:
                reward = 0
                return reward, False, self.n_bounces_player_two
            else:
                self.board_player_two[0] += self.board_player_two_direction
                reward = 0
                return reward, False, self.n_bounces_player_two

    def makeMoveAIOne(self):
        """"
        move by AI as player one
        reward is 0 he wins game, because the player can play terrible, which would let think that the move was good.
        Reward is -20 if he loses a game
        Reward is 10 if the ball bounces on the board
        Reward is 0 else
        """
        if self.gameOver():
            if self.player_two_lost:
                reward = 0
                return reward, True, self.n_bounces_player_one
            elif self.player_one_lost:
                reward = -20
                return reward, True, self.n_bounces_player_one
        else:
            if self.bounceBallAgainstBoard() == -1:
                self.n_bounces_player_one += 1
                reward = 10
                return reward, False, self.n_bounces_player_one

            elif (self.board_width / 2 == self.board_player_one[0] and self.board_player_one_direction < 0):
                reward = 0
                return reward, False, self.n_bounces_player_one

            elif (self.board_player_one[
                      0] == self.window_width - self.board_width / 2 and self.board_player_one_direction > 0):
                reward = 0
                return reward, False, self.n_bounces_player_one
            else:
                self.board_player_one[0] += self.board_player_one_direction
                reward = 0
                return reward, False, self.n_bounces_player_one

    def reset(self):
        """"
        Game reset
        """
        self.player_one_to_move = False
        self.player_two_to_move = True

        self.n_bounces_player_one = 0
        self.n_bounces_player_two = 0
        self.points = 0
        self.player_one_lost = False
        self.player_two_lost = False

        # boards are going to be chosen 50 x 20
        self.board_height = 10
        self.board_width = 120
        self.board_edge = self.board_width / 15

        self.board_player_one = [self.window_width / 2,
                                 self.window_height - self.board_height]  # Coordinate center of board
        self.board_player_one_direction = 0

        self.board_player_two = [self.window_width / 2, self.board_height]  # Coordinate center of board
        self.board_player_two_direction = 0  # -1: left, +1 right

        self.ball = [self.window_width / 2, self.window_height / 2]
        self.ball_speed_y = -10
        possible_velocities = [x for x in range(-12, 0)] + [x for x in range(1, 13)]

        self.ball_speed_x = random.choice(possible_velocities)
        return
