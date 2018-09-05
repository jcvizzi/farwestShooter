import pygame
from pygame.locals import *
from tkinter import *
from tkinter import font
import sys
import ftplib
import webbrowser
from time import *
import random
from math import exp
from Classes import *
from Constante import *


def create_game(name_joueur):
    """ Créer une partie :
        Créer une fenetre de jeu
        Créer une zone de jeu
        Créer la liste d'élément à afficher
        Créer un joueur
        Return fenetre, zdj, toDisplay, joueur
    """

    # Création de la fenetre
    fenetre = pygame.display.set_mode((fenetreWidth, fenetreHeight), RESIZABLE)
    pygame.display.set_caption(fenetreTitle)
    menu_info = pygame.Surface((menu_info_width,menu_info_height))
    menu_info.fill((0, 153, 255))             #(96,96,96))
    font_info = pygame.font.Font(None, 24)
    font_info2 = pygame.font.Font(None, 48)
    zdj = pygame.image.load(src_zdj).convert()

    # Liste des élements à afficher
    toDisplay = [[], [], []]
    
    # Création personnage
    joueur = Personnage(name_joueur, zdj_X, (zdj_Y + zdj_Height) - persoHeight)


    return fenetre, menu_info, font_info, font_info2, zdj, toDisplay, joueur


def set_sprite():
    """Défini les listes de sprites"""

    walk_ennemis = [pygame.image.load("Images/ennemis/walk/W0.png").convert_alpha(),pygame.image.load("Images/ennemis/walk/W1.png").convert_alpha(),
                pygame.image.load("Images/ennemis/walk/W2.png").convert_alpha(),pygame.image.load("Images/ennemis/walk/W3.png").convert_alpha()]
    end_ennemi = [pygame.image.load("Images/ennemis/end/E0.png").convert_alpha(),pygame.image.load("Images/ennemis/end/E1.png").convert_alpha(),
                 pygame.image.load("Images/ennemis/end/E2.png").convert_alpha(),pygame.image.load("Images/ennemis/end/E3.png").convert_alpha(),
                 pygame.image.load("Images/ennemis/end/E4.png").convert_alpha(),pygame.image.load("Images/ennemis/end/E5.png").convert_alpha(),
                 pygame.image.load("Images/ennemis/end/E6.png").convert_alpha(),pygame.image.load("Images/ennemis/end/E7.png").convert_alpha(),
                 pygame.image.load("Images/ennemis/end/E8.png").convert_alpha()]
    idle = [pygame.image.load("Images/joueur/idle/I0.png").convert_alpha(),pygame.image.load("Images/joueur/idle/I1.png").convert_alpha()]
    shoot = [pygame.image.load("Images/joueur/shoot/S0.png").convert_alpha(),pygame.image.load("Images/joueur/shoot/S1.png").convert_alpha(),
             pygame.image.load("Images/joueur/shoot/S2.png").convert_alpha(),pygame.image.load("Images/joueur/shoot/S3.png").convert_alpha()]
    walk_joueur = [pygame.image.load("Images/joueur/walk/W0.png").convert_alpha(),pygame.image.load("Images/joueur/walk/W1.png").convert_alpha(),
            pygame.image.load("Images/joueur/walk/W2.png").convert_alpha(),pygame.image.load("Images/joueur/walk/W3.png").convert_alpha()]
    chargeur = [pygame.image.load("Images/chargeur/B0.png").convert_alpha(),pygame.image.load("Images/chargeur/B1.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B2.png").convert_alpha(),pygame.image.load("Images/chargeur/B3.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B4.png").convert_alpha(),pygame.image.load("Images/chargeur/B5.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B6.png").convert_alpha(),pygame.image.load("Images/chargeur/B7.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B8.png").convert_alpha(),pygame.image.load("Images/chargeur/B9.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B10.png").convert_alpha(),pygame.image.load("Images/chargeur/B11.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B12.png").convert_alpha(),pygame.image.load("Images/chargeur/B13.png").convert_alpha(),
                pygame.image.load("Images/chargeur/B14.png").convert_alpha()]
    munitions = [pygame.image.load("Images/munitions/M0.png").convert_alpha(),pygame.image.load("Images/munitions/M1.png").convert_alpha(),
                 pygame.image.load("Images/munitions/M2.png").convert_alpha(),pygame.image.load("Images/munitions/M3.png").convert_alpha(),
                 pygame.image.load("Images/munitions/M4.png").convert_alpha(),pygame.image.load("Images/munitions/M5.png").convert_alpha(),
                 pygame.image.load("Images/munitions/M6.png").convert_alpha()]

                
    return walk_ennemis, end_ennemi, idle, shoot, walk_joueur, chargeur, munitions

             
