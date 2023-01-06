from simulators.simulator_03.environment import Environment03, Food, Obstacle, Plant, Burrow, Floor
from simulator.simulator import Simulator2D, Simulator
import drawing.util as draw
import pygame

class Simulator03_2D(Simulator2D):
    def __init__(self, ClassEnvironment) -> None:
        super().__init__(ClassEnvironment)

    def draw(self, environment, screen):            

        screen.fill(draw.LIGHTSALMON)
        for i in range(environment.shape_map[0]):
            for j in range(environment.shape_map[1]):
                obj = environment._map[i][j]
                if isinstance(obj, Obstacle):
                    draw.draw_diamond(screen, (i,j), draw.BLACK)
                elif isinstance(obj, Plant):
                    draw.draw_ellipse(screen, (i,j), draw.GREEN, 40)
                elif isinstance(obj, Burrow):
                    draw.draw_rect(screen, (i,j), draw.MEDIUMORCHID, 40)
                    if not obj.isEmpty():
                        draw.draw_rect(screen, (i,j), draw.BLUE, 20)
                elif isinstance(obj, Floor):
                    if obj.hasPredator():
                        draw.draw_rect(screen, (i,j), draw.RED, 36)
                    if obj.hasPrey():
                        draw.draw_rect(screen, (i,j), draw.BLUE, 30)
                    if obj.hasFood():
                        draw.draw_ellipse(screen, (i,j), draw.YELLOW, 20)
                else:
                    raise Exception('Error al pintar. Casilla Invalida')
        pygame.display.flip()

class Simulator03(Simulator):
    def __init__(self) -> None:
        super().__init__(Environment03)

    def StartManySimulations(self, count_simulations, stop_steps, reset= True, *args, **kvargs):
        simulations = []
        for _ in range(count_simulations):
            outputs = self.StartSimulation(stop_steps, reset, *args, **kvargs)            
            env = outputs[0]
            env : Environment03
            simulations.append((outputs[1], env.life_preys, env.life_predators, env.heatmap_preys, env.heatmap_predators))
        return simulations