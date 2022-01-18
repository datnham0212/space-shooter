import pygame as pg
import window
import laser

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

    def draw(self):
        #Constantly draw lasers
        for laser in self.lasers:
            laser.draw(self.screen)

    def move(self, keys):
        #TIRL multiple ifs allow you to check for multiple conditions at once
        if keys[pg.K_LEFT] and self.x > 0:
            self.x -= self.velocity
        
        if keys[pg.K_RIGHT] and self.x < window.WIDTH - self.width:
            self.x += self.velocity
        
        if keys[pg.K_UP] and self.y > 0:
            self.y -= self.velocity
        
        if keys[pg.K_DOWN] and self.y < window.HEIGHT - self.height:
            self.y += self.velocity
        
        #Continuously move lasers
        for laser in self.lasers:
            laser.move()
        
        #Remove lasers that have gone off the screen
        self.lasers = [laser for laser in self.lasers if laser.y > 0]
    
    def default_shot(self): 
        #Return the current time since running the program
        current_time = pg.time.get_ticks()
        
        #If the time since the last laser is greater than the cooldown, shoot a new laser
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
        