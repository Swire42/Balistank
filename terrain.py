import pygame
import pygame.gfxdraw
import math
import random
import time

pygame.display.init()
size = width, height = 1920, 1080
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

    def genPoints(self, xvalues):
        yvalues=[[0 for k in range(len(xvalues))] for j in range(len(self.funcs))]
        prev=[0 for k in range(len(xvalues))]
        cst=0
        der=[0 for k in range(len(xvalues))]

        for k in range(len(self.funcs)):
            for xi in range(len(xvalues)):
                prev[xi]=(prev[xi]-cst)*self.amorts[k]+cst + self.funcs[k].val(xvalues[xi])*math.sqrt((der[xi])**2 + 1)
                der[xi]*=self.amorts[k]
                yvalues[k][xi]=prev[xi]
            cst+=self.funcs[k].cst

        return yvalues

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
        allpts=self.genPoints([x/dpu for x in range(width)])
        for k in range(len(self.funcs)-1):
            pts=[(x, height-allpts[k][x]*dpu-0.5) for x in range(width)]
            pygame.draw.aalines(surface, self.colors[k], False, pts)
            pts=[(x, height-round(allpts[k][x]*dpu)) for x in range(width)]+[(x, height-round(allpts[k+1][x]*dpu)+2) for x in range(width-1, -1, -1)]
            pygame.gfxdraw.filled_polygon(surface, pts, self.colors[k])

background=pygame.Surface(size)
terrain=Terrain()

def genTerrain(amp):
    global terrain, background
    terrain=Terrain()
    background=pygame.Surface(size)
    terrain.skycolor=(32,128,255)

    f1=0.007
    f2=0.011
    terrain.add(TrigFunc(f1, f2, random.random()*amp+amp, random.random()*amp+amp, random.random()*10, random.random()*10, height/4/dpu), (10, 128, 0))
    terrain.add(TrigFunc(0, 0, 0, 0, 0, 0, -10), (10, 60, 5))

    n=1

    while ((terrain.cst(n)+terrain.amp(n))*dpu > 0):
        v=random.random()*0.25+0.15
        s=random.random()*0.25+0.1
        h=random.random()*0.25+0.5
        color=(255*v, 128*(s+h)*v, 64*s*v)

        minH=0.2*terrain.amp(n)+10

        terrain.add(TrigFunc(random.random()*0.01+0.01, random.random()*0.005+0.005, random.random()*10, random.random()*5, random.random()*10, random.random()*10, -(random.random()*10+minH)), color, 0.8)
        n+=1

    terrain.display(background, height, width)

print(time.time())
genTerrain(30)
print(time.time())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            exit()
    screen.blit(background, (0,0))
    pygame.display.flip()
