import pygame
import pygame.gfxdraw
import math
import random
import time

# Terrain generator
# by Victor MIQUEL
# github.com/dido11/

pygame.display.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

dpu=1 # dot per unit

class TrigFunc:
    def __init__(self, freqa, freqb, ampa, ampb, phasea, phaseb, const):
        self.fa=freqa
        self.fb=freqb
        self.aa=ampa
        self.ab=ampb
        self.pa=phasea
        self.pb=phaseb
        self.cst=const

    def val(self, x, amort=1):
        return amort*( self.aa*math.sin(self.fa*x+self.pa) + self.ab*math.sin(self.fb*x+self.pb) ) + self.cst

    def der(self, x, amort=1):
        return amort*(self.aa*self.fa*math.cos(self.fa*x+self.pa) + self.ab*self.fb*math.cos(self.fb*x+self.pb))


class Terrain:
    def __init__(self):
        self.funcs=[]
        self.amorts=[]
        self.colors=[]
        self.skycolor=(0,0,0)

    def add(self, func, color, amort=1):
        self.funcs.append(func)
        self.colors.append(color)
        self.amorts.append(amort)

    def val(self, n, x):
        amort=1
        ret=0
        der=0
        for k in range(n, -1, -1):
            ret+=self.funcs[k].val(x, amort)*math.sqrt((der)**2 + 1)
            der+=self.funcs[k].der(x, amort)
            amort*=self.amorts[k]
        return ret

    def der(self, n, x):
        amort=1
        ret=0
        for k in range(n, -1, -1):
            ret+=self.funcs[k].der(x, amort)
            amort*=self.amorts[k]
        return ret

    def cst(self, n):
        return sum([f.cst for f in self.funcs[:n]])

    def amp(self, n):
        amort=1
        ret=0
        for k in range(n-1, -1, -1):
            ret+=amort*( self.funcs[k].aa + self.funcs[k].ab )
            amort*=self.amorts[k]
        return ret

    def displaySky(self, surface):
        surface.fill(self.skycolor)

    def display(self, surface, height, width):
        self.displaySky(surface)
        for k in range(len(self.funcs)-1):
            pts=[(x, self.val(k, x/dpu)*dpu-0.5) for x in range(width)]
            pygame.draw.aalines(screen, self.colors[k], False, pts)
            pts=[(x, round(self.val(k, x/dpu)*dpu)) for x in range(width)]+[(x, round(self.val(k+1, x/dpu)*dpu)+2) for x in range(width-1, -1, -1)]
            pygame.gfxdraw.filled_polygon(screen, pts, self.colors[k])




def genBasic():
    ter=Terrain()
    ter.skycolor=(32,128,255)

    #ter.add(TrigFunc(0.01, 0.02, 60, 50, 1, 0, 500), (10, 128, 0))
    f1=random.random()*0.005+0.005
    f2=f1+random.random()*0.005+0.005
    ter.add(TrigFunc(f1, f2, random.random()*30+30, random.random()*30+30, random.random()*10, random.random()*10, 500), (10, 128, 0))
    ter.add(TrigFunc(0, 0, 0, 0, 0, 0, 10), (10, 60, 5))

    n=1

    while ((ter.cst(n)-ter.amp(n))*dpu < height):
        v=random.random()*0.25+0.15
        s=random.random()*0.25+0.1
        h=random.random()*0.25+0.5
        color=(255*v, 128*(s+h)*v, 64*s*v)

        ter.add(TrigFunc(random.random()*0.01+0.01, random.random()*0.005+0.005, random.random()*10, random.random()*5, random.random()*10, random.random()*10, random.random()*10+20), color, 0.8)
        n+=1

    ter.display(screen, height, width)

print(time.time())
genBasic()
print(time.time())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            exit()
    pygame.display.flip()
