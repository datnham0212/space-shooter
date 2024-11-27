import pygame as pg
import random
import window
from enemies import BasicEnemy, FastEnemy, StrongEnemy, Meteor, BossEnemy

class ManageEnemies:
    def __init__(self, screen, player, difficulty="Normal"):
        self.screen = screen
        self.player = player  # Store the player instance
        self.enemies = []
        self.meteors = []
        self.enemy_lasers = []
        self.previous_spawn_time = 0
        self.difficulty = difficulty
        self._set_difficulty_parameters()
        self.score_threshold = 1000  # Points threshold for increasing difficulty
        self.difficulty_increment = 0  # Track how many times difficulty has been increased

    def generate_enemies(self):
        current_spawn_time = pg.time.get_ticks()
        boss_present = any(isinstance(enemy, BossEnemy) for enemy in self.enemies)

        if not boss_present:
            if current_spawn_time - self.previous_spawn_time >= 1.5 * self.enemy_cooldown:
                if random.random() < self.enemy_spawn_chance:  # Chance to spawn an enemy
                    if random.random() < 0.2:  # 20% chance to spawn a line of fast enemies
                        self.spawn_fast_enemy_line()
                    else:
                        enemy_type = random.choice([BasicEnemy, StrongEnemy])
                        new_enemy = enemy_type(self.screen, random.randrange(50, 900))
                        self.enemies.append(new_enemy)
                else:  # Chance to spawn a meteor
                    if random.random() < self.meteor_spawn_chance:
                        new_meteor = Meteor(self.screen, random.randrange(50, 900))
                        self.meteors.append(new_meteor)
                self.previous_spawn_time = current_spawn_time

        # Spawn boss if score threshold is met
        if self.player.logic.scores % 1000 == 0 and self.player.logic.scores != 0 and not boss_present:
            self.spawn_boss()

    def _set_difficulty_parameters(self):
        if self.difficulty == "Easy":
            self.enemy_cooldown = 3000
            self.enemy_spawn_chance = 0.7
            self.meteor_spawn_chance = 0.3
        elif self.difficulty == "Hard":
            self.enemy_cooldown = 1000
            self.enemy_spawn_chance = 0.9
            self.meteor_spawn_chance = 0.5
        else:  # Normal difficulty
            self.enemy_cooldown = 2000
            self.enemy_spawn_chance = 0.8
            self.meteor_spawn_chance = 0.7

    def spawn_fast_enemy_line(self):
        start_x = random.randrange(50, 900 - 6 * 70)  # Ensure the line fits within the screen width
        for i in range(10):
            new_enemy = FastEnemy(self.screen, start_x + i * 70)
            self.enemies.append(new_enemy)

    def spawn_boss(self):
        boss = BossEnemy(self.screen)
        self.enemies.append(boss)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
            new_laser = enemy.enemy_shoot()
            if new_laser:
                self.enemy_lasers.append(new_laser)
        for meteor in self.meteors:
            meteor.move()

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for meteor in self.meteors:
            meteor.draw(self.screen)
        for laser in self.enemy_lasers:
            laser.draw(self.screen)

    def move_lasers(self):
        for laser in self.enemy_lasers:
            laser.enemy_laser_move()
        self.enemy_lasers = [laser for laser in self.enemy_lasers if laser.y < window.HEIGHT]

    def adjust_difficulty(self, player_score):
        # Increase difficulty every 1000 points
        if player_score // self.score_threshold > self.difficulty_increment:
            self.difficulty_increment += 1
            for enemy in self.enemies:
                enemy.velocity += 1  # Increase enemy speed
                enemy.cooldown = max(100, enemy.cooldown - 100)  # Decrease cooldown, but not below 100ms