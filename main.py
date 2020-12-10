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

            # Reset screen and count fps
            self.screen.fill((0, 0, 0))
            self.time_count += self.frame.tick() / 300
            self.snake.handle_moves()
            if self.time_count > 0.5:
                self.snake.move_direction()
                self.time_count -= 0.5

            # Keep snake on surface
            self.snake.draw()
            collision = self.snake.check_self_coll()
            if collision:
                break
                
            # Food generator
            if self.food_counter == 0:
                self.food_generator()
            if len(self.food):
                pygame.draw.rect(self.screen, (200, 40, 80), self.food[0])
            self.check_snake_eat()

            pygame.display.flip()

    def food_generator(self):
        self.food_counter += 1
        foodx, foody = Vector2(random.randrange(0, self.screen.get_width(), self.snake.size),
                               random.randrange(0, self.screen.get_height(), self.snake.size))
        self.food.append((foodx, foody, 20, 20))

    def check_snake_eat(self):
        if len(self.food):
            fx, fy = self.food[0][0], self.food[0][1]
            if fx == self.snake.snake[-1].x and fy == self.snake.snake[-1].y:
                self.snake.eat()


class Snake:

    def __init__(self, board, x, y):
        # Board
        self.board = board
        # Starting points
        self.start_point = Vector2(x, y)
        self.size = 20
        self.snake = [pygame.Rect(self.start_point.x - 2 * self.size, self.start_point.y, self.size, self.size),
                      pygame.Rect(self.start_point.x - self.size, self.start_point.y, self.size, self.size),
                      pygame.Rect(self.start_point, (self.size, self.size))]
        self.direction = 'right'

    def draw(self):
        for i, block in enumerate(self.snake):
            block.x, block.y = self.through_wall(block.x, block.y)
            if i == len(self.snake) - 1:
                pygame.draw.rect(self.board.screen, (10, 200, 50), block)
            else:
                pygame.draw.rect(self.board.screen, (100, 0, 100), block)

    def handle_moves(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.direction != 'down':
                self.direction = 'up'
        if keys[pygame.K_s]:
            if self.direction != 'up':
                self.direction = 'down'
        if keys[pygame.K_d]:
            if self.direction != 'left':
                self.direction = 'right'
        if keys[pygame.K_a]:
            if self.direction != 'right':
                self.direction = 'left'

    def move_direction(self):
        cx, cy = self.snake[-1].x, self.snake[-1].y
        self.snake.pop(0)
        if self.direction == 'down':
            cy += self.size
        elif self.direction == 'up':
            cy -= self.size
        elif self.direction == 'right':
            cx += self.size
        elif self.direction == 'left':
            cx -= self.size
        self.snake.append(pygame.Rect(cx, cy, self.size, self.size))

    def eat(self):
        tailx, taily = self.snake[0].x, self.snake[0].y
        self.snake[0:0] = [pygame.Rect(tailx - 20, taily - 20, self.size, self.size)]
        self.board.food = []
        self.board.food_counter -= 1

    def check_self_coll(self):
        for elem in self.snake:
            df = self.snake.count(elem)
            if df > 1:
                return True

    def through_wall(self, x, y):
        max_w = self.board.screen.get_width()
        max_h = self.board.screen.get_height()
        if x >= max_w:
            x -= max_w
        if y >= max_h:
            y -= max_h
        if x < 0 and self.direction == 'left':
            x += self.board.screen.get_width()
        if y < 0 and self.direction == 'up':
            y += self.board.screen.get_height()
        return x, y


Board()
