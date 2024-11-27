import pygame as pg
import window
import time
from manage_player import ManagePlayer

class Player:
    IMAGE_PATH = "assets/player.png"
    DAMAGE_SOUND_PATH = "sounds/damage_taken.mp3"
    FONT_SIZE = 36

    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load(self.IMAGE_PATH)
        self.logic = ManagePlayer()
        self.damage_sound = pg.mixer.Sound(self.DAMAGE_SOUND_PATH)
        self.damage_sound.set_volume(window.sound_settings['volume'] / 100.0 if window.sound_settings["sound_on"] else 0)
        self.font = pg.font.Font(None, self.FONT_SIZE)
        self.key_bindings = self.logic.key_bindings  # Expose key_bindings from ManagePlayer

    def draw(self):
        self.draw_lasers()
        self.draw_player()

    def draw_lasers(self):
        for laser in self.logic.lasers:
            laser.draw(self.screen)

    def draw_player(self):
        current_time = time.time()
        if current_time - self.logic.last_hit_time < self.logic.invincibility_duration:
            if int(current_time * 20) % 2 == 0:
                self.screen.blit(self.image, (self.logic.x, self.logic.y))
        else:
            self.screen.blit(self.image, (self.logic.x, self.logic.y))

    def move(self, keys):
        self.logic.move_player(keys)
        self.logic.move_lasers()

    def laser_shot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.logic.last_time >= self.logic.cooldown:
            self.logic.shoot_lasers()
            self.logic.last_time = current_time

    def update(self):
        self.logic.move_lasers()

    def generate_lives(self):
        self.logic.generate_lives()
        margin = 10
        for life in self.logic.lives:
            self.screen.blit(life, (margin, 10))
            margin += 40

    def increase_scores(self):
        text = self.font.render(f"Scores: {self.logic.scores}", True, (255, 255, 255))
        self.screen.blit(text, (int(window.WIDTH / 2) - 50, 10))

    def draw_ammo(self):
        if self.logic.triple_shot:
            ammo_text = self.font.render(f"{self.logic.triple_shot_ammo}", True, (255, 255, 255))
            text_rect = ammo_text.get_rect(topright=(self.screen.get_width() - 10, 10))
            self.screen.blit(ammo_text, text_rect)

    def check_collisions(self, enemies, meteors, enemy_lasers, pickup_manager):
        return self.logic.check_collisions(enemies, meteors, enemy_lasers, pickup_manager)