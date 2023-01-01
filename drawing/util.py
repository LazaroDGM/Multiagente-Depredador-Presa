import pygame
from pygame.locals import *

ORANGE = (255, 165, 0)
DARKORANGE = (255, 140, 0)
LIGHTSALMON = (255, 160, 122)
YELLOW = (255, 255, 0)
KHAKI = (240, 230, 140)
MEDIUMORCHID = (186, 85, 211)
MEDIUMPURPLE = (147, 112, 219)
PURPLE = (128, 0, 128)
VIOLET = (238, 130, 238)
GREENYELLOW = (173, 255, 47)
PALEGREEN = (152, 251, 152)
GREEN = (0, 128, 0)
MEDIUMAQUAMARINE = (102, 205, 170)
DARKCYAN = (0, 139, 139)
BLUE = (0, 0, 255)
MAROON = (128, 0, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

def draw_diamond(screen, position, color):
    y, x = position
    pygame.draw.polygon(screen, color, [[x * 40 + 20 , y * 40     ],
                                        [x * 40 + 40 , y * 40 + 20],
                                        [x * 40 + 20 , y * 40 + 40],
                                        [x * 40      , y * 40 + 20], ])

def draw_rect(screen, position, color, size = 40):
    y, x = position
    pygame.draw.rect(screen, color, (x * 40 + (40 - size)//2, y * 40 + (40 - size)//2, size, size))

def draw_ellipse(screen, position, color, size = 40):
    y, x = position
    pygame.draw.ellipse(screen, color, (x * 40 + (40 - size)//2, y * 40 + (40 - size)//2, size, size))


#pygame.init()
#screen = pygame.display.set_mode((15 * 40, 10 * 40))
##
#running = True
#while running:
#    for event in pygame.event.get():
#        if event.type == QUIT:
#            running = False
#    position = (1,3)
#    y, x = position
#    screen.fill(GRAY)
#    pygame.draw.rect(screen, RED, (14 * 40, 2 * 40, 40, 40))
#    draw_rect(screen, (3,14), GREEN)
#    #draw_rect(screen, (4,14), GREEN, 24)
#    draw_ellipse(screen, (4,14), GREEN, 24)
#    pygame.display.flip()
#
#pygame.quit()

