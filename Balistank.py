import numpy as np
import pygame
import math
import random
import os
import time
import pathlib
import terrain
import option
import menu
from scipy.integrate import*

###Initialisation des variables utiles aux classes

pygame.display.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 300)
size = width, height = 1920,1080
screen = pygame.display.set_mode(size,flags = pygame.FULLSCREEN)
path = pathlib.Path(__file__).parent.absolute()

###Génération du terrain

dpu=12.5 #dot per unit
terrain.dpu = dpu
HP_img = pygame.transform.scale(myfont.render("HP",True,(255,255,255)),(int(width/32),int(height/32)))

###Définition des classes

class Bullet:
    def __init__(self, position, force, alpha):
        global bullet
        bullet = self
        self.angle = alpha
        self.position = position
        self.speed = force * np.cos(np.radians(alpha)), force*np.sin(np.radians(alpha))
        self.m = 5
        self.clock = 0

    def updateSpeed(self,dt):
        b=-0.5*(1.29)*((np.pi*0.22**2)/4)*(0.45)
        g=9.81
        def F(x,y):
            F1=(b/self.m)*x* np.sqrt(x**2+y**2)
            F2=(b/self.m)*y* np.sqrt(x**2+y**2)-g
            return (F1,F2)
        xPrime, yPrime = F(self.speed[0],self.speed[1])
        X = self.speed[0] + xPrime*dt
        Y = self.speed[1] + yPrime*dt
        return X,Y


class Tank:
    def __init__(self,id,x):
        self.id = id
        entity[self.id] = (self)
        self.sprite = [pygame.image.load(os.path.join(path,"img","cannon 1.png")).convert_alpha(), pygame.image.load(os.path.join(path,"img","Player " + str(id) + ".png")).convert_alpha()]
        self.cannon_width,self.cannon_height= 0.5,3
        self.width, self.height = 4,2
        self.sprite[0] = pygame.transform.scale(self.sprite[0],(int(self.cannon_width*dpu),int(self.cannon_height*dpu)))
        self.sprite[1] = pygame.transform.scale(self.sprite[1],(int(self.width*dpu),int(self.height*dpu)))
        self.position=[x,terrain.terrain.val(0,x)]
        self.speed = 15
        self.HP = 100
        self.HPmax = float(self.HP)
        self.angle = float()
        self.force, self.cannon_angle = 20,45
        self.fuel = 10
        if self.id%2==1:
            self.cannon_angle += 90
            self.sprite[1] = pygame.transform.flip(self.sprite[1],True,False)

    def shooting(self):
        position,force,cannon_angle=[self.position[0],self.position[1]+self.height/2], float(self.force), float(self.cannon_angle + np.degrees(self.angle))
        Bullet(position,force,cannon_angle)

class Player:
    def __init__(self,x):
        self.id = len(players)
        self.name = ""
        self.tank = Tank(int(self.id),x)
        self.score = 0
        self.score_img = pygame.transform.scale(myfont.render("Score : "+str(self.score),True,(255,255,255)),(int(width/8),int(height/32)))

class Wall:
    def __init__(self,x):
        self.position = x,0
        self.width, self.height = 2, height*2/(3*dpu)

###Initialisation des variables

Flag = True
Fullscreen = True
esc_Menu = False
opt_Menu = False
Win = False
InGame = False

menu_escape = m_width, m_height = [32*dpu,48*dpu]
menu_escape=[[(150,150,150),[width/2 - m_width/2,height/2 - m_height/2,m_width,m_height]],
            [(140,140,140),[width/2 - 3*m_width/8 , height/2 - 3*m_height/8,3*m_width/4,m_height/3], pygame.transform.scale(myfont.render("Options",True,(255,255,255)),(int(m_width*3/4),int(m_height/3)))],
            [(140,140,140),[width/2 - 3*m_width/8 , height/2 + m_height/24,3*m_width/4,m_height/3], pygame.transform.scale(myfont.render("Quit",True,(255,255,255)),(int(m_width*3/4),int(m_height/3)))]]
menu_opt = opt_width, opt_height = [144*dpu, 72*dpu]
menu_opt = option.genMenu(menu_opt,width,height,myfont)

