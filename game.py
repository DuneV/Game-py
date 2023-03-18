import pygame
import numpy as np
import random
from enum import Enum
from collections import namedtuple

# Crea la ventana Pygame
pygame.init()

# pasos de la serpiente de tierra caliente

# Define puntos de ganancia 
matrix_goal  = np.zeros((10,10))
matrix_goal[0, 0] = 1
matrix_goal[2, 0] = 1

# Define puntos de perdida
matrix_fail = np.zeros((10,10))
matrix_fail[1, 8] = 1
matrix_fail[3, 6] = 1
matrix_fail[5, 4] = 1
matrix_fail[6, 3] = 1
matrix_fail[7, 2] = 1

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    ENTER = 4


class SL():

    def __init__(self, scaler = 50, radius = 15, bad_max = matrix_fail, good_matrix = matrix_goal):
        self.matrix = np.random.randint(0, 255, (10, 10))
        self.matrix_fail = bad_max
        self.matrix_goal = good_matrix
        self.scaler = scaler 
        self.steps = 0
        self.step = 0
        self.radius = radius
        self.objectsx = []
        self.objectsy = []
        self.size = 35
        self.redux = -10
        self.x = (len(self.matrix[0]) -1)*self.scaler
        self.y = (len(self.matrix) -1)*self.scaler
        self.piso = 0
        self.clock = pygame.time.Clock()
        # init game state
        self.direction = Direction.UP
        self.steps_space = 5*self.scaler
        self.width, self.height = len(self.matrix[0]) * self.scaler + self.steps_space, len(self.matrix) * self.scaler
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.draw_base()
        self.draw_fail()
        self.draw_goal()
        self.draw_cha()
        self.draw_text("Pasos", 625, 80)
        self._update()

    def draw_text(self, text, x, y):
        font = pygame.font.SysFont("serif", self.size)
        text_surface = font.render(text, True, GREEN, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_cha(self):
        rect = pygame.Rect(self.x + self.scaler/6, self.y + self.scaler/3, self.scaler + self.redux, self.scaler + self.redux*2.5)
        pygame.draw.rect(self.screen, GREEN, rect)

    def draw_base(self):
        # Dibuja la matriz en la ventana Pygame
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                rect = pygame.Rect(j * self.scaler, i * self.scaler, self.scaler, self.scaler)
                pygame.draw.rect(self.screen, (self.matrix[i][j], self.matrix[i][j], self.matrix[i][j]), rect)
    
    def draw_goal(self):
        for i in range(len(self.matrix_goal)):
            for j in range(len(self.matrix_goal[0])):
                # circ = pygame.circle(j * scaler, i * scaler, scaler, scaler)
                if (self.matrix_goal[i, j] != 0):
                    pygame.draw.circle(self.screen, BLUE1, (j * self.scaler + self.scaler/2, i * self.scaler + self.scaler/2), self.radius)
    
    def draw_fail(self):
        for i in range(len(self.matrix_fail)):
            for j in range(len(self.matrix_fail[0])):
                # circ = pygame.circle(j * scaler, i * scaler, scaler, scaler)
                if (self.matrix_fail[i, j] != 0):
                    pygame.draw.circle(self.screen, RED, (j * self.scaler + self.scaler/2, i * self.scaler + self.scaler/2), self.radius)
                    self.objectsx.append(j * self.scaler + self.scaler/2)
                    self.objectsy.append(i * self.scaler + self.scaler/2)
    
    '''def collision(self):
        flag = False
        for i in self.objectsx:
            for j in self.objectsy:
                if self.x <= self.objectsx[i] + 20 and self.x >= self.objectsx[i]:
                    if self.y <= self.'''

    def izq(self):
        print("iz")
        self.x += - self.step * self.scaler
        if self.x < 0:
            self.piso += 1 
            self.y += - self.scaler
            self.x += self.step * self.scaler
        print(self.x)
        print(self.y)
        print(self.piso)
        self.draw_base()
        self.draw_fail()
        self.draw_goal()    
        self.draw_cha()
        self._update()
        self.step = 0
    
    def der(self):
        print("de")
        self.x += self.step * self.scaler
        if self.x > 450:
            self.piso += 1 
            self.y += - self.scaler 
            self.x += - self.step * self.scaler
        print(self.x)
        print(self.y)
        print(self.piso)
        self.draw_base()
        self.draw_fail()
        self.draw_goal()    
        self.draw_cha()
        self._update()
        self.step = 0

    def actions(self, direction):
        if direction == Direction.ENTER:
            print("enter")
            self.step = random.randint(1, 2)
            self.steps = self.steps + self.step
            self.draw_text(str(self.step), 625, 200)
            self._update()
            self.direction = Direction.UP
        if self.step != 0:
            if direction == Direction.LEFT:
                if self.piso % 2 == 0:
                    self.izq()
                else:
                    self.der()
            if direction == Direction.RIGHT:
                if self.piso % 2 == 0:
                    self.der()
                else:
                    self.izq()
    
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.direction = Direction.ENTER
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
    
        self.actions(self.direction)
        game_over = False
        return game_over
        

    def _update(self):
        # Actualiza la pantalla Pygame
        pygame.display.update()

# Espera a que el usuario cierre la ventana Pygame
if __name__ == '__main__':
    game = SL()
    while True:
        game_over = game.play_step()
        if game_over == True:
            break

    pygame.quit()
