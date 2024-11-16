import pygame as pg
from pickups import ExtraLives
import random

class ManagePickups:
    def __init__(self, screen):
        self.screen = screen
        self.pickups = pg.sprite.Group()

    def create_pickup(self, x, y, pickup_type="extra_lives"):
        if pickup_type == "extra_lives":
            if random.random() < 0.15:  # 15% chance to create an extra life pickup
                pickup = ExtraLives(x, y)
                self.pickups.add(pickup)

    def update_pickups(self):
        self.pickups.update()

    def draw_pickups(self):
        self.pickups.draw(self.screen)

    def get_pickups(self):
        return self.pickups