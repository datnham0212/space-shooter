import pygame as pg
import window

class Menu:
    def __init__(self, screen, options, custom_height=0):
        self.screen = screen
        self.font = pg.font.Font(None, 50)
        self.options = options
        self.selected = 0
        self.custom_height = custom_height
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(window.WIDTH//2, window.HEIGHT//2 - self.custom_height + i * 60))
            self.screen.blit(text, rect)

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pg.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pg.K_RETURN:
                return self.options[self.selected]
        return None

class StartMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, ["Start Game", "Options", "Quit"])

class PauseMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, ["Resume Game", "Back to Start Menu"])
        
class OptionsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, ["Sound", "Controls", "Difficulty", "Back to Start Menu"], custom_height=50)

class SoundMenu(Menu):
    def __init__(self, screen):
        self.sound_options = ['On', 'Off']
        self.volume_options = list(range(0, 101))
        self.sound_index = 0
        self.volume_index = 50  # Default volume
        super().__init__(screen, [f"Volume: {self.volume_index}", f"Sound: {self.sound_options[self.sound_index]}", "Return"])

    def handle_input(self, event):
        result = super().handle_input(event)

        if result is not None:
            return result

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                if self.selected == 0:  # Adjust volume
                    self.volume_index = (self.volume_index + (1 if event.key == pg.K_RIGHT else -1)) % len(self.volume_options)
                    self.options[0] = f"Volume: {self.volume_options[self.volume_index]}"
                elif self.selected == 1:  # Toggle sound on/off
                    self.sound_index = (self.sound_index + (1 if event.key == pg.K_RIGHT else -1)) % len(self.sound_options)
                    self.options[1] = f"Sound: {self.sound_options[self.sound_index]}"
        return None


class ControlsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, ["Up: ", "Down: ", "Left: ", "Right: ", "Shoot: ", "Pause: ", "Return"], custom_height=150)

class DifficultyMenu(Menu):
    def __init__(self, screen):
        self.diff_options = ['Normal', 'Hard']
        self.index = 0  # Initialize index to 0
        super().__init__(screen, [f"Set Difficulty: {self.diff_options[self.index]}", "Return"])
    
    def handle_input(self, event):
        # Call the base class method for up/down navigation and return option selection
        result = super().handle_input(event)
        if result is not None:
            return result  # Return the selected option

        # Handle left and right arrow keys for difficulty selection
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:  # Left arrow key
                self.index = (self.index - 1) % len(self.diff_options)  # Loop back
                self.update_diff_text()
            elif event.key == pg.K_RIGHT:  # Right arrow key
                self.index = (self.index + 1) % len(self.diff_options)  # Loop forward
                self.update_diff_text()
        return None
    
    def update_diff_text(self):
        self.options[0] = f"Set Difficulty: {self.diff_options[self.index]}"
    
    

            

    
    
