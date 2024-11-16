import pygame as pg
import time
from enemy import BossEnemy

def check_collisions(player, enemies, meteors, enemy_lasers, pickup_manager):
    # Define invincibility duration (in seconds)
    invincibility_duration = 2

    # Get the current time
    current_time = time.time()

    # Player being hit by enemy
    player_rect = pg.Rect(player.x, player.y, player.width, player.height)
    
    for enemy in enemies:
        enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        if player_rect.colliderect(enemy_rect):
            if current_time - player.last_hit_time > invincibility_duration:
                player.max_lives -= 1
                player.last_hit_time = current_time  # Update last hit time
                player.damage_sound.play()  # Play damage sound
                
                if player.max_lives == 0:
                    return False  # Indicate game over
                
                # Do not remove the enemy
                break
    
    # Player being hit by meteor
    for meteor in meteors:
        meteor_rect = pg.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
        if player_rect.colliderect(meteor_rect):
            if current_time - player.last_hit_time > invincibility_duration:
                player.max_lives -= 1
                player.last_hit_time = current_time  # Update last hit time
                player.damage_sound.play()  # Play damage sound
                
                if player.max_lives == 0:
                    return False  # Indicate game over
                
                # Do not remove the meteor
                break
    
    # Player being hit by enemy's laser
    for laser in enemy_lasers:
        laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
        if player_rect.colliderect(laser_rect):
            if current_time - player.last_hit_time > invincibility_duration:
                player.max_lives -= 1
                player.last_hit_time = current_time  # Update last hit time
                player.damage_sound.play()  # Play damage sound
                
                if player.max_lives == 0:
                    return False  # Indicate game over
                
                enemy_lasers.remove(laser)
                break

    # Enemy being hit by player's laser
    for laser in player.lasers:
        laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
        for enemy in enemies:
            enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if laser_rect.colliderect(enemy_rect):
                points, remove_enemy = enemy.take_damage()
                if points:
                    player.scores += points
                    # Create a pickup at the enemy's position
                    pickup_manager.create_pickup(enemy.x, enemy.y, "extra_lives")
                if remove_enemy:
                    enemies.remove(enemy)
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

                player.lasers.remove(laser)
                break

    # Player collecting pickups
    for pickup in pickup_manager.get_pickups():
        if player_rect.colliderect(pickup.rect):
            pickup.apply(player)
            pickup_manager.get_pickups().remove(pickup)
            break
    
    return True  # Indicate game is still running