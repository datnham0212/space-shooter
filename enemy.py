import pygame as pg

class Enemy:

    def __init__(self, screen, x):
        self.screen = screen
        self.grunt1Image = pg.image.load("assets/ship1.png")
        self.x = x
        self.y = 0 # <= 200
        self.velocity = 2
        self.width = 70
        self.height = 70
    
    def drawGrunt1(self, screen):
        screen.blit(self.grunt1Image, (self.x, self.y))

    def move(self):
        self.y += self.velocity
