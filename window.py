import pygame as pg
import menu
import player 
import enemy
import collisions_handling

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

        self.player = player.Player(self.screen)
        self.enemy_manager = enemy.ManageEnemies(self.screen)

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

        pg.display.set_caption("Space Shooter")

        self.run()
    
    def handle_menu(self, menu_type):
        menu_map = {
            "start": self.start_menu,
            "pause": self.pause_menu,
            "options": self.options_menu,
            "sound": self.sound_menu,
            "controls": self.controls_menu,
            "difficulty": self.difficulty_menu
        }
        menu = menu_map[menu_type]
        menu.draw()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = menu.handle_input(event)
            
            if menu_type == "start":
                if action == "Start Game":
                    self.in_start_menu = False
                elif action == "Options":
                    self.in_start_menu = False
                    self.in_options_menu = True
                elif action == "Quit":
                    self.running = False
                    
            elif menu_type == "pause":
                if action == "Resume Game":
                    self.in_pause_menu = False
                elif action == "Return to Start Menu":
                    self.reset_game()
                    self.in_pause_menu = False
                    self.in_start_menu = True
            
            elif menu_type == "options":
                if action == "Return to Start Menu":
                    self.in_options_menu = False
                    self.in_start_menu = True
                elif action in ["Sound", "Controls", "Difficulty"]:
                    self.in_options_menu = False
                    setattr(self, f'in_{action.lower()}_menu', True)

            elif menu_type in ["sound", "controls", "difficulty"]:
                if action == "Return to Options":
                    setattr(self, f'in_{menu_type}_menu', False)
                    self.in_options_menu = True

        pg.display.update()
    
    def run(self):
        clock = pg.time.Clock()
        while self.running:
            if self.in_start_menu:
                self.handle_menu("start")
            elif self.in_pause_menu:
                self.handle_menu("pause")
            elif self.in_options_menu:
                self.handle_menu("options")
            elif self.in_sound_menu:
                self.handle_menu("sound")
            elif self.in_controls_menu:
                self.handle_menu("controls")
            elif self.in_difficulty_menu:
                self.handle_menu("difficulty")
            else:
                if not collisions_handling.check_collisions(self.player, self.enemy_manager.enemies, self.enemy_manager.meteors):
                    self.running = False
                
                self.handle_background()
                self.handle_events()
                self.constant_update_movements()
                self.initialize_screen()

            clock.tick(60)  # Ensure 60fps
        pg.quit()
    

    def reset_game(self):
        self.player = player.Player(self.screen)
        self.enemies = []
        self.meteors = []
        self.previous_spawn_time = 0
    
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
        self.enemy_manager.move_enemies()
        self.handle_shooting(keys)

    def initialize_screen(self):
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        self.player.draw()
        self.player.generate_lives()
        self.player.increase_scores()
        self.enemy_manager.generate_enemies()  # Use enemy manager to generate enemies
        self.enemy_manager.draw_enemies()  # Use enemy manager to draw enemies
        pg.display.update()
    
    def handle_shooting(self, keys):
        if keys[pg.K_z]:
            self.player.default_shot()
        
        for enemy in self.enemy_manager.enemies:
            enemy.enemy_shoot()

    