def timeManager(start, temps_pause):
    """Gere le temps"""

    start = start + temps_pause
    temps = time() - start
    minutes = 0
    secondes_t = int(temps)
    while temps > 60:
        temps -= 60
        minutes += 1
    secondes = int(temps)

    return (secondes, minutes), secondes_t, start

def create_bullet(x, y):
    """
    Créer un ennemis
    Renvoi cette ennemis
    """
    #Créer la balle au niveau du joueur
    balle = Balles(x, y)
    balle.coef = (100 -(perspective_speed*((zdj_Y + zdj_Height - ballesHeight - balle.y)/(perso_speed*2)))) / 100
    balle.resize_to_src(balle._src)

    return balle

def create_ennemis():
    """
    Créer un ennemis
    Renvoi cette ennemis
    """
    # Définis des coordonnées aléatoires dans la zone de jeu
    x = (zdj_X + zdj_Width) - ennemisWidth
    min_y = 1 + int((ennemisHeight*(-perspective_speed*(zdj_Height-ennemisHeight)+100*perso_speed)-100*(zdj_ground - zdj_Y)*perso_speed)/(-ennemisHeight*perspective_speed-100*perso_speed))
    y = random.randint(min_y + zdj_Y, zdj_Y + zdj_Height - ennemisHeight)

    # Créer l'ennemis
    ennemi = Ennemis(x, y)
    ennemi.coef = (100 - (perspective_speed*((zdj_Y + zdj_Height - ennemisHeight - ennemi.y)/perso_speed))) / 100
    ennemi.resize_to_src(ennemi._src)
    
    return ennemi


def collision(objetA, objetB):
    """Gere les collisons"""

    xA, yA, widthA, heightA = objetA
    rightA = xA + widthA
    leftA = xA
    topA = yA
    bottomA = yA + heightA

    xB, yB, widthB, heightB = objetB
    rightB = xB + widthB
    leftB = xB
    topB = yB
    bottomB = yB + heightB

    if rightB < leftA:
        # objetB est à gauche
        return False
    if bottomB < topA:
        # objetB est au-dessus
        return False
    if leftB > rightA:
        # objetB est à droite
        return False
    if topB > bottomA:
        # objetB est en-dessous
        return False
    # Dans tous les autres cas il y a collision
    return True


