import pygame

class Player(pygame.sprite.Sprite): # Classe qui hérite de sprite pygame
    
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("player.png") # récupere l'image du joueur
        self.image = self.get_image(0, 0) # a partir de quel point on découpe l'image
        self.image.set_colorkey([0, 0, 0]) # on met un bacground transparent
        self.rect = self.image.get_rect() # on defini un rectangle autour de l'image
        self.position = [x, y]
        
    def update(self):
        self.rect.topleft = self.position
        
    def get_image(self, x, y):
        image = pygame.Surface([32, 32]) # défini la taille du bout d'image qu'on veut récupérer
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) # récupere le morceau qui nous interesse
        return image
    