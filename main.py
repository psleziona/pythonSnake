import sys
import pygame
from pygame import Vector2
import random


class Board:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.snake = Snake(self, self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.frame = pygame.time.Clock()
        self.time_count = 0
        self.food_counter = 0
        self.food = []
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.time_count += self.frame.tick() / 300
            if self.time_count > 0.5:
                self.snake.move()
                self.time_count -= 0.5

            self.snake.draw()
            if self.food_counter == 0:
                self.food_gen()
            if len(self.food):
                pygame.draw.rect(self.screen, (200, 40, 80), self.food[0])
            self.check_is_eat()
            pygame.display.flip()

    def food_gen(self):
        self.food_counter += 1
        foodx, foody = Vector2(random.randrange(0, 1280, 20), random.randrange(0, 640, 20))
        self.food.append((foodx, foody, 20, 20))

    def check_is_eat(self):
        if len(self.food) > 0:
            fx, fy = self.food[0][0], self.food[0][1]
            if fx == self.snake.snake[-1].x and fy == self.snake.snake[-1].y:
                self.snake.eat()


class Snake:

    def __init__(self, board, x, y):
        # Board
        self.board = board
        # Starting points
        self.start_point = Vector2(x, y)
        self.snake = [pygame.Rect(self.start_point.x - 40, self.start_point.y, 20, 20),
                      pygame.Rect(self.start_point.x - 20, self.start_point.y, 20, 20),
                      pygame.Rect(self.start_point, (20, 20))]
        self.move_direction = 'right'

    def draw(self):
        for block in self.snake:
            pygame.draw.rect(self.board.screen, (200, 0, 100), block)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.turn('up')
        if keys[pygame.K_s]:
            self.turn('down')
        if keys[pygame.K_d]:
            self.turn('left')
        if keys[pygame.K_a]:
            self.turn('right')
        if self.move_direction == 'right':
            self.turn('left')
        if self.move_direction == 'left':
            self.turn('right')
        if self.move_direction == 'top':
            self.turn('up')
        if self.move_direction == 'down':
            self.turn('down')

    def turn(self, dir):
        cx, cy = self.snake[-1].x, self.snake[-1].y
        self.snake.pop(0)
        if dir == 'down':
            cy += 20
            self.move_direction = 'down'
        elif dir == 'up':
            cy -= 20
            self.move_direction = 'top'
        elif dir == 'right':  # Dojebac szerokosc wensza jako zmienna
            cx -= 20
            self.move_direction = 'left'
        elif dir == 'left':
            cx += 20
            self.move_direction = 'right'
        if cx == 1280:
            self.snake[-1].x = 0
        if cy == 720:
            self.snake[-1].y = 0
        print(cx, cy)
        self.snake.append(pygame.Rect(cx, cy, 20, 20))

    def eat(self):
        tailx, taily = self.snake[0].x, self.snake[0].y
        self.snake[0:0] = [pygame.Rect(tailx, taily, 20, 20)]
        self.board.food = []
        self.board.food_counter -= 1


Board()
