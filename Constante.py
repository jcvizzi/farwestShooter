# Paramètres de la fenêtre
fenetreWidth = 800
fenetreHeight = 450
fenetreTitle = "Shooter"

#Paramètre menu_info
menu_info_X = 0
menu_info_Y = 0
menu_info_width = fenetreWidth
menu_info_height = 50
menu_info_src = "Images/menu_info2.png"

# Paramètre zone de jeu
zdj_X = 0
zdj_Y = menu_info_height
zdj_Width = 800
zdj_Height = 400
zdj_ground = zdj_Y + 230

# Paramètre controle pygame.key.set_repeat(before,between)
BEFORE = 100
BETWEEN = 300

# Paramètre partie
fps_max = 30

# Paramètre joueur
perso_X = 0
perso_Y = 0
persoWidth = 130
persoHeight = 103
perso_speed = 24/(fps_max/15)
UP = 1
DOWN = 0

# Paramètre ennemis
ennemisWidth = 130
ennemisHeight = 103
ennemis_speed = 14/(fps_max/15)

# Paramètre balles
ballesWidth = 18
ballesHeight = 8
balles_speed = 24/(fps_max/15)

# Paramètre chargeur
chargeur_width = 130
chargeur_height = 103


# Paramètre de perspective
perspective_speed = 4/(fps_max/15)

# Parametre pour toDisplay
ENNEMIS = 1
BALLES = 0
ENDSPRITE = 2

# Source images
src_joueur = "Images/joueur/idle/I0.png"
src_ennemis = "Images/ennemis/walk/W0.png"
src_balles = "Images/balles.png"
src_chargeur = "Images/chargeur/B0.png"
src_zdj = "Images/desert.png"

# Paramètre vie du joueur
player_life = 100
life_damage = 10


# Paramètre scores
score_elimination = 100
score_lost_bullet = 50
