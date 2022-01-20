import pygame as pg
import menu
import player 
import enemy
import random

WIDTH = 960
HEIGHT = 640

class Window:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
        self.background = pg.image.load("assets/background.jpg")
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_x = 0
        self.background_y = 0
        self.background_y_speed = 1

        self.running = True
        self.in_start_menu = True
        self.start_menu = menu.StartMenu(self.screen)

        self.in_pause_menu = False
        self.pause_menu = menu.PauseMenu(self.screen)

        self.in_options_menu = False
        self.options_menu = menu.OptionsMenu(self.screen)
        self.in_sound_menu = False
        self.sound_menu = menu.SoundMenu(self.screen)
        self.in_controls_menu = False
        self.controls_menu = menu.ControlsMenu(self.screen)
        self.in_difficulty_menu = False
        self.difficulty_menu = menu.DifficultyMenu(self.screen)

        #Can be used for resetting the game
        self.player = player.Player(self.screen)
        self.enemies = []   
        self.meteors = []
        self.previous_spawn_time = 0

        self.enemy_cooldown = 2000

        pg.display.set_caption("Space Shooter")

        self.run()
    
    def run(self):
        clock = pg.time.Clock()

        while self.running:
            if self.in_start_menu:
                self.handle_start_menu()

            elif self.in_pause_menu:
                self.handle_pause_menu()
            
            elif self.in_options_menu:
                self.handle_options_menu()
            
            elif self.in_sound_menu:
                self.handle_sound_menu()

            elif self.in_controls_menu:
                self.handle_controls_menu()

            elif self.in_difficulty_menu:
                self.handle_difficulty_menu()
            
            else:
                self.handle_background()
                self.check_collisions()
                self.handle_events()
                self.constant_update_movements()
                self.initialize_screen()

            clock.tick(60) # Ensure 60fps
        
        pg.quit()
    
    def handle_start_menu(self):
        self.start_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.start_menu.handle_input(event)
            if action == "Start Game":
                self.in_start_menu = False
            elif action == "Options":
                self.in_start_menu = False
                self.in_options_menu = True
            elif action == "Quit":
                self.running = False
        pg.display.update()
    
    def handle_pause_menu(self):
        self.pause_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.pause_menu.handle_input(event)
            if action == "Resume Game":
                self.in_pause_menu = False
            elif action == "Return to Start Menu":
                self.reset_game()
                self.in_pause_menu = False
                self.in_start_menu = True
        pg.display.update()

    def reset_game(self):
        self.player = player.Player(self.screen)
        self.enemies = []
        self.meteors = []
        self.previous_spawn_time = 0

    def handle_options_menu(self):
        self.options_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.options_menu.handle_input(event)
            if action == "Return to Start Menu":
                self.in_options_menu = False
                self.in_start_menu = True
            
            elif action == "Sound":
                self.in_options_menu = False
                self.in_sound_menu = True
            
            elif action == "Controls":
                self.in_options_menu = False
                self.in_controls_menu = True

            elif action == "Difficulty":
                self.in_options_menu = False
                self.in_difficulty_menu = True

        pg.display.update()

    def handle_sound_menu(self):
        self.sound_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.sound_menu.handle_input(event)
            if action == "Return to Options":
                self.in_sound_menu = False
                self.in_options_menu = True
        pg.display.update()

    def handle_controls_menu(self):
        self.controls_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.controls_menu.handle_input(event)
            if action == "Return to Options":
                self.in_controls_menu = False
                self.in_options_menu = True
        pg.display.update()

    def handle_difficulty_menu(self):
            self.difficulty_menu.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                action = self.difficulty_menu.handle_input(event)
                if action == "Return to Options":
                    self.in_difficulty_menu = False
                    self.in_options_menu = True
            pg.display.update()
    
    def handle_background(self):
        self.background_y += self.background_y_speed
        if self.background_y == HEIGHT:
            self.background_y = 0
        
        self.screen.blit(self.background, (self.background_x, self.background_y))
        self.screen.blit(self.background, (0, self.background_y - HEIGHT))
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.in_pause_menu = True

    def constant_update_movements(self):
        keys = pg.key.get_pressed()
        self.player.move(keys)
        self.move_enemies()
        self.handle_shooting(keys)

    def initialize_screen(self):
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        self.player.draw()
        self.player.generate_lives()
        self.player.increase_scores()
        self.generate_enemies()
        pg.display.update()

    def generate_enemies(self):
        current_spawn_time = pg.time.get_ticks()
        if current_spawn_time - self.previous_spawn_time >= 1.5*self.enemy_cooldown:
            if random.random() < 0.5:
                new_enemy = enemy.Enemy(self.screen, random.randrange(50,900))
                self.enemies.append(new_enemy)
            else:
                new_meteors = enemy.Meteor(self.screen, random.randrange(50,900))
                self.meteors.append(new_meteors)
            self.previous_spawn_time = current_spawn_time

        self.draw_enemies()
    
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
        
        for meteor in self.meteors:
            meteor.move()

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)

        for meteor in self.meteors:
            meteor.draw(self.screen)
    
    def handle_shooting(self, keys):
        if keys[pg.K_z]:
            self.player.default_shot()
        
        for enemy in self.enemies:
            enemy.enemy_shoot()

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
