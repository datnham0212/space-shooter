import pygame as pg
import window
import laser
import time

import json
import os
import pygame as pg

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load("assets/player.png")
        self.x = 240
        self.y = 400
        self.velocity = 6
        self.width = 70
        self.height = 70
        self.lasers = []
        self.last_time = 0
        self.cooldown = 200
        self.max_lives = 3
        self.lives = []
        self.scores = 0
        self.last_hit_time = 0  # Initialize the hit time
        self.invincibility_duration = 2  # Duration of invincibility in seconds
        self.damage_sound = pg.mixer.Sound("sounds/damage_taken.mp3")  # Load the damage sound
        self.damage_sound.set_volume(window.sound_settings['volume'] / 100.0 if window.sound_settings["sound_on"] else 0)
        self.key_bindings = self.load_key_bindings()

    def load_key_bindings(self):
        if os.path.exists("key_bindings.json"):
            with open("key_bindings.json", "r") as file:
                key_bindings = json.load(file)
                return {action: getattr(pg, key) for action, key in key_bindings.items()}
        else:
            return {
                "Up": pg.K_UP,
                "Down": pg.K_DOWN,
                "Left": pg.K_LEFT,
                "Right": pg.K_RIGHT,
                "Shoot": pg.K_z,
                "Pause": pg.K_RETURN
            }

    def save_key_bindings(self):
        key_bindings = {
            action: f"K_{pg.key.name(key).lower()}" if pg.K_a <= key <= pg.K_z else f"K_{pg.key.name(key).upper()}"
            for action, key in self.key_bindings.items()
        }
        with open("key_bindings.json", "w") as file:
            json.dump(key_bindings, file, indent=4)


    def update_key_bindings(self, new_bindings):
        self.key_bindings.update(new_bindings)
        self.save_key_bindings()

    def draw(self):
        # Constantly draw lasers
        for laser in self.lasers:
            laser.draw(self.screen)

        # Handle flickering effect during invincibility
        current_time = time.time()
        if current_time - self.last_hit_time < self.invincibility_duration:
            # Flicker effect: show/hide the player sprite every 50ms
            if int(current_time * 20) % 2 == 0:
                self.screen.blit(self.image, (self.x, self.y))
        else:
            # Draw the player sprite normally
            self.screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[self.key_bindings["Left"]] and self.x > 0:
            self.x -= self.velocity
        
        if keys[self.key_bindings["Right"]] and self.x < window.WIDTH - self.width:
            self.x += self.velocity
        
        if keys[self.key_bindings["Up"]] and self.y > 0:
            self.y -= self.velocity
        
        if keys[self.key_bindings["Down"]] and self.y < window.HEIGHT - self.height:
            self.y += self.velocity
        
        # Continuously move lasers
        for laser in self.lasers:
            laser.move()
        
        # Remove lasers that have gone off the screen
        self.lasers = [laser for laser in self.lasers if laser.y > 0]
    
    def default_shot(self): 
        current_time = pg.time.get_ticks()
        
        if current_time - self.last_time >= self.cooldown:
            new_laser = laser.Laser(self.x + self.width / 2 - 2, self.y)  # Adjust x position for laser center
            self.lasers.append(new_laser)
            self.last_time = current_time

    def generate_lives(self):
        self.lives.clear()
        margin = 10
        for i in range(self.max_lives):
            self.lives.append(pg.image.load("assets/heart.png"))
            self.screen.blit(self.lives[i], (margin, 10))
            margin += 40
    
    def increase_scores(self):
        font = pg.font.Font(None, 36)
        text = font.render(f"Scores: {self.scores}", True, (255, 255, 255))
        self.screen.blit(text, (int(window.WIDTH/2)-50, 10))