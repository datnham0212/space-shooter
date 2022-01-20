import pygame as pg
import window

class Menu:
    def __init__(self, screen, options):
        self.screen = screen
        self.font = pg.font.Font(None, 50)
        self.options = options
        self.selected = 0
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(window.WIDTH//2, window.HEIGHT//2 - 50 + i * 60))
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
        super().__init__(screen, ["Resume Game", "Return to Start Menu"])
        
class OptionsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, ["Sound", "Controls", "Difficulty", "Return to Start Menu"])
    