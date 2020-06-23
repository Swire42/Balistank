import pygame


def genMenu(menu_opt,width, height,myfont):
    opt_width, opt_height = menu_opt
    menu = [[(150,150,150),[width/2 - opt_width/2,height/2 - opt_height/2,opt_width,opt_height]],
            [(140,140,140),[width/2 - opt_width*9/20, height/2 - opt_height*7/16,opt_width*2/5,opt_height/16], pygame.transform.scale(myfont.render("1920x1080",True,(255,255,255)),(int(opt_width/5),int(opt_height/16)))],
            [(140,140,140),[width/2 - opt_width*9/20, height/2 - opt_height*5/16,opt_width*2/5,opt_height/16], pygame.transform.scale(myfont.render("1600x900",True,(255,255,255)),(int(opt_width/5),int(opt_height/16)))],
            [(140,140,140),[width/2 - opt_width*9/20, height/2 - opt_height*3/16,opt_width*2/5,opt_height/16], pygame.transform.scale(myfont.render("1280x720",True,(255,255,255)),(int(opt_width/5),int(opt_height/16)))],
            [(140,140,140),[width/2 - opt_width*9/20, height/2 - opt_height*1/16,opt_width*2/5,opt_height/16], pygame.transform.scale(myfont.render("960x540",True,(255,255,255)),(int(opt_width/5),int(opt_height/16)))],
            [(255,0,0),[width/2 - opt_width*9/20, height/2 + opt_height*1/16,opt_height/16,opt_height/16], pygame.transform.scale(myfont.render("   Fullscreen",True,(255,255,255)),(int(opt_width/5),int(opt_height/16)))]]
    return(menu)

