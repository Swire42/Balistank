import pygame
import math
import os


def menu(screen, myfont, size, dpu):
    Flag = True
    Quit = False
    width, height = size
    nb_players = 2
    menu = genMenu(width, height, myfont, dpu, nb_players)
    Walls = True
    terrain = (0, 0, 1,"grass")
    path = os.path.abspath("")
    background = pygame.image.load(os.path.join(path,"img","menu_background.png")).convert()
    background = pygame.transform.scale(background,size)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load(os.path.join(path,"msc","balistank.mp3"))
    pygame.mixer.music.play(loops=-1)
    while Flag:
        Flag, Quit, menu, Walls, terrain, nb_players = event(Flag, Quit, menu, Walls, terrain, nb_players, myfont,dpu)
        display(screen,background, menu, dpu, myfont, width, height)
    pygame.mixer.quit()
    return(Quit,nb_players, Walls, terrain)

def isInRect(pos,rect):
    x,y = pos
    if (x >= rect[0] and x <= rect[0]+rect[2]) and (y >= rect[1] and y <= rect[1]+rect[3]):
        return(True)
    else:
        return(False)

def event(Flag, Quit, menu, Walls, terrain, nb_players, myfont, dpu):
    flat = (0, 0, 1,"grass")
    plains = (2, 0.2, 1,"desert")
    hills = (4, 0.2, 1,"snow")
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            Flag, Quit= False,True
    if (pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]):
        Flag, Quit = False,True
    if isInRect(pygame.mouse.get_pos(),menu[0][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                terrain = flat
                for m in menu[:3]:
                    m[0] = (140,140,140)
        if pygame.mouse.get_pressed()[0]:
            menu[0][0] = (120,120,120)
        else:
            menu[0][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu[1][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                terrain = plains
                for m in menu[:3]:
                    m[0] = (140,140,140)
        if pygame.mouse.get_pressed()[0]:
            menu[1][0] = (120,120,120)
        else:
            menu[1][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu[2][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                terrain = hills
                for m in menu[:3]:
                    m[0] = (140,140,140)
        if pygame.mouse.get_pressed()[0]:
            menu[2][0] = (120,120,120)
        else:
            menu[2][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu[3][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                if Walls:
                    menu[3][0] = (250,0,0)
                    Walls = False
                else:
                    menu[3][0] = (0,250,0)
                    Walls = True
        if pygame.mouse.get_pressed()[0]:
            if Walls:
                menu[3][0] = (0,230,0)
            else:
                menu[3][0] = (230,0,0)
        else:
            if Walls:
                menu[3][0] = (0,240,0)
            else:
                menu[3][0] = (240,0,0)
    elif isInRect(pygame.mouse.get_pos(),menu[4][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP and nb_players > 2:
                nb_players -= 1
                menu[6][2] = pygame.transform.scale(myfont.render(str(nb_players),True,(0,0,0)),(int(6*dpu),int(6*dpu)))
        if pygame.mouse.get_pressed()[0]:
            menu[4][0] = (120,120,120)
        else:
            menu[4][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu[5][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP and nb_players < 4:
                nb_players += 1
                menu[6][2]=pygame.transform.scale(myfont.render(str(nb_players),True,(0,0,0)),(int(6*dpu),int(6*dpu)))
        if pygame.mouse.get_pressed()[0]:
            menu[5][0] = (120,120,120)
        else:
            menu[5][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu[7][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                Flag = False
        if pygame.mouse.get_pressed()[0]:
            menu[7][0] = (120,120,120)
        else:
            menu[7][0] = (130,130,130)
    elif isInRect(pygame.mouse.get_pos(),menu[8][1]):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                Flag, Quit = False,True
        if pygame.mouse.get_pressed()[0]:
            menu[8][0] = (240,0,0)
        else:
            menu[8][0] = (250,0,0)
    else:
        menu[0][0] = (140,140,140)
        menu[1][0] = (140,140,140)
        menu[2][0] = (140,140,140)
        if Walls:
            menu[3][0] = (0,250,0)
        else:
            menu[3][0] = (250,0,0)
        menu[4][0] = (140,140,140)
        menu[5][0] = (140,140,140)
        menu[7][0] = (140,140,140)
        menu[8][0] = (255,0,0)
    if terrain == flat:
        menu[0][0] = (0,255,0)
    elif terrain == plains:
        menu[1][0] = (0,255,0)
    elif terrain == hills:
        menu[2][0] = (0,255,0)
    return(Flag,Quit, menu, Walls, terrain, nb_players)

def display(screen,background,menu,dpu,myfont,width,height):
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    blitMenu(screen,menu,dpu,myfont,width,height)
    pygame.display.flip()

def genMenu(width, height, myfont, dpu, nb_players):
    menu = [[(140,140,140),[width/2 - width*9/20, height/2 - height*5/16,width*2/5,height/16], pygame.transform.scale(myfont.render("Plains",True,(255,255,255)),(int(width/6),int(height/16)))],
            [(140,140,140),[width/2 - width*9/20, height/2 - height*3/16,width*2/5,height/16], pygame.transform.scale(myfont.render("Desert",True,(255,255,255)),(int(width/6),int(height/16)))],
            [(140,140,140),[width/2 - width*9/20, height/2 - height*1/16,width*2/5,height/16], pygame.transform.scale(myfont.render("Extreme Hills",True,(255,255,255)),(int(width*2/5),int(height/16)))],
            [(255,0,0),[width/2 - width*9/20, height/2 + height*1/16,height/16,height/16], pygame.transform.scale(myfont.render("  Walls",True,(255,255,255)),(int(width*2/10),int(height/16)))],
            [(140,140,140),[6*width/10, height/2 - 3*dpu,6*dpu,6*dpu], pygame.transform.scale(myfont.render("-",True,(255,255,255)),(int(6*dpu),int(6*dpu)))],
            [(140,140,140),[6*width/10 + 12*dpu, height/2 - 3*dpu,6*dpu,6*dpu], pygame.transform.scale(myfont.render("+",True,(255,255,255)),(int(6*dpu),int(6*dpu)))],
            [(255,255,255),[6*width/10 + 6*dpu, height/2 - 3*dpu,6*dpu,6*dpu], pygame.transform.scale(myfont.render(str(nb_players),True,(0,0,0)),(int(6*dpu),int(6*dpu)))],
            [(140,140,140),[width/2-width/6, height - height/4,width/3,height/4], pygame.transform.scale(myfont.render("Play!",True,(255,255,255)),(int(width/3),int(height/4)))],
            [(250,0,0),[width-width/32,0,width/32,width/32], pygame.transform.scale(myfont.render("X",True,(255,255,255)),(int(width/32),int(width/32)))]]
    return(menu)

def blitMenu(screen,menu,dpu,myfont,width,height):
    text = pygame.transform.scale(myfont.render("Balistank",True,(255,255,255)),(int(width/3),int(height/8)))
    screen.blit(text,(width/2-width/6,0))
    text = pygame.transform.scale(myfont.render("Players:",True,(255,255,255)),(int(18*dpu),int(6*dpu)))
    screen.blit(text,(width/2, height/2 - 9*dpu))
    for button in menu:
        pygame.draw.rect(screen,button[0],button[1])
        pygame.draw.rect(screen,(0,0,0),button[1],math.ceil(0.16*dpu))
        if len(button) == 3:
            screen.blit(button[2],(button[1][0],button[1][1]))

