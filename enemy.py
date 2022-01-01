import pygame as pg

class Enemy:

    def __init__(self, screen, x):
        self.screen = screen
        self.x = x
        self.y = 0 # <= 200
        self.velocity = 2
        self.width = 50
        self.height = 50

    def draw(self):
        points = [
            (self.x + self.width / 2, self.y + self.height),
            (self.x , self.y),
            (self.x + self.width, self.y)
        ]
        pg.draw.polygon(self.screen, (255, 0, 0), points)

    def move(self):
        self.y += self.velocity
