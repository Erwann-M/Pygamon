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
        player_position = tmx_data.get_object_by_name("player") # on récupere la position du joueur par defaut défini sur tiled
        self.player = Player(player_position.x, player_position.y) # la position du joueur est maintenant dynamique 
        
        # définir la liste des rectangles de collision.
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5) # calques déssiner et default_layer est la position du calque par defaut
        self.group.add(self.player) # on ajoute le joueur au groupe de calque
        
        #definition du rectangle de colision pour entré dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        # utilisation des méthodes de mouvement définient dans l'objet player
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("up")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")
                
                
    def switch_house(self):
        tmx_data = pytmx.util_pygame.load_pygame("house.tmx") # Récupère le fichier qui contient la carte
        map_data = pyscroll.data.TiledMapData(tmx_data) # Récupère les données de la cartes qui nous intéresse
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # Contient tout les calques regroupé
        map_layer.zoom = 2
        
        # définir la liste des rectangles de collision.
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5) # calques déssiner et default_layer est la position du calque par defaut
        self.group.add(self.player) # on ajoute le joueur au groupe de calque
        
        #definition du rectangle de colision pour sortir de la maison
        enter_house = tmx_data.get_object_by_name("exit_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        
        # point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y
        
    def switch_world(self):
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx") # Récupère le fichier qui contient la carte
        map_data = pyscroll.data.TiledMapData(tmx_data) # Récupère les données de la cartes qui nous intéresse
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # Contient tout les calques regroupé
        map_layer.zoom = 2
        
        # définir la liste des rectangles de collision.
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5) # calques déssiner et default_layer est la position du calque par defaut
        self.group.add(self.player) # on ajoute le joueur au groupe de calque
        
        #definition du rectangle de colision pour sortir de la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        
        # point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y
        
            
    def update(self):
        self.group.update()
        
        #verifier entré maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            
        #verifier entré maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
        
        #verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
        
    def run(self):
        
        clock = pygame.time.Clock() # la methode clock de pygame, permet de fixé les fps, de définir un temps donné entre chaque boucles
        
        #boucle du jeu
        running = True

        while running:
            
            self.player.save_location()
            
            self.handle_input()
            self.update() # actualisation du groupe
            
            self.group.center(self.player.rect.center)
            
            self.group.draw(self.screen)# Dessine la carte dans notre fenetre
            pygame.display.flip() # Actualise a chaque boucle
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            clock.tick(60) # ici on utilise clock et on lui donne une valeur de fps.

        pygame.quit()
