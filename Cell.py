import pygame
import random

class Cell():
    def reset_to_defaults(self):
        self.set_dead()
        self.x = self.default_x
        self.y = self.default_y
        self.width = self.default_width
        self.height = self.default_height
        self.translated_x = self.default_x
        self.translated_y = self.default_y
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def set_dead(self):
        if self.state != "dead":
            self.state = "dead"
            self.color = self.default_color
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def set_alive(self):
        if self.state != "alive":
            self.state = "alive"
            self.color = (random.randint(0, 255),0,random.randint(0, 255))
            # self.color = (255, 255, 255)
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def __init__(self, x, y, w, h, color, screen):
        self.default_x = x
        self.default_y = y
        self.default_width = w
        self.default_height = h
        self.default_color = color
        self.translated_x = x
        self.translated_y = y
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.color = color
        self.state = "dead"
        self.number_of_alive_neightbours = 0
        self.screen = screen
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))