def init():
    global t, turn, players, bullet, entity, walls, nb_players, terrain, InGame, varpower
    players = []
    entity = []
    walls = []
    bullet = 0
    nb_players, Walls, terrain_data = menu.menu(screen, myfont, size, dpu)
    terrain.genTerrain(terrain_data[0],terrain_data[1],terrain_data[2],terrain_data[3])

    def initplayer(i,x):
        players.append(Player(x))

    entity = [0 for i in range(nb_players)]
    x = 1/8
    for i in range(nb_players):
        initplayer(i,x*width/dpu)
        x += ((-1)**i *(6-2*i))/8
    if Walls:
        for i in range(1,nb_players):
            walls.append(Wall(width*i/(nb_players*dpu)))
    turn = random.randint(0,nb_players-1)
    t = time.perf_counter()
    InGame = True
    score = pygame.transform.scale(myfont.render("Score : "+str(players[i].score),True,(255,255,255)),(int(width/8),int(height/32)))
    varpower = -1

def reinit():
    global Win
    x = 1/8
    for i in range(nb_players):
        players[i].tank = Tank(int(players[i].id),x*width/dpu)
        x += ((-1)**i *(6-2*i))/8
    Win = False

###Fonctions calculatoires

def setAngle():
    for p in players:
        if p.tank != 0 :
            p.tank.angle = np.arctan(terrain.terrain.der(0,p.tank.position[0]))

def tangente(a):
    d = terrain.terrain.der(0,a)
    a,b=d,terrain.terrain.val(0,a)-d*a
    return(a,b)

###Gestions des "input"

def regularInput(ev):
    global varpower,cannon_height,force
    for event in ev:
        if bullet == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            varpower = 0
            cannon_height = players[turn].tank.cannon_height
            force = players[turn].tank.force
        if bullet == 0 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            players[turn].tank.shooting()
            players[turn].tank.cannon_height = cannon_height
            players[turn].tank.sprite[0] = pygame.transform.scale(players[turn].tank.sprite[0],(int(players[turn].tank.cannon_width*dpu),int(players[turn].tank.cannon_height*dpu)))
            players[turn].tank.force = force
            varpower = -1
    if ((pygame.key.get_pressed()[pygame.K_d]) or (pygame.key.get_pressed()[pygame.K_RIGHT])) and players[turn].tank.fuel > 0:
        distance = players[turn].tank.speed * np.cos(players[turn].tank.angle)*dt
        players[turn].tank.position[0] += distance
        players[turn].tank.position[1] = terrain.terrain.val(0, players[turn].tank.position[0])
        players[turn].tank.fuel -= distance
        if players[turn].tank.position[0] > width/dpu:
            players[turn].tank.position[0] = width/dpu
            players[turn].tank.position[1] = terrain.terrain.val(0, players[turn].tank.position[0])
        for w in walls:
            if tankHittingWall(w,players[turn].tank):
                players[turn].tank.position[0] = w.position[0]-w.width/2-np.cos(players[turn].tank.angle)*players[turn].tank.width/2
                players[turn].tank.position[1] = terrain.terrain.val(0, players[turn].tank.position[0])
    if (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]) and players[turn].tank.fuel > 0:
        distance = players[turn].tank.speed *np.cos(players[turn].tank.angle)*dt
        players[turn].tank.position[0] -= distance
        players[turn].tank.position[1] = terrain.terrain.val(0, players[turn].tank.position[0])
        players[turn].tank.fuel -= distance
        if players[turn].tank.position[0] < 0:
            players[turn].tank.position[0] = 0
            players[turn].tank.position[1] = terrain.terrain.val(0, players[turn].tank.position[0])
        for w in walls:
            if tankHittingWall(w,players[turn].tank):
                players[turn].tank.position[0] = w.position[0]+w.width/2+np.cos(players[turn].tank.angle)*players[turn].tank.width/2
                players[turn].tank.position[1] = terrain.terrain.val(0, players[turn].tank.position[0])
    if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
        angle = players[turn].tank.cannon_angle
        if turn%2 == 0:
            players[turn].tank.cannon_angle += 30*dt
            if angle <=90 and players[turn].tank.cannon_angle > 90:
                players[turn].tank.sprite[1] = pygame.transform.flip(players[turn].tank.sprite[1],True,False)
        else:
            players[turn].tank.cannon_angle -= 30*dt
            if angle >=90 and players[turn].tank.cannon_angle < 90:
                players[turn].tank.sprite[1] = pygame.transform.flip(players[turn].tank.sprite[1],True,False)
    if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
        angle = players[turn].tank.cannon_angle
        if turn%2 == 0:
            players[turn].tank.cannon_angle -= 30*dt
            if angle >=90 and players[turn].tank.cannon_angle < 90:
                players[turn].tank.sprite[1] = pygame.transform.flip(players[turn].tank.sprite[1],True,False)
        else:
            players[turn].tank.cannon_angle += 30*dt
            if angle <=90 and players[turn].tank.cannon_angle > 90:
                players[turn].tank.sprite[1] = pygame.transform.flip(players[turn].tank.sprite[1],True,False)
    if players[turn].tank.cannon_angle < 0:
        players[turn].tank.cannon_angle = 0
    if players[turn].tank.cannon_angle > 180:
        players[turn].tank.cannon_angle = 180
    setAngle()


