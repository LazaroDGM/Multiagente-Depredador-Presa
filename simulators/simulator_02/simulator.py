from simulator.simulator import Simulator2D
from simulators.simulator_02.agent import PredatorAgent, scaredPreyAgent
import drawing.util as draw
import pygame
from simulator.entities import Obstacle, Food

class Simulator02(Simulator2D):
    def __init__(self, ClassEnvironment) -> None:
        super().__init__(ClassEnvironment)

    def draw(self, environment, screen):            

        screen.fill(draw.GRAY)
        for i in range(environment.shape_map[0]):
            for j in range(environment.shape_map[1]):
                for item in environment._map[i][j]:
                    #if isinstance(item, Agent):
                    #    pygame.draw.rect(screen, RED, (j * 40, i * 40, 40, 40))
                    if isinstance(item, Food):
                        draw.draw_ellipse(screen, (i,j), draw.YELLOW, 20)
                    if isinstance(item, Obstacle):
                        draw.draw_diamond(screen, (i,j), draw.BLACK)
        for r, c in environment.agents_groups[0].values():
            draw.draw_rect(screen, (r, c), draw.RED, 38)
        for r, c in environment.agents_groups[1].values():
            draw.draw_rect(screen, (r, c), draw.BLUE, 30)
            
        pygame.display.flip()


