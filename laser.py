import pygame as pg

class Laser:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.color = (255, 255, 255)
        self.velocity = 7
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y -= self.velocity