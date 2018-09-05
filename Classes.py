import pygame
from Constante import *


class Personnage:
    def __init__(self, name, positionX, positionY):
        self.name = name
        self.x = positionX
        self.y = positionY
        self.life = player_life
        self.perspective_pos = 100
        self.coef = 1
        self.balles = 6
        self.munitions = 6
        self.chargeurs = 1
        self.isWalk = 0
        self.idle = 0
        self.walk = 0
        self.shoot = 0
        self.space = [positionX, positionY, persoWidth, persoHeight]
        self.src = pygame.image.load(src_joueur).convert_alpha()
        self._src = pygame.image.load(src_joueur).convert_alpha()

    def move(self, direction):
        
        if direction:
            self.y -= perso_speed
            self.y = max(self.y, zdj_ground - self.space[3])
            self.space[1] = self.y
            if not self.y == zdj_ground - self.space[3]:
                self.perspective_pos -= perspective_speed
                self.coef = self.perspective_pos / 100
                self.isWalk = 1
        else:
            self.y += perso_speed
            self.y = min(self.y, (zdj_Y + zdj_Height) - persoHeight)
            self.space[1] = self.y
            if not self.y == (zdj_Y + zdj_Height) - persoHeight:
                self.perspective_pos += perspective_speed
                self.coef = self.perspective_pos / 100
                self.isWalk = 1

    def shoot_f(self):
        self.shoot = 1
        self.balles -= 1
        front = self.x + self.space[2]  # Coordonné devant le joueur
        middle = self.y + (self.space[3]/2)  # Coordonné au milieu de son corps

        return front, middle

    def munitions_update(self):
        if self.balles % 6 == 0 and self.balles != 0:
            self.munitions = 6
        else:
            self.munitions = self.balles % 6

        self.chargeurs = int((self.balles - self.munitions) / 6)
        
    def damage(self):
        self.life -= life_damage

    def resize_to_src(self, img):
        width = int(persoWidth * self.coef)
        height = int(persoHeight * self.coef)
        self.space[2] = width
        self.space[3] = height
        self.src = pygame.transform.scale(img, (width,height))

    def idleSprite(self):
        self.idle += 1
        if self.idle > (fps_max*10/30)*2-1:
            self.idle = 0
        return int(self.idle / (fps_max*10/30))

    def shootSprite(self):
        self.shoot += 1
        if self.shoot > (fps_max/30)*3:
            self.shoot = 0

        return int(self.shoot / (fps_max/30))

    def walkSprite(self):
        self.walk += 1
        if self.walk > (fps_max*5/30)*3:
            self.walk = 0
        return int(self.walk / (fps_max*5/30))

    def __repr__(self):
        return "objetPersonnage"


class Ennemis:
    def __init__(self, positionX, positionY):
        self.x = positionX
        self.y = positionY
        self.coef = 1
        self.walk = 0
        self.end = 0
        self.space = [positionX, positionY, ennemisWidth, ennemisHeight]
        self.src = pygame.image.load(src_ennemis).convert_alpha()
        self._src = pygame.image.load(src_ennemis).convert_alpha()

    def move(self):
        self.x -= ennemis_speed
        self.space[0] = self.x
        
    def resize_to_src(self, img):
        width = int(ennemisWidth * self.coef)
        height = int(ennemisHeight * self.coef)
        self.space[2] = width
        self.space[3] = height
        self.src = pygame.transform.scale(img, (width,height))

    def walkSprite(self):
        self.walk += 1
        if self.walk > (fps_max*4/30)*3:  
            self.walk = 0
        return int(self.walk / (fps_max*4/30))
    
    def endSprite(self):
        self.end += 1
        if self.end > (fps_max*2/30)*8:
            self.end = -2
        return int(self.end / (fps_max*2/30))
        
    def __repr__(self):
        return "objetEnnemis"


class Balles:
    def __init__(self, positionX, positionY):
        self.x = positionX
        self.y = positionY
        self.coef = 1
        self.space = [positionX, positionY, ballesWidth, ballesHeight]
        self.src = pygame.image.load(src_balles).convert_alpha()
        self._src = pygame.image.load(src_balles).convert_alpha()
        
    def move(self):
        self.x += balles_speed
        self.space[0] = self.x

    def resize_to_src(self, img):
        width = int(ballesWidth * self.coef)
        height = int(ballesHeight * self.coef)
        self.space[2] = width
        self.space[3] = height
        self.src = pygame.transform.scale(img, (width,height))

    def __repr__(self):
        return "objetBalles"

class Chargeur:
    def __init__(self, positionX, positionY):
        self.x = positionX
        self.y = positionY
        self.coef = 1
        self.end = 0
        self.src = pygame.image.load(src_chargeur).convert_alpha()
        self._src = pygame.image.load(src_chargeur).convert_alpha()

    def resize_to_src(self, img):
        width = int(ennemisWidth * self.coef)
        height = int(ennemisHeight * self.coef)
        self.src = pygame.transform.scale(img, (width,height))

    def endSprite(self):
        self.end += 1
        if self.end > (fps_max*2/30)*14:
            self.end = -2
        return int(self.end / (fps_max*2/30))

    def __repr__(self):
        return "objetChargeur"

