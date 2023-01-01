from simulators.simulator_03.environment import Environment03, Food, Obstacle, Plant
from simulator.simulator import Simulator2D
import drawing.util as draw
import pygame

class Simulator02(Simulator2D):
    def __init__(self, ClassEnvironment) -> None:
        super().__init__(ClassEnvironment)

    def draw(self, environment, screen):            

        screen.fill(draw.GRAY)
        for i in range(environment.shape_map[0]):
            for j in range(environment.shape_map[1]):
                if isinstance(environment._map[i][j], Obstacle):
                    draw.draw_diamond(screen, (i,j), draw.BLACK)
                elif isinstance(environment._map[i][j], Plant):
                    draw.draw_ellipse(screen, (i,j), draw.GREEN, 40)
                else:
                    for item in environment._map[i][j]:
                        if isinstance(item, Food):
                            draw.draw_ellipse(screen, (i,j), draw.YELLOW, 20)
        pygame.display.flip()