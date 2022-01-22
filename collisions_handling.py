import pygame as pg

def check_collisions(player, enemies, meteors):
    # Player being hit by enemy
    player_rect = pg.Rect(player.x, player.y, player.width, player.height)
    
    for enemy in enemies:
        enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        if player_rect.colliderect(enemy_rect):
            player.max_lives -= 1
            
            if player.max_lives == 0:
                return False  # Indicate game over
            
            enemies.remove(enemy)
            break
    
    # Player being hit by meteor
    for meteor in meteors:
        meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
        if player_rect.colliderect(meteor_rect):
            player.max_lives -= 1
            
            if player.max_lives == 0:
                return False  # Indicate game over
            
            meteors.remove(meteor)
            break
    
    # Player being hit by enemy's laser
    for enemy in enemies:
        for laser in enemy.lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            if player_rect.colliderect(laser_rect):
                player.max_lives -= 1
                enemy.lasers.remove(laser)
                
                if player.max_lives == 0:
                    return False  # Indicate game over
                
                break

    # Enemy being hit by player's laser
    for laser in player.lasers:
        laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
        for enemy in enemies:
            enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if laser_rect.colliderect(enemy_rect):
                if enemy.take_damage():
                    enemies.remove(enemy)
                    player.scores += 100
                player.lasers.remove(laser)
                break
    
    # Meteor being hit by player's laser
    for laser in player.lasers:
        laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
        for meteor in meteors:
            meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
            if laser_rect.colliderect(meteor_rect):
                if meteor.take_damage():
                    meteors.remove(meteor)
                    player.scores += 100
                player.lasers.remove(laser)
                break
    
    return True  # Indicate game is still running
