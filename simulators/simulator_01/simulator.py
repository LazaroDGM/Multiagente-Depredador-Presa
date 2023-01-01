from simulator.simulator import Simulator2D
import pygame
from pygame.locals import *
from simulator.agent import Agent
from simulators.simulator_01.entities import Food

RED = (255, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 0, 255)

class Simulator01(Simulator2D):
    def __init__(self, ClassEnvironment) -> None:
        super().__init__(ClassEnvironment)

    def draw(self, environment, screen):
        map = environment._map
        SIZE = environment.shape_map

        screen.fill(GRAY)
        for r, c in environment.agents.values():
            pygame.draw.rect(screen, RED, (c * 40, r * 40, 40, 40))
        for i in range(environment.shape_map[0]):
            for j in range(environment.shape_map[1]):

                for item in environment._map[i][j]:
                    #if isinstance(item, Agent):
                    #    pygame.draw.rect(screen, RED, (j * 40, i * 40, 40, 40))
                    if isinstance(item, Food):
                        pygame.draw.ellipse(screen, GREEN, (j * 40, i * 40, 40, 40))
        pygame.display.flip()