def update(toDisplay, joueur, secondes_t, difficulty, stat):
    """ Actualise les instances à afficher :
        Fait bouger les balles et les ennemis
        Supprime les balles sortie de la zone de jeu
        Regarde si un ennemis franchis le joueur
        Retire les elements qui on fini leur animation de fin
        Créer des ennemis aléatoirement
        Fait les actions liée au collisions
        Return toDisplay
    """
    
    toDelete = [[], [], []]

    # Ajoute les balles sortie de la zone de jeu à toDelete
    for balle in toDisplay[BALLES]:
        balle.move()
        if balle.x > (zdj_X + zdj_Width):
            stat["game_score"] -= score_lost_bullet
            stat["game_score"] = max(stat["game_score"], 0)
            toDelete[BALLES].append(balle)

    # Regarde si un ennemis franchis le joueur
    for ennemi in toDisplay[ENNEMIS]:
        ennemi.move()
        if ennemi.x < joueur.x + persoWidth:
            joueur.damage()
            toDelete[ENNEMIS].append(ennemi)
            stat["ennemi_echappe"] += 1
            

    # Ajoute à toDelete les elements qui on fini leur animation de fin
    for element in toDisplay[ENDSPRITE]:
        if element.end < 0:
            toDelete[ENDSPRITE].append(element)

    # Créer des ennemis aléatoirement
    t = int(60*exp(secondes_t/-100))+6
    if difficulty >= t:
        toDisplay[ENNEMIS].append(create_ennemis())
        difficulty = 0
    difficulty += 30/fps_max

    # Observe les collisions et ajoute à toDelete les balles et à ENDSPRITE les ennemis en contact
    for ennemi in toDisplay[ENNEMIS]:
        for balle in toDisplay[BALLES]:
            if collision(ennemi.space, balle.space):
                toDelete[BALLES].append(balle)
                toDisplay[ENDSPRITE].append(ennemi)
                toDelete[ENNEMIS].append(ennemi)
                if random.randint(1,10) == 1 or joueur.balles == 0:
                    toDisplay[ENDSPRITE].append(Chargeur(ennemi.x,ennemi.y))
                    joueur.balles += 6
                stat["game_score"] += score_elimination
                stat["ennemi_elimine"] += 1

    # Soustrait les elements de toDelete à toDisplay
    toDisplay = [list(set(toDisplay[BALLES]) - set(toDelete[BALLES])), list(set(toDisplay[ENNEMIS]) - set(toDelete[ENNEMIS])), list(set(toDisplay[ENDSPRITE]) - set(toDelete[ENDSPRITE]))]

    return toDisplay, difficulty, stat


def affichage(fenetre, joueur, toDisplay, sprites):
    """ Gère l'affichage des élément sur la fenetres"""

    # Récupération des sprites
    walk_ennemis, end_ennemi, idle, shoot, walk_joueur, chargeur, munitions = sprites

    #Affichage du nombre de munitions
    fenetre.blit(munitions[joueur.munitions], (zdj_X + 5,zdj_Y + 5))

    # Affiche le joueur selon son action
    if joueur.shoot:
        joueur.resize_to_src(shoot[joueur.shootSprite()])
    elif joueur.isWalk:
        joueur.resize_to_src(walk_joueur[joueur.walkSprite()])
    else:
        joueur.resize_to_src(idle[joueur.idleSprite()])
        
    joueur.isWalk = 0
    fenetre.blit(joueur.src, (joueur.x, joueur.y))

    # Affiche tout les éléments de toDisplay 
    for balle in toDisplay[BALLES]:
        fenetre.blit(balle.src, (balle.x, balle.y))
    for ennemi in toDisplay[ENNEMIS]:
        ennemi.resize_to_src(walk_ennemis[ennemi.walkSprite()])
        fenetre.blit(ennemi.src, (ennemi.x,ennemi.y))
    for element in toDisplay[ENDSPRITE]:
        if type(element) == Ennemis:    
            element.resize_to_src(end_ennemi[element.endSprite()])
        if type(element) == Chargeur:
            element.resize_to_src(chargeur[element.endSprite()])    
        fenetre.blit(element.src, (element.x, element.y))


