import pygame as pg
import window
import laser

class Player:

    def __init__(self, screen):
        self.screen = screen
        self.x = 240
        self.y = 400
        self.velocity = 6
        self.width = 30
        self.height = 30
        self.lasers = []
        self.last_time = 0
        self.cooldown = 200
    
    def draw(self):
        points = [
            (self.x + self.width / 2, self.y),  # Top vertex
            (self.x + self.width, self.y + self.height),  # Bottom-right vertex
            (self.x , self.y + self.height)  # Bottom-left vertex
        ]
        pg.draw.polygon(self.screen, (255, 255, 255), points)

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
