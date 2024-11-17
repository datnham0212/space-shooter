import pygame as pg
from pickups import ExtraLives, TripleShots
import random

class ManagePickups:
    def __init__(self, screen):
        self.screen = screen
        self.pickups = pg.sprite.Group()

    def create_pickup(self, x, y, pickup_type="extra_lives"):
        if pickup_type == "extra_lives":
            # if random.random() < 0.2:  # 20% chance to create an extra life pickup
                pickup = ExtraLives(x, y)
        
        elif pickup_type == "triple_shot":
            # if random.random() < 0.5:  # 50% chance to create a triple shot pickup
                pickup = TripleShots(x, y)
        
        self.pickups.add(pickup)

    def update_pickups(self):
        self.pickups.update()

    def draw_pickups(self):
        self.pickups.draw(self.screen)

    def get_pickups(self):
        return self.pickups