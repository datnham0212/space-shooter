import pygame

class Pickup(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        super().__init__()
        self.image = pygame.image.load(f"assets/{image_name}.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self, player):
        pass

    def update(self):
        self.rect.y += 2
        if self.rect.y > 600:
            self.kill()

class ExtraLives(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y, "extra_lives")
        self.value = 1

    def apply(self, player):
        if player.max_lives < 5:  # Limit the maximum lives to 5
            player.max_lives += self.value
        self.kill()