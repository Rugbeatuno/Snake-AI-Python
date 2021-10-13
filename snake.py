import pygame
from random import randrange
from ai import assign_variables
import time

pygame.init()

# colors
gray = (50, 50, 50)
white = (250, 250, 250)
red = (200, 0, 0)
green = (0, 200, 0)
yellow = (0, 150, 150)

# screen
screen_width, screen_height = 700, 700
pygame.display.set_caption("Snake AI")
rows, cols = 35, 35
scale = 20

class Game:
    head_pos = (0, 0)
    win = pygame.display.set_mode((screen_width, screen_height))
    food_cords = 500, 400


    def __init__(self):
        self.refresh()

    def refresh(self):
        self.background()
        self.show_path()
        self.draw_food()
        self.draw_body()

    def background(self):
        self.win.fill(gray)

        '''for i in range(60):
            pygame.draw.line(self.win, white, (0, i * scale), (screen_width, i * scale))
            pygame.draw.line(self.win, white, (i * scale, 0), (i * scale, screen_height))'''

    def draw_food(self):
        x, y = Game.food_cords
        pygame.draw.rect(self.win, red, (x + 1, y + 1, scale - 1, scale - 1))  # draws food

    def draw_body(self):
        head = len(Snake.body) - 1
        for index, segment in enumerate(Snake.body):
            x, y = segment.x, segment.y

            if index == head:
                pygame.draw.rect(self.win, green, (x + 1, y + 1, scale - 1, scale - 1))  # draws head

            elif segment.facing == "L" or segment.facing == "R":  # draws body if moving vertically or horizontally
                pygame.draw.rect(self.win, white, (x, y + 4, scale, scale - 8))
            elif segment.facing == "U" or segment.facing == "D":
                pygame.draw.rect(self.win, white, (x + 4, y, scale - 8, scale))

            elif segment.facing == "DR" or segment.facing == "LU":  # draws body when turning
                pygame.draw.rect(self.win, white, (x + 4, y, scale - 8, scale - 4))  # vertical     []
                pygame.draw.rect(self.win, white, (x + 4, y + 4, scale, scale - 8))  # horizontal   [] []
            elif segment.facing == "UR" or segment.facing == "LD":
                pygame.draw.rect(self.win, white, (x + 4, y + 4, scale, scale - 8))  # horizontal   [] []
                pygame.draw.rect(self.win, white, (x + 4, y + 4, scale - 8, scale))  # vertical     []
            elif segment.facing == "UL" or segment.facing == "RD":
                pygame.draw.rect(self.win, white, (x, y + 4, scale - 8, scale - 8))  # horizontal   [] []
                pygame.draw.rect(self.win, white, (x + 4, y + 4, scale - 8, scale))  # vertical        []
            elif segment.facing == "RU" or segment.facing == "DL":
                pygame.draw.rect(self.win, white, (x + 4, y, scale - 8, scale - 4))  # vertical        []
                pygame.draw.rect(self.win, white, (x, y + 4, scale - 8, scale - 8))  # horizontal   [] []


    @staticmethod
    def show_path():
        x, y = Game.head_pos
        for letter in Snake.path:
            if letter == "L":
                x -= scale
            elif letter == "R":
                x += scale
            elif letter == "U":
                y -= scale
            elif letter == "D":
                y += scale

            pygame.draw.rect(Game.win, yellow, (x + 5, y + 5, scale - 10, scale - 10))

    @staticmethod
    def create_food():
        x, y = randrange(0, cols) * scale, randrange(0, rows) * scale  # assigns food to new location
        Game.food_cords = x, y

        for segment in Snake.body:
            if segment.x == x and segment.y == y:
                return False
        return True






class Snake:
    body = []  # all body segment cords
    prev_tail_pos = 0, 0, None
    moving = None
    prev_dir = ""
    path_index = 0
    path = ""

    def __init__(self, x, y, facing=moving):
        self.x = x
        self.y = y
        self.facing = facing
        Snake.body.insert(0, self)
        Snake.get_path()

    def move(self):
        delta_x = 0
        delta_y = 0
        if Snake.moving == 'L':  # adds or subtracts from x or y axis based on key pressed
            delta_x = -scale
        if Snake.moving == 'R':
            delta_x = scale
        if Snake.moving == 'U':
            delta_y = -scale
        if Snake.moving == 'D':
            delta_y = scale

        self.add_segment(delta_x, delta_y)
        self.turn()


    def turn(self):
        if Snake.prev_dir != Snake.moving:
            head = len(Snake.body) - 2  # changes body after head
            Snake.body[head].facing = Snake.prev_dir + Snake.moving

        Snake.prev_dir = Snake.moving

    def ate_food(self):
        #  [body, body, body, head]
        head = len(Snake.body) - 1
        x = Snake.body[head].x  # gets the snakes head x, y position
        y = Snake.body[head].y

        if (x, y) == (Game.food_cords):  # if head is at the same coordinates as food
            return True
        return False

    def add_segment(self, x, y):
        head = len(Snake.body) - 1
        new_x = Snake.body[head].x + x  # gets the new head x, y position
        new_y = Snake.body[head].y + y

        if self.ate_food():
            tail_x, tail_y, facing = Snake.prev_tail_pos[0], Snake.prev_tail_pos[1], Snake.prev_tail_pos[2]
            Snake(tail_x, tail_y, facing)  # creates new head which replaces old head -- old head becomes body
        else:
            for i in range(head):
                Snake.body[i].x = Snake.body[i+1].x  # moves all body segments to the segment in front of it
                Snake.body[i].y = Snake.body[i+1].y
                Snake.body[i].facing = Snake.body[i+1].facing

            Snake.body[head].x = new_x  # moves head to new head position
            Snake.body[head].y = new_y
            Snake.body[head].facing = Snake.moving
            Snake.prev_tail_pos = Snake.body[0].x, Snake.body[0].y, Snake.body[0].facing

    def crashed(self):
        direction = self.moving
        head = len(Snake.body) - 1


        '''head_x, head_y = Snake.body[head].x, Snake.body[head].y
        for segment in Snake.body:
            x, y = segment.x, segment.y
            if head_x == x and head_y == y and len(Snake.body) > 4:
                return True'''

        return False

    @staticmethod
    def get_path():
        head = len(Snake.body) - 1
        while not Game.create_food():
            pass


        Snake.path = assign_variables(Snake.body, (Game.food_cords))
        Game.head_pos = (Snake.body[head].x, Snake.body[head].y)
        if Snake.path == "trapped":
            print("trapped")


        Snake.path_index = 0







def main():
    clock = pygame.time.Clock()
    FPS = 40
    run = True

    Snake(60, 400)
    Snake(80, 400)
    snake = Snake(100, 400)


    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    FPS += 1
                if event.key == pygame.K_DOWN:
                    FPS -= 1

        try:
            Snake.moving = Snake.path[Snake.path_index]
            Snake.path_index += 1
        except IndexError:
            pass

        Game()
        snake.move()

        pygame.display.flip()

main()