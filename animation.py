import pygame

class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self, sprite_name):
        super().__init__()
        
        self.image = pygame.image.load(f"{sprite_name}.png")