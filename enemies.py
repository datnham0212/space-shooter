import pygame as pg
import random
import laser

class Enemy:
    def __init__(self, screen, x, y=0, velocity=2, width=120, height=120, cooldown_range=(100, 200), damage_threshold=3, points=100):
        self.screen = screen
        self.x = x
        self.y = y
        self.velocity = velocity
        self.width = width
        self.height = height
        self.damage = 0
        self.last_time = 0
        self.cooldown = random.randint(*cooldown_range)
        self.spawn_time = pg.time.get_ticks()
        self.damage_threshold = damage_threshold
        self.points = points
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.velocity

    def enemy_shoot(self):
        current_time = pg.time.get_ticks()
        delay = random.randint(200, 3000)
        if current_time - self.spawn_time < delay:
            return None

        if current_time - self.last_time >= self.cooldown:
            laser_x = self.x + self.width / 2 - 2.5  # Center the laser horizontally
            laser_y = self.y + self.height  # Position the laser at the bottom of the enemy
            new_laser = laser.Laser(laser_x, laser_y)
            self.last_time = current_time
            self.cooldown = random.randint(500, 2000)
            return new_laser
        return None

    def take_damage(self):
        self.damage += 1
        if self.damage >= self.damage_threshold:
            return self.points, True  # Return points and a flag indicating the enemy should be removed
        return 0, False  # Return 0 points and a flag indicating the enemy should not be removed

class BasicEnemy(Enemy):
    def __init__(self, screen, x):
        super().__init__(screen, x, points=100)
        self.image = pg.image.load("assets/ship1.png")

class FastEnemy(Enemy):
    def __init__(self, screen, x):
        super().__init__(screen, x, velocity=3, width=80, height=80, cooldown_range=(200, 400), damage_threshold=1, points=100)
        self.image = pg.image.load("assets/ship2.png")

class StrongEnemy(Enemy):
    def __init__(self, screen, x):
        super().__init__(screen, x, velocity=2, width=180, height=180, cooldown_range=(400, 1000), damage_threshold=5, points=200)
        self.image = pg.image.load("assets/ship3.png")

class BossEnemy(Enemy):
    def __init__(self, screen):
        super().__init__(screen, x=(screen.get_width() - 140) // 2, y=70, velocity=0, width=140, height=140, cooldown_range=(500, 1000), damage_threshold=20, points=300)
        self.image = pg.image.load("assets/bossship.png")
        self.health = 20  # Boss health
        self.direction = random.choice([-1, 1])  # Initial direction: -1 for left, 1 for right
        self.move_interval = random.randint(2000, 5000)  # Time interval for changing direction
        self.last_move_time = pg.time.get_ticks()  # Last time the boss changed direction

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            return self.points, True  # Return points and a flag indicating the boss should be removed
        return 0, False  # Return 0 points and a flag indicating the boss should not be removed

    def move(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_move_time >= self.move_interval:
            self.direction = random.choice([-1, 1])  # Change direction
            self.last_move_time = current_time
            self.move_interval = random.randint(2000, 5000)  # Reset move interval

        self.x += self.direction * 2  # Move the boss left or right

        # Ensure the boss stays within screen bounds
        if self.x < 0:
            self.x = 0
            self.direction = 1
        elif self.x + self.width > self.screen.get_width():
            self.x = self.screen.get_width() - self.width
            self.direction = -1

class Meteor:
    def __init__(self, screen, x):
        self.screen = screen
        self.image = pg.image.load("assets/meteor1.png")
        self.x = x
        self.y = 0
        self.velocity = 3
        self.width = 180
        self.height = 180
        self.damage = 0
        self.angle = 0  # Initialize the rotation angle

    def draw(self, screen):
        self.angle += 1  # Increment the rotation angle
        rotated_image = pg.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

    def move(self):
        self.y += self.velocity

    def take_damage(self):
        self.damage += 1
        if self.damage >= 6:
            return 300  # Example points for destroying a meteor
        return 0