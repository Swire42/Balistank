import pygame
import pygame.gfxdraw
import math
import random
import time

# Terrain generator
# by Victor Miquel
# github.com/dido11

# usage : genTerrain(amplitude, baseFrequency, layerHeight, biome), creates a Background surface, a Terrain and blit the terrain on the surface.

size = width, height = 1920, 1080
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

def genTerrain(amp, freq, layerSize, biome="grass"):
    assert biome in ["grass", "snow", "desert"], "unknow biome "+biome

    global terrain, background
    terrain=Terrain()
    background=pygame.Surface(size)
    terrain.skycolor=(32,128,255)

    f1=freq*0.7
    f2=freq*1.1
    if biome=="grass":
        color1=(10, 128, 0)
        color2=(10, 60, 5)
    elif biome=="snow":
        color1=(255, 255, 255)
        color2=(225, 225, 225)
    elif biome=="desert":
        color1=(255, 245, 0)
        color2=(215, 205, 0)
    terrain.add(TrigFunc(f1, f2, random.random()*amp+amp, random.random()*amp+amp, random.random()*(2*math.pi), random.random()*(2*math.pi), height/4/dpu), color1)
    terrain.add(TrigFunc(0, 0, 0, 0, 0, 0, -layerSize), color2)

    n=1

    while ((terrain.cst(n)+terrain.amp(n))*dpu > 0):
        if biome=="grass":
            v=random.random()*0.25+0.15
            s=random.random()*0.25+0.1
            h=random.random()*0.25+0.5
            color=(255*v, 128*(s+h)*v, 64*s*v)

        elif biome=="snow":
            v=random.random()*0.25+0.15
            s=random.random()*0.15+0.6
            h=random.random()*0.25+0.5
            color=(255*v, 128*(s+h)*v, 128*s*v)

        elif biome=="desert":
            v=random.random()*0.15+0.7
            h=random.random()*0.25+0.05
            color=(255*v, 255*(1-h)*v, 0)

        minH=0.2*terrain.amp(n)+layerSize

        terrain.add(TrigFunc(random.random()*freq+freq, random.random()*freq*0.5+freq*0.5, random.random()*layerSize, random.random()*layerSize*0.5, random.random()*(2*math.pi), random.random()*(2*math.pi), -(random.random()*layerSize+minH)), color, 0.8)
        n+=1

    terrain.display(background, height, width)

