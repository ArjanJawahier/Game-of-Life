import pygame
import random

class Cell():
    def set_dead(self):
        self.state = "dead"
        self.color = self.defaultcolor

    def set_alive(self):
        self.state = "alive"
        self.color = (random.randint(0, 255),0,0)

    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.defaultcolor = color
        self.color = color
        self.state = "dead"
        self.number_of_alive_neightbours = 0