def game(name):
    """Lance une partie"""
    
    pygame.init()

    # Créer une partie
    fenetre, menu_info, font_info, font_info2, zdj, toDisplay, joueur = create_game(name)
    difficulty = 0
    img_menu_info = pygame.image.load(menu_info_src).convert_alpha()

    # Musics
    musics = pygame.mixer.music.load("RIGAKU.ogg")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)


    # Créer les sprites
    sprites = set_sprite()

    # Créer les statistique
    stat = {"game_score" : 0, "ennemi_elimine" : 0, "nb_balle" : 0, "ennemi_echappe": 0}

    # Temps de départ
    start = time()
    temps = 0
    start_for_pause = 0
    temps_pause = 0

    # Permet d'activer la pression continue des touches
    pygame.key.set_repeat(BEFORE, BETWEEN)

    continuer = 1
    pause = 0
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = 0 if pause else 1
                if not pause:
                    if event.key == K_SPACE:
                        if joueur.balles > 0:
                            front, middle = joueur.shoot_f()
                            toDisplay[BALLES].append(create_bullet(front, middle))
                            stat["nb_balle"] += 1
                    if event.key == K_r:
                        pygame.mixer.music.pause()
                    if event.key == K_t:
                        pygame.mixer.music.unpause()

        if pause:
            pygame.time.Clock().tick(fps_max)
            if not start_for_pause:
                start_for_pause = time()
            temps_pause = time() - start_for_pause
            pygame.mixer.music.pause() #Met la musique en pause
        else:
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                joueur.move(UP)
            if keys[K_DOWN]:
                    joueur.move(DOWN)


            # Gestion du temps
            pygame.time.Clock().tick(fps_max)
            temps, secondes_t, start = timeManager(start, temps_pause)
            if  start_for_pause:
                pygame.mixer.music.unpause() #Reprend la musique là où elle a été coupée
            start_for_pause = 0
            temps_pause = 0

            # Déplacement et actualisation des instances
            toDisplay, difficulty, stat = update(toDisplay, joueur, secondes_t, difficulty, stat)
            joueur.munitions_update()
            if joueur.life <= 0:
                continuer = 0

            # Gestion menu_info
            info_vie = font_info.render('Vie: '+str(joueur.life),1,(0,0,0))
            info_score = font_info.render('Score: '+str(stat["game_score"]),1,(0,0,0))
            info_ennemi = font_info.render('Ennemis éliminés: '+str(stat["ennemi_elimine"]),1,(0,0,0))
            info_balle = font_info.render('Balles shootées: '+str(stat["nb_balle"]),1,(0,0,0))
            info_temps = font_info.render('Temps: '+str(temps[1])+' : '+str(temps[0]),1,(0,0,0))
            info_chargeurs = font_info2.render('+ '+ str(joueur.chargeurs),1,(255,0,0))
            
            # Affichage
            fenetre.blit(zdj, (zdj_X, zdj_Y))
            fenetre.blit(menu_info, (menu_info_X,menu_info_Y))
            menu_info.blit(img_menu_info, (0,0))
            fenetre.blit(info_vie,(10,25))
            fenetre.blit(info_score,(90,25))
            fenetre.blit(info_ennemi,(210,25))
            fenetre.blit(info_balle,(410,25))
            fenetre.blit(info_temps,(600,25))
            fenetre.blit(info_chargeurs, (zdj_X + 110,zdj_Y + 7))
            affichage(fenetre, joueur, toDisplay, sprites)
            pygame.display.flip()
            
    # Quand la partie est finie
    temps = str(temps[1]) + ':'+ str(temps[0])
    pygame.mixer.music.stop()
    pygame.display.quit()
    save_score(stat, joueur, temps)

    
    return toDisplay, joueur, temps, stat


def close(fenetre):
    """Ferme une fenetre tkinter"""
    fenetre.quit()
    fenetre.destroy()


def save_score(stat, joueur, temps):
    """Créer ou actualise le fichier score et l'envoie sur le site"""
    file_name = ''+ joueur.name +'.txt'
    
    file = open(file_name, "a")
    file.write(''+str(stat["game_score"])+','+str(stat["ennemi_elimine"])+','+str(stat["nb_balle"])+','+str(stat["ennemi_echappe"])+','+temps+'\n')
    file.close()
    
    try:
        session = ftplib.FTP("host","username","password")

        file = open(file_name,'rb')

        session.cwd('*******')
        session.storbinary('STOR '+file_name, file)
        session.quit()
    except:
        pass

    file.close()  


def launcher():
    """Fenetre de demarage"""
    global on_play, replay
    
    on_play = 0
    first_fenetre = Tk()
    first_fenetre.geometry('800x400')
    first_fenetre.resizable(width=False, height=False)
    first_fenetre.title('Shooter')

    canvas = Canvas(first_fenetre, bg='blue', height=250, width=300)
    filename = PhotoImage(file="./Images/menu.gif")
    back_label = Label(first_fenetre, image=filename)
    back_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    name = StringVar()
    input_name = Entry(first_fenetre, textvariable=name)
    input_name.pack(pady =(210,0))
    input_name.focus_set()
    input_name.bind("<Return>", (lambda event: play(name.get(), first_fenetre)))

    btnPlay = Button(first_fenetre, width = 10, height = 2, text = 'JOUER', relief = RAISED, command = lambda : play(name.get(), first_fenetre))
    btnPlay.pack(pady =(20,0), padx = 10)   
    btnRegister = Button(first_fenetre, width = 10, height = 2, text = 'S\'INSCRIRE', relief = RAISED, command = lambda : webbrowser.open('https://carboniferous-gener.000webhostapp.com/farwest/membre/register.php'))
    btnRegister.pack(pady = 20, padx = 10)   

    first_fenetre.mainloop()

    return on_play, name.get()

