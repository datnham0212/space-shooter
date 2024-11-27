import pygame as pg
import json
import os
import laser
import window
import time
import random

class ManagePlayer:
    INITIAL_X = 240
    INITIAL_Y = 400
    VELOCITY = 6
    WIDTH = 70
    HEIGHT = 70
    COOLDOWN = 200  # milliseconds
    MAX_LIVES = 3
    INVINCIBILITY_DURATION = 2  # seconds
    HEART_IMAGE_PATH = "assets/heart.png"

    def __init__(self):
        self.x = self.INITIAL_X
        self.y = self.INITIAL_Y
        self.velocity = self.VELOCITY
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.lasers = []
        self.last_time = 0
        self.cooldown = self.COOLDOWN
        self.triple_shot = False
        self.triple_shot_ammo = 0
        self.max_lives = self.MAX_LIVES
        self.lives = []
        self.scores = 0
        self.last_hit_time = 0
        self.invincibility_duration = self.INVINCIBILITY_DURATION
        self.key_bindings = self.load_key_bindings()
        self.damage_sound = pg.mixer.Sound(window.DAMAGE_SOUND)

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

    def update_sound_volumes(self, volume):
        self.damage_sound.set_volume(volume)

    def move_player(self, keys):
        if keys[self.key_bindings["Left"]] and self.x > 0:
            self.x -= self.velocity
        if keys[self.key_bindings["Right"]] and self.x < window.WIDTH - self.width:
            self.x += self.velocity
        if keys[self.key_bindings["Up"]] and self.y > 0:
            self.y -= self.velocity
        if keys[self.key_bindings["Down"]] and self.y < window.HEIGHT - self.height:
            self.y += self.velocity

    def move_lasers(self):
        for laser in self.lasers:
            laser.move()
        self.lasers = [laser for laser in self.lasers if laser.y > 0]

    def shoot_lasers(self):
        if self.triple_shot and self.triple_shot_ammo > 0:
            self.shoot_triple_lasers()
            self.triple_shot_ammo -= 1
            if self.triple_shot_ammo == 0:
                self.triple_shot = False
        else:
            self.shoot_single_laser()

    def shoot_triple_lasers(self):
        new_laser1 = laser.Laser(self.x + self.width / 2 - 15, self.y)
        new_laser2 = laser.Laser(self.x + self.width / 2 - 2, self.y)
        new_laser3 = laser.Laser(self.x + self.width / 2 + 11, self.y)
        self.lasers.extend([new_laser1, new_laser2, new_laser3])

    def shoot_single_laser(self):
        new_laser = laser.Laser(self.x + self.width / 2 - 2, self.y)
        self.lasers.append(new_laser)

    def generate_lives(self):
        self.lives.clear()
        for i in range(self.max_lives):
            self.lives.append(pg.image.load(self.HEART_IMAGE_PATH))

    def check_collisions(self, enemies, meteors, enemy_lasers, pickup_manager):
        current_time = time.time()
        player_rect = pg.Rect(self.x, self.y, self.width, self.height)

        # Player being hit by enemy
        for enemy in enemies:
            enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                if current_time - self.last_hit_time > self.invincibility_duration:
                    self.max_lives -= 1
                    self.last_hit_time = current_time
                    self.damage_sound.play()
                    if self.max_lives == 0:
                        return False
                    break

        # Player being hit by meteor
        for meteor in meteors:
            meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
            if player_rect.colliderect(meteor_rect):
                if current_time - self.last_hit_time > self.invincibility_duration:
                    self.max_lives -= 1
                    self.last_hit_time = current_time
                    self.damage_sound.play()
                    if self.max_lives == 0:
                        return False
                    break

        # Player being hit by enemy's laser
        for laser in enemy_lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            if player_rect.colliderect(laser_rect):
                if current_time - self.last_hit_time > self.invincibility_duration:
                    self.max_lives -= 1
                    self.last_hit_time = current_time
                    self.damage_sound.play()
                    if self.max_lives == 0:
                        return False
                    enemy_lasers.remove(laser)
                    break

        # Enemy being hit by player's laser
        for laser in self.lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            for enemy in enemies:
                enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if laser_rect.colliderect(enemy_rect):
                    points, remove_enemy = enemy.take_damage()
                    if points:
                        self.scores += points
                        pickup_type = "extra_lives" if random.random() < 0.5 else "triple_shot"
                        pickup_manager.create_pickup(enemy.x, enemy.y, pickup_type)
                    if remove_enemy:
                        enemies.remove(enemy)
                    self.lasers.remove(laser)
                    break

        # Meteor being hit by player's laser
        for laser in self.lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            for meteor in meteors:
                meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
                if laser_rect.colliderect(meteor_rect):
                    if meteor.take_damage():
                        meteors.remove(meteor)
                    self.lasers.remove(laser)
                    break

        # Player collecting pickups
        for pickup in pickup_manager.get_pickups():
            if player_rect.colliderect(pickup.rect):
                pickup.apply(self)
                pickup_manager.get_pickups().remove(pickup)
                break

        return True