def escMenuInput(ev):
    global esc_Menu, opt_Menu, Flag
    if isInRect(pygame.mouse.get_pos(),menu_escape[1][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                esc_Menu, opt_Menu = False, True
        if pygame.mouse.get_pressed()[0]:
            menu_escape[1][0] = (120,120,120)
        else:
            menu_escape[1][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu_escape[2][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                Flag = False
        if pygame.mouse.get_pressed()[0]:
            menu_escape[2][0] = (120,120,120)
        else:
            menu_escape[2][0] = (130,130,130)
    else:
        menu_escape[1][0] = (140,140,140)
        menu_escape[2][0] = (140,140,140)

def optMenuInput(ev):
    global screen,esc_Menu, opt_Menu, Flag, Fullscreen
    if isInRect(pygame.mouse.get_pos(),menu_opt[1][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                resize((1920,1080))
        if pygame.mouse.get_pressed()[0]:
            menu_opt[1][0] = (120,120,120)
        else:
            menu_opt[1][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu_opt[2][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                resize((1600,900))
        if pygame.mouse.get_pressed()[0]:
            menu_opt[2][0] = (120,120,120)
        else:
            menu_opt[2][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu_opt[3][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                resize((1280,720))
        if pygame.mouse.get_pressed()[0]:
            menu_opt[3][0] = (120,120,120)
        else:
            menu_opt[3][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu_opt[4][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                resize((960,540))
        if pygame.mouse.get_pressed()[0]:
            menu_opt[4][0] = (120,120,120)
        else:
            menu_opt[4][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu_opt[5][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                if Fullscreen:
                    menu_opt[5][0] = (250,0,0)
                    Fullscreen = False
                    screen = pygame.display.set_mode(size)
                else:
                    menu_opt[5][0] = (0,250,0)
                    Fullscreen = True
                    screen = pygame.display.set_mode(size,flags = pygame.FULLSCREEN)
        if pygame.mouse.get_pressed()[0]:
            if Fullscreen:
                menu_opt[5][0] = (0,230,0)
            else:
                menu_opt[5][0] = (230,0,0)
        else:
            if Fullscreen:
                menu_opt[5][0] = (0,240,0)
            else:
                menu_opt[5][0] = (240,0,0)
    else:
        menu_opt[1][0] = (140,140,140)
        menu_opt[2][0] = (140,140,140)
        menu_opt[3][0] = (140,140,140)
        menu_opt[4][0] = (140,140,140)
        if Fullscreen:
            menu_opt[5][0] = (0,250,0)
        else:
            menu_opt[5][0] = (250,0,0)
    for event in ev:
        if (event.type == pygame.KEYDOWN) and event.key == pygame.K_ESCAPE:
            opt_Menu = False



###Fonctions booleennes

def hitting(tank,bullet):
    '''renvoie True si le tank est en contact avec la balle'''
    a,b = tangente(tank.position[0])
    x,y = bullet.position
    if (a > 0):
        alpha = tank.angle
        cos = np.cos(alpha)
        sin = np.sin(alpha)
        perpendiculaire = -1/a * x + tank.position[1] + 1/a * tank.position[0]
        if(y <= a*x + b + tank.height/cos and y >= a*x+b) and (y <= perpendiculaire + tank.width/(2 * sin) and y >= perpendiculaire - tank.width/(2 * sin)):
            return(True)
        else:
            return(False)
    if (a < 0):
        x,y = bullet.position
        alpha = tank.angle
        cos = np.cos(alpha)
        sin = np.sin(alpha)
        perpendiculaire = -1/a * x + tank.position[1] + 1/a * tank.position[0]
        if(y <= a*x + b + tank.height/cos and y >= a*x+b) and (y >= perpendiculaire + tank.width/(2 * sin) and y <= perpendiculaire - tank.width/(2 * sin)):
            return(True)
        else:
            return(False)
    else:
        if (y <= tank.position[1] + tank.height and y >= tank.position[1]) and (x <= tank.position[0] + tank.width/2 and x >= tank.position[0] - tank.width/2 ):
            return(True)
        else:
            return(False)

def bulletHittingWall(wall,bullet):
    x,y = bullet.position
    if (y <= wall.position[1] + wall.height) and (x <= wall.position[0] + wall.width/2 and x >= wall.position[0]-wall.width/2):
        return(True)
    else:
        return(False)

def tankHittingWall(wall,tank):
    if (tank.position[0]-np.cos(tank.angle)*tank.width/2 <= wall.position[0] + wall.width/2 and tank.position[0]-np.cos(tank.angle)*tank.width/2 >= wall.position[0] - wall.width/2) or (tank.position[0]+np.cos(tank.angle)*tank.width/2 >= wall.position[0] - wall.width/2 and tank.position[0]+np.cos(tank.angle)*tank.width/2 <= wall.position[0] + wall.width/2):
        return(True)
    else:
        return(False)

def isInRect(pos,rect):
    x,y = pos
    if (x >= rect[0] and x <= rect[0]+rect[2]) and (y >= rect[1] and y <= rect[1]+rect[3]):
        return(True)
    else:
        return(False)



###Fonctions d'affichage

def blitWithRotateCenter(surf, entity):
    rotated_sprite = pygame.transform.rotate(entity.sprite[1], entity.angle*180/np.pi)
    position = [i*dpu for i in entity.position]
    new_rect = rotated_sprite.get_rect(center = ((position[0]-np.sin(entity.angle)*(entity.height*dpu/2)), (height - position[1]-np.cos(entity.angle) * (entity.height*dpu/2)))).topleft
    surf.blit(rotated_sprite, new_rect)

def blitCannon(surf, entity):
    angle = np.radians(entity.cannon_angle) + entity.angle
    rotated_sprite = pygame.transform.rotate(entity.sprite[0], np.degrees(angle-np.pi/2))
    position = [i*dpu for i in entity.position]
    new_rect = rotated_sprite.get_rect(center = ((position[0]-np.sin(entity.angle)*(entity.height*dpu/2)) + np.cos(angle)*entity.cannon_height*dpu/2, (height - position[1]- np.sin(angle)*entity.cannon_height*dpu/2 -np.cos(entity.angle) * (entity.height*dpu/2)))).topleft
    surf.blit(rotated_sprite, new_rect)

def blitMenu(menu):
    for button in menu:
        pygame.draw.rect(screen,button[0],button[1])
        pygame.draw.rect(screen,(0,0,0),button[1],math.ceil(0.16*dpu))
        if len(button) == 3:
            screen.blit(button[2],(button[1][0],button[1][1]))

def resize(newsize):
    global dpu, size, width, height,menu_escape, menu_opt, opt_width, opt_height, HP_img
    ratio = newsize[0]/size[0]
    size = width, height = newsize
    if Fullscreen:
        screen = pygame.display.set_mode(size,flags = pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(size)
    dpu = ratio *dpu
    terrain.dpu = dpu
    terrain.size = terrain.width, terrain.height = size
    terrain.terrain.display(terrain.background, terrain.height, terrain.width)
    for e in entity:
        e.sprite = [pygame.image.load(os.path.join(path,"img","cannon 1.png")).convert_alpha(), pygame.image.load(os.path.join(path,"img","Player " + str(e.id) + ".png")).convert_alpha()]
        e.sprite[0] = pygame.transform.scale(e.sprite[0],(int(e.cannon_width*dpu),int(e.cannon_height*dpu)))
        e.sprite[1] = pygame.transform.scale(e.sprite[1],(int(e.width*dpu),int(e.height*dpu)))
    menu_escape = m_width, m_height = [32*dpu,48*dpu]
    menu_escape=[[(150,150,150),[width/2 - m_width/2,height/2 - m_height/2,m_width,m_height]],
                [(140,140,140),[width/2 - 3*m_width/8 , height/2 - 3*m_height/8,3*m_width/4,m_height/3], pygame.transform.scale(myfont.render("Options",True,(255,255,255)),(int(m_width*3/4),int(m_height/3)))],
                [(140,140,140),[width/2 - 3*m_width/8 , height/2 + m_height/24,3*m_width/4,m_height/3], pygame.transform.scale(myfont.render("Quit",True,(255,255,255)),(int(m_width*3/4),int(m_height/3)))]]
    for w in walls:
        w.position = x,height
        w.width, w.height = 2*dpu, height*2/3
    menu_opt = opt_width, opt_height = [144*dpu, 72*dpu]
    menu_opt  = option.genMenu(menu_opt,width, height,myfont)
    HP_img = pygame.transform.scale(myfont.render("HP",True,(255,255,255)),(int(width/32),int(height/32)))
    for p in players:
        p.score_img = pygame.transform.scale(myfont.render("Score : "+str(p.score),True,(255,255,255)),(int(width/8),int(height/32)))

def blitHUD():
    global score , HP_img
    for i in range(nb_players):
        position = ((-1)**i*(1+i*2)%16)*width/16,height/16
        if players[i].tank != 0:
            ratio = (players[i].tank.HP/players[i].tank.HPmax)
            if ratio >= 0:
                pygame.draw.rect(screen,(255*(1-ratio),ratio*255,0),[position[0],position[1],width*ratio*3/16,height/32])
        pygame.draw.rect(screen,(0,0,0),[position[0],position[1],width*3/16,height/32],math.ceil(0.16*dpu))
        screen.blit(players[i].score_img,(position[0],position[1]+height/32))
        screen.blit(HP_img,(position[0]-(width/32),position[1]))

###Fonction fondamentales

def gameplay():
    global t, dt, bullet, varpower, cannon_height,force
    dt = time.perf_counter() - t
    t = time.perf_counter()
    # print(round(1/dt))
    if bullet != 0:
        bullet.clock += dt
        bullet.speed = bullet.updateSpeed(dt)
        bullet.position[0] += bullet.speed[0]*dt
        bullet.position[1] += bullet.speed[1]*dt
    if varpower != -1:
        varpower += dt
        coef = (np.cos(varpower+np.pi)*0.5)+1.5
        players[turn].tank.cannon_height = cannon_height * coef
        players[turn].tank.force = force * coef
        players[turn].tank.sprite[0] = pygame.transform.scale(players[turn].tank.sprite[0],(int(players[turn].tank.cannon_width*dpu),int(players[turn].tank.cannon_height*dpu)))

def event():
    '''Gère les événements'''
    global players, Flag, Win, esc_Menu, opt_Menu, turn, bullet, InGame
    #Gestion de la balle
    if bullet!=0:
        for tank in [p.tank for p in players]:
            if bullet != 0 and tank !=0 and (tank.id != turn or bullet.clock >= 0.3) and hitting(tank,bullet):
                tank.HP -= (1/2) * bullet.m * np.sqrt((bullet.speed[0]**2)+(bullet.speed[1]**2))
                players[turn].tank.fuel = 10
                turn = (turn + 1) % nb_players
                bullet = 0
                if tank.HP <= 0:
                    players[tank.id].tank = 0
                    entity[tank.id] = 0
        while players[turn].tank == 0:
            turn = (turn + 1) % nb_players
        counter = 0
        for i in entity:
            if i == 0:
                counter +=1
        if counter == nb_players-1:
            Win = True
    if bullet != 0 and bullet.position[1] <= terrain.terrain.val(0,bullet.position[0]):
        bullet = 0
        players[turn].tank.fuel = 10
        turn = (turn + 1) % nb_players
        while players[turn].tank == 0:
            turn = (turn + 1) % nb_players
    for w in walls:
        if bullet != 0 and bulletHittingWall(w,bullet):
            bullet = 0
            players[turn].tank.fuel = 10
            turn = (turn + 1) % nb_players
            while players[turn].tank == 0:
                turn = (turn + 1) % nb_players
    #Gestion des inputs
    ev= pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            Flag = False
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                esc_Menu = not(esc_Menu)
    if (pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]):
        Flag = False
    if not esc_Menu and not opt_Menu:
        regularInput(ev)
    elif esc_Menu:
        escMenuInput(ev)
    else:
        optMenuInput(ev)
    if Win == True:
        players[turn].score += 1
        for p in players:
            p.score_img = pygame.transform.scale(myfont.render("Score : "+str(p.score),True,(255,255,255)),(int(width/8),int(height/32)))
        reinit()
        for p in players:
            if p.score == 3:
                InGame = False

def display():
    screen.blit(terrain.background,(0,0))
    if bullet != 0:
        pygame.draw.circle(screen,(40,40,40),(int(bullet.position[0]*dpu),height-int(bullet.position[1]*dpu)),3)
    for w in walls:
        pygame.draw.rect(screen,(120,120,120),((w.position[0]*dpu-w.width*dpu/2),height/3,w.width*dpu,w.height*dpu))
    for e in entity:
        if e != 0:
            blitCannon(screen, e)
            blitWithRotateCenter(screen, e)
    if esc_Menu == True:
        blitMenu(menu_escape)
    elif opt_Menu == True:
        blitMenu(menu_opt)
    else:
        blitHUD()
    pygame.display.flip()

def close():
    pygame.display.quit()

###Main

while Flag:
    if InGame == False:
        init()
    gameplay()
    event()
    display()
close()