def play(name, first_fenetre):
    """Action à réaliser lorsque le joueur clique sur le bouton"""
    global on_play
    
    name_joueur = name
    if (name_joueur != ''):
        close(first_fenetre)
        on_play = 1
    else:
        error = Label(first_fenetre, text="Veuillez rentrer votre nom !")
        error.pack(side=BOTTOM, pady=1)

def replay_game(fenetre):
    """Action à réaliser lorsque le joueur clique sur le bouton"""
    global on_play
    
    close(fenetre)
    on_play = 1
    

def end_game(temps, stat):
    """Lance la fenetre de fin récapitulative"""
    global on_play

    on_play = 0

    # Création fenetre
    end_fenetre = Tk()
    end_fenetre.geometry('600x400')
    end_fenetre.title('Statistiques')

    # Variable à afficher
    game_duree = StringVar()
    game_score = StringVar()
    ennemis_elimines = StringVar()
    ennemis_echappes = StringVar()
    balles = StringVar()

    game_duree.set(temps)
    game_score.set(str(stat['game_score']))
    ennemis_elimines.set(str(stat['ennemi_elimine']))
    ennemis_echappes.set(str(stat['ennemi_echappe']))
    balles.set(str(stat['nb_balle']))

    # Création widget
    Frame1 = Frame(end_fenetre, width=500, height=500)
    Frame1.pack_propagate(False)
    Frame1.pack(pady=30)
    
    Frame2 = Frame(Frame1)
    Frame2.pack(pady=10)

    btnReplay = Button(Frame1, width = 10, height = 2, text = 'REJOUER',  relief = RAISED, command = lambda arg = end_fenetre: replay_game(arg))
    btnReplay.pack(side=LEFT, padx= 60)
    btnSite = Button(Frame1, width = 25, height = 2, text = 'Voir les infos sur le site', relief = RAISED, command = lambda : webbrowser.open('https://carboniferous-gener.000webhostapp.com/farwest/membre/membre.php'))
    btnSite.pack(side=RIGHT)

    # Résumer de la partie
    stat = Label(Frame2, text='Statistique de la partie:')
    f = font.Font(stat, stat.cget("font"))
    f.configure(underline = True)
    stat.configure(font=f)
    stat.pack(pady=5)

    stat_score = Label(Frame2, text='Score :')
    stat_score.pack()
    stat_score_result = Label(Frame2, textvariable=game_score)
    stat_score_result.pack()
    
    stat_temps = Label(Frame2, text='Durée :')
    stat_temps.pack()
    stat_temps_result = Label(Frame2, textvariable=game_duree)
    stat_temps_result.pack()

    stat_ennemi_elimine = Label(Frame2, text='Ennemis éliminés :')
    stat_ennemi_elimine.pack()
    stat_ennemi_elimine_result = Label(Frame2, textvariable=ennemis_elimines)
    stat_ennemi_elimine_result.pack()
    
    stat_ennemi_echappe = Label(Frame2, text='Ennemis échappés :')
    stat_ennemi_echappe.pack()
    stat_ennemi_echappe_result = Label(Frame2, textvariable=ennemis_echappes)
    stat_ennemi_echappe_result.pack()

    stat_balle_utilise = Label(Frame2, text='Balles utilisées :')
    stat_balle_utilise.pack()
    stat_balle_utilise_result = Label(Frame2, textvariable=balles)
    stat_balle_utilise_result.pack()
 
    end_fenetre.mainloop()

    return on_play


# Lancement du programme
on_play = 0
on_play, name = launcher()
    
while on_play:
    toDisplay = 0
    joueur = 0
    temps = 0
    stat = 0
    
    toDisplay, joueur, temps, stat = game(name)
    on_play = end_game(temps, stat)

