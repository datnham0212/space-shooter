import pygame as pg
from pygame import mixer

import manage_pickups
import menu
import player
import manage_enemies
from leaderboard import Leaderboard

# Constants
WIDTH = 960
HEIGHT = 640
FPS = 60
BACKGROUND_IMG = "assets/background.jpg"
BACKGROUND_MUSIC = 'sounds/bg.mp3'
SHOT_SOUND = 'sounds/shot.wav'
DAMAGE_SOUND = 'sounds/damage_taken.mp3'
MOVE_SOUND = 'sounds/ST0E_U0_00004.wav'
SELECT_SOUND = 'sounds/ST0E_U0_00014.wav'
sound_settings = {
    'volume': 50,
    'sound_on': True
}

class Window:
    def __init__(self):
        self._initialize_pygame()
        self._load_assets()
        self.leaderboard = Leaderboard()  # Initialize leaderboard here
        self._initialize_game_states()
        self._update_sound_volumes()  # Ensure sound volumes are updated at the start
        self.run()
    
    def _initialize_pygame(self):
        pg.init()
        pg.mouse.set_visible(False)
        pg.display.set_caption("Space Shooter")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    def _load_assets(self):
        self.background = pg.image.load(BACKGROUND_IMG)
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_y = 0
        self.background_y_speed = 1

        mixer.music.load(BACKGROUND_MUSIC)
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        
        self.player = player.Player(self.screen)
        self.enemy_manager = manage_enemies.ManageEnemies(self.screen, self.player)  # Pass player instance
        self.pickup_manager = manage_pickups.ManagePickups(self.screen)  # Initialize pickup manager

        # Initialize move and select sounds
        self.move_sound = mixer.Sound(MOVE_SOUND)
        self.select_sound = mixer.Sound(SELECT_SOUND)
    
    def _initialize_game_states(self):
        self.running = True
        self.in_start_menu = True
        self.in_pause_menu = False
        self.in_options_menu = False
        self.in_sound_menu = False
        self.in_controls_menu = False
        self.in_difficulty_menu = False
        self.in_gameover_menu = False
        self.in_leaderboard_menu = False
        self.selected_difficulty = None

        # Menus
        self.start_menu = menu.StartMenu(self.screen, self.player, self)
        self.pause_menu = menu.PauseMenu(self.screen, self.player, self)
        self.options_menu = menu.OptionsMenu(self.screen, self.player, self)
        self.sound_menu = menu.SoundMenu(self.screen, self.player, self)
        self.controls_menu = menu.ControlsMenu(self.screen, self.player, self)
        self.difficulty_menu = menu.DifficultyMenu(self.screen, self.player, self)
        self.gameover_menu = menu.GameOver(self.screen, self.leaderboard)
        self.leaderboard_menu = menu.LeaderboardMenu(self.screen, self.leaderboard)

    def run(self):
        clock = pg.time.Clock()
        while self.running:
            self._handle_current_menu()
            clock.tick(FPS)
        pg.quit()
    
    def _handle_current_menu(self):
        if self.in_start_menu:
            self._handle_menu("start")
        elif self.in_pause_menu:
            self._handle_menu("pause")
        elif self.in_options_menu:
            self._handle_menu("options")
        elif self.in_sound_menu:
            self._handle_menu("sound")
        elif self.in_controls_menu:
            self._handle_menu("controls")
        elif self.in_difficulty_menu:
            self._handle_menu("difficulty")
        elif self.in_gameover_menu:
            self._handle_menu("gameover")
        elif self.in_leaderboard_menu:
            self._handle_menu("leaderboard")
        else:
            self._update_game()
    
    def _handle_menu(self, menu_type):
        menu_map = {
            "start": self.start_menu,
            "pause": self.pause_menu,
            "options": self.options_menu,
            "sound": self.sound_menu,
            "controls": self.controls_menu,
            "difficulty": self.difficulty_menu,
            "gameover": self.gameover_menu,
            "leaderboard": self.leaderboard_menu
        }
        menu = menu_map[menu_type]
        if menu_type == "gameover":
            menu.draw(self.player.logic.scores)  # Pass the score to the GameOver menu
        else:
            menu.draw()  # Call draw with no arguments for other menus

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if menu_type == "gameover":
                action = menu.handle_input(event, self.player.logic.scores)  # Pass the score to handle_input
            else:
                action = menu.handle_input(event)
            self._process_menu_action(menu_type, action)

        pg.display.update()
    
    def _process_menu_action(self, menu_type, action):
        if menu_type == "start":
            if action == "Start Game":
                self.in_start_menu = False
            elif action == "Options":
                self._open_menu("options")
            elif action == "Leaderboard":
                self._open_menu("leaderboard")
            elif action == "Quit":
                self.running = False
        elif menu_type == "pause":
            if action == "Resume Game":
                self.in_pause_menu = False
            elif action == "Back to Start Menu":
                self._reset_game()
                self._open_menu("start")
        elif menu_type == "options":
            if action == "Back to Start Menu":
                self._open_menu("start")
            elif action in ["Sound", "Controls", "Difficulty"]:
                self._open_menu(action.lower())
        elif menu_type in ["sound", "controls", "difficulty"]:
            self._handle_submenu_action(menu_type, action)
        elif menu_type == "gameover" and action == "Show Leaderboard":
            self._open_menu("leaderboard")
        elif menu_type == "leaderboard" and action == "Back to Start Menu":
            self._open_menu("start")
            self._reset_game()
    
    def _handle_submenu_action(self, menu_type, action):
        if action == "Return":
            self._open_menu("options")
        elif menu_type == "difficulty" and action:
            self.selected_difficulty = action.split(": ")[-1]
            self.enemy_manager = manage_enemies.ManageEnemies(self.screen, difficulty=self.selected_difficulty)
        elif menu_type == "controls" and action:
            pass
        elif menu_type == "sound" and action:
            if action == "On":
                sound_settings['sound_on'] = True
                mixer.music.unpause()  # Unpause music when turning sound on
            elif action == "Off":
                sound_settings['sound_on'] = False
                mixer.music.pause()  # Pause music when turning sound off
            
        self._update_sound_volumes()  # Update the sound volumes
    
    def _open_menu(self, menu_name):
        setattr(self, f'in_{menu_name}_menu', True)
        for attr in ["in_start_menu", "in_pause_menu", "in_options_menu", "in_sound_menu", "in_controls_menu", "in_difficulty_menu", "in_gameover_menu", "in_leaderboard_menu"]:
            if attr != f'in_{menu_name}_menu':
                setattr(self, attr, False)
    
    def _reset_game(self):
        self.player = player.Player(self.screen)
        self.enemy_manager = manage_enemies.ManageEnemies(self.screen, self.player, difficulty=self.selected_difficulty or "Normal")
        self._initialize_game_states()

    def _update_game(self):
        if not self.player.logic.check_collisions(self.enemy_manager.enemies, self.enemy_manager.meteors, self.enemy_manager.enemy_lasers, self.pickup_manager):
            self._open_menu("gameover")
        
        self._scroll_background()
        self._handle_events()
        self._update_movements()
        self._render_screen()
        self._update_sound_volumes()
    
    def _scroll_background(self):
        self.background_y = (self.background_y + self.background_y_speed) % HEIGHT
        self.screen.blit(self.background, (0, self.background_y))
        self.screen.blit(self.background, (0, self.background_y - HEIGHT))
    
    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN and event.key == self.player.key_bindings["Pause"]:
                self.in_pause_menu = True

    def _update_movements(self):
        keys = pg.key.get_pressed()
        self.player.move(keys)
        self.enemy_manager.move_enemies()
        self.enemy_manager.move_lasers()
        self.pickup_manager.update_pickups()  # Update pickups
        self.enemy_manager.adjust_difficulty(self.player.logic.scores)  # Adjust difficulty based on score
        self.enemy_manager.generate_enemies()  # Generate enemies including boss
        if keys[self.player.key_bindings["Shoot"]]:
            self.player.laser_shot()
            self._play_sound(SHOT_SOUND)
        self._handle_enemy_shooting()
        
    def _render_screen(self):
        self.screen.blit(self.player.image, (self.player.logic.x, self.player.logic.y))
        self.player.draw()
        self.player.draw_ammo()  # Draw triple shot ammo
        self.player.generate_lives()
        self.player.increase_scores()
        self.enemy_manager.generate_enemies()
        self.enemy_manager.draw_enemies()
        self.pickup_manager.draw_pickups()  # Draw pickups
        pg.display.update()
    
    def _handle_enemy_shooting(self):
        for enemy in self.enemy_manager.enemies:
            new_laser = enemy.enemy_shoot()
            if new_laser:
                self.enemy_manager.enemy_lasers.append(new_laser)

    def _play_sound(self, audio):
        sound = mixer.Sound(audio)
        sound.set_volume(sound_settings['volume'] / 100.0 if sound_settings["sound_on"] else 0)  # Use the global volume setting
        sound.play()

    def _update_sound_volumes(self, volume=None):
        if volume is None:
            volume = sound_settings['volume'] / 100.0 if sound_settings['sound_on'] else 0
        mixer.music.set_volume(volume)
        self.player.logic.update_sound_volumes(volume)
        self.move_sound.set_volume(volume)
        self.select_sound.set_volume(volume)
