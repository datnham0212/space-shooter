import pygame as pg
from pygame import mixer
import window
import time

class Menu:
    def __init__(self, screen, options, player, custom_height=0):
        self.screen = screen
        self.font = pg.font.Font(None, 50)
        self.options = options
        self.selected = 0
        self.custom_height = custom_height
        self.move_sound = pg.mixer.Sound('sounds/ST0E_U0_00004.wav')
        self.select_sound = pg.mixer.Sound('sounds/ST0E_U0_00014.wav')
        self.player = player  # Store the player instance

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(window.WIDTH // 2, window.HEIGHT // 2 - self.custom_height + i * 60))
            self.screen.blit(text, rect)

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                if window.sound_settings['sound_on']:
                    self.move_sound.play()
            elif event.key == pg.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                if window.sound_settings['sound_on']:
                    self.move_sound.play()
            elif event.key == self.player.key_bindings["Pause"]:  # Use the player's key binding for selecting an option
                if window.sound_settings['sound_on']:
                    self.select_sound.play()
                return self.options[self.selected]
        return None

class StartMenu(Menu):
    def __init__(self, screen, player):
        super().__init__(screen, ["Start Game", "Options", "Quit"], player)

class PauseMenu(Menu):
    def __init__(self, screen, player):
        super().__init__(screen, ["Resume Game", "Options", "Back to Start Menu"], player)

class OptionsMenu(Menu):
    def __init__(self, screen, player):
        super().__init__(screen, ["Sound", "Controls", "Difficulty", "Back to Start Menu"], player, custom_height=50)

class SoundMenu(Menu):
    def __init__(self, screen, player):
        super().__init__(screen, [f"Volume: {window.sound_settings['volume']}", f"Sound On: {window.sound_settings['sound_on']}", "Return"], player)
        self.volume = window.sound_settings['volume']
        self.sound_on = window.sound_settings['sound_on']

    def handle_input(self, event):
        result = super().handle_input(event)
        if result:
            return result

        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                self.update_settings(event.key)
        return None

    def update_settings(self, key):
        if self.selected == 0:  # Adjust volume
            if key == pg.K_LEFT and self.volume > 0:
                self.volume -= 10
            elif key == pg.K_RIGHT and self.volume < 100:
                self.volume += 10

            # Update the menu text and global sound settings
            self.options[0] = f"Volume: {self.volume}"
            window.sound_settings['volume'] = self.volume
            # Apply volume change immediately
            mixer.music.set_volume(self.volume / 100.0)

        elif self.selected == 1:  # Toggle sound on/off
            if key in [pg.K_LEFT, pg.K_RIGHT]:
                self.sound_on = not self.sound_on

            # Update the menu text and global sound settings
            self.options[1] = f"Sound On: {self.sound_on}"
            window.sound_settings['sound_on'] = self.sound_on

            if self.sound_on:
                mixer.music.unpause()
                self.move_sound.set_volume(1)
                self.select_sound.set_volume(1)
                self.player.damage_sound.set_volume(1)
            else:
                mixer.music.pause()
                self.move_sound.set_volume(0)
                self.select_sound.set_volume(0)
                self.player.damage_sound.set_volume(0)

class ControlsMenu(Menu):
    def __init__(self, screen, player):
        self.player = player
        self.key_bindings = player.key_bindings.copy()
        self.reassigning_key = None
        super().__init__(screen, self.build_options(), player, custom_height=150)

    def build_options(self):
        return [f"{action} - {pg.key.name(key)}" for action, key in self.key_bindings.items()] + ["Return"]

    def handle_input(self, event):
        if self.reassigning_key:
            if event.type == pg.KEYDOWN:
                self.key_bindings[self.reassigning_key] = event.key
                self.reassigning_key = None
                self.options = self.build_options()
                self.player.update_key_bindings(self.key_bindings)  # Update player key bindings and save to JSON
            return None

        result = super().handle_input(event)
        if result and self.selected < len(self.options) - 1:
            self.reassigning_key = list(self.key_bindings.keys())[self.selected]
            self.options[self.selected] = f"{self.reassigning_key} - Press new key"
        return result

class DifficultyMenu(Menu):
    DIFFICULTIES = ["Easy", "Normal", "Hard"]

    def __init__(self, screen, player):
        super().__init__(screen, ["Set Difficulty: Normal", "Return"], player)
        self.difficulties = ["Normal", "Hard"]
        self.index = 0

    def handle_input(self, event):
        result = super().handle_input(event)
        if result:
            return result

        if event.type == pg.KEYDOWN and event.key in [pg.K_LEFT, pg.K_RIGHT]:
            self.index = (self.index + (1 if event.key == pg.K_RIGHT else -1)) % len(self.difficulties)
            self.options[0] = f"Set Difficulty: {self.difficulties[self.index]}"
        return None

class LeaderboardMenu:
    def __init__(self, screen, leaderboard):
        self.screen = screen
        self.leaderboard = leaderboard
        self.font = pg.font.Font(None, 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.render_text("Leaderboard", self.font, (255, 255, 255), y_offset=50)
        for i, entry in enumerate(self.leaderboard.get_scores()):
            self.render_text(f"{i + 1}. {entry['name']} - {entry['score']}", self.font, (255, 255, 255), y_offset=100 + i * 40)
        self.render_text("Press any key to return to the start menu", self.font, (255, 255, 255), y_offset=500)

    def render_text(self, text, font, color, y_offset):
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (window.WIDTH // 2 - rendered_text.get_width() // 2, y_offset))

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            return "Back to Start Menu"
        return None

class GameOver:
    def __init__(self, screen, leaderboard):
        self.screen = screen
        self.leaderboard = leaderboard
        self.entered_name = ""
        self.font = pg.font.Font(None, 36)

    def draw(self, score):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Game Over! Enter your name:", True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        name_text = self.font.render(self.entered_name, True, (255, 255, 255))
        self.screen.blit(name_text, (100, 150))
        pg.display.flip()

    def handle_input(self, event, score):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.leaderboard.add_score(self.entered_name, score)
                return "Show Leaderboard"
            elif event.key == pg.K_BACKSPACE:
                self.entered_name = self.entered_name[:-1]
            else:
                self.entered_name += event.unicode
        return None
    