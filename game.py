import pygame
import pytmx
import pyscroll

from player import Player

class Game:
    def __init__(self):

        # Création de la fenetre
        self.screen = pygame.display.set_mode((800, 600)) # taille de la fenetre
        pygame.display.set_caption("Pygamon - Aventure") # titre de la fenetre
        
        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx") # Récupère le fichier qui contient la carte
        map_data = pyscroll.data.TiledMapData(tmx_data) # Récupère les données de la cartes qui nous intéresse
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # Contient tout les calques regroupé
        map_layer.zoom = 2
        
        # Générer un joueur a partir de l'objet player
        self.player = Player(30, 40)
        
        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1) # calques déssiner et default_layer est la position du calque par defaut
        self.group.add(self.player)
        
    def run(self):
        
        #boucle du jeu
        running = True

        while running:
            
            self.group.update()
            
            self.group.draw(self.screen)# Dessine la carte dans notre fenetre
            pygame.display.flip() # Actualise a chaque boucle
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
