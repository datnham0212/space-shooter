import pygame as pg
def check_collisions(self):
        #Player being hit by enemy
        player_rect = pg.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for enemy in self.enemies:
            enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                self.player.max_lives -= 1
                
                if self.player.max_lives == 0:
                    self.running = False
                
                self.enemies.remove(enemy)
                break
                # Handle hit (e.g. play sound, etc.)
        
        #Player being hit by meteor
        for meteor in self.meteors:
            meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
            if player_rect.colliderect(meteor_rect):
                self.player.max_lives -= 1
                
                if self.player.max_lives == 0:
                    self.running = False
                
                self.enemies.remove(enemy)
                break
                
        
        #Player being hit by enemy's laser
        for enemy in self.enemies:
            for laser in enemy.lasers:
                laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
                if player_rect.colliderect(laser_rect):
                    self.player.max_lives -= 1
                    enemy.lasers.remove(laser)
                    
                    if self.player.max_lives == 0:
                        self.running = False
                        print("Game Over")
                    
                    break

        #Enemy being hit
        for laser in self.player.lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            for enemy in self.enemies:
                enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if laser_rect.colliderect(enemy_rect):
                    if enemy.take_damage():
                        self.enemies.remove(enemy)
                        self.player.scores += 100
                    self.player.lasers.remove(laser)
        
        #Meteor being hit by player's laser
        for laser in self.player.lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            for meteor in self.meteors:
                meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
                if laser_rect.colliderect(meteor_rect):
                    if meteor.take_damage():
                        self.meteors.remove(meteor)
                        self.player.scores += 100
                    self.player.lasers.remove(laser)