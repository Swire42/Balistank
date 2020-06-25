import terrain
import pygame

pygame.display.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)

terrain.dpu=10

terrain.genTerrain(3, 0.1, 1, "snow")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            exit()
    screen.blit(terrain.background, (0,0))
    pygame.display.flip()

