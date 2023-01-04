from importlib.resources import path
from turtle import position
from simulator.agent import ProactiveAgent
from simulators.simulator_03.memory import PreyMemory, PredatorMemory, FoodMemory
from simulators.simulator_03.entities import Plant, Obstacle
import Algorithms.util as util
from Algorithms.AStarPlus import AStarPlus
from Algorithms.transform import transform, betterMove
import numpy as np
import random
import math

BURROW = 'BURROW'
FLOOR = None

EAT = 'EAT'
GO_EAT= 'GO_EAT'
FIND_EAT = 'FIND EAT'
GESTATE = 'GESTATE'
ESCAPE = 'ESCAPE'
NOTHING = 'NOTHING'
WAIT = 'WAIT'

################################################################
######################### PREY #################################
################################################################

####################### PERCEPTION #############################

class PerceptionPrey():
    def __init__(self,
        position,
        close_preys,
        close_predators,
        close_food
        ) -> None:
        self.position = position
        self.close_preys = close_preys
        self.close_predators = close_predators
        self.close_food = close_food

########################## ACTION ##############################

class ActionPrey():
    def __init__(self,
        new_position,
        eat = False,
        die = False
        ) -> None:

        self.new_position = new_position
        self.eat = eat
        self.die = die
        

######################### PARAMS ###############################
class ParamsPrey():
    '''
    Clase contenedora de parametros de una Presa. Se debe utilizar como
    parametro para la inicializar una instancia de Presa
    '''
    def __init__(self,
            digestion_time,
            max_energy,
            velocity,
            vision_radius,
            lost_energy_wait,
            lost_energy_walk,
            lost_energy_wait_burrow,
            lost_energy_walk_burrow,
            memory_prey_wait_time,
            memory_predator_wait_time,
            forget_tick,
            weight_memory_food,
            breeding_point,
            food_energy_ratio
        ) -> None:
        self.digestion_time = digestion_time
        self.max_energy = max_energy
        self.velocity = velocity
        self.vision_radius = vision_radius
        self.lost_energy_wait = lost_energy_wait
        self.lost_energy_walk = lost_energy_walk
        self.lost_energy_wait_burrow = lost_energy_wait_burrow
        self.lost_energy_walk_burrow = lost_energy_walk_burrow
        self.memory_prey_wait_time = memory_prey_wait_time
        self.memory_predator_wait_time = memory_predator_wait_time
        self.forget_tick = forget_tick
        self.weight_memory_food = weight_memory_food
        self.breeding_point = breeding_point
        self.food_energy_ratio = food_energy_ratio


###################### PROPIERTIES #################################
class PreyAgentPropierties:
    '''
    Clase contenedora de parametros de una Presa. Es una clase singleton y
    la contienen como propiedad todas las presas creadas
    '''
    def __new__(cls, params: ParamsPrey, map):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PreyAgentPropierties, cls).__new__(cls)
            cls.digestion_time = params.digestion_time
            cls.max_energy = params.max_energy
            cls.velocity = params.velocity
            cls.vision_radius = params.vision_radius
            cls.map = np.copy(map)
            cls.lost_energy_wait = params.lost_energy_wait
            cls.lost_energy_walk = params.lost_energy_walk
            cls.lost_energy_wait_burrow = params.lost_energy_wait_burrow
            cls.lost_energy_walk_burrow = params.lost_energy_walk_burrow
            cls.memory_prey_wait_time = params.memory_prey_wait_time
            cls.memory_predator_wait_time = params.memory_predator_wait_time
            cls.forget_tick = params.forget_tick
            cls.weight_memory_food = params.weight_memory_food
            cls.breeding_point = params.breeding_point
            cls.food_energy_ratio = params.food_energy_ratio
            cls.rand = random.Random()
        return cls.instance
    
    @classmethod
    def delete(cls):
        del(cls.instance)

####################### AGENT PREY #################################
class PreyAgent(ProactiveAgent):
    '''
    Clase para modelar una presa. Contiene las propiedades locales de la presa y las globales
    '''
    def __init__(self, propierties: PreyAgentPropierties) -> None:
        super().__init__()
        self.prop = propierties
        self.food_memory = FoodMemory(weight= self.prop.weight_memory_food, forget_tick= self.prop.forget_tick)
        self.prey_memory = PreyMemory(self.prop.memory_prey_wait_time)
        self.predator_memory = PredatorMemory(self.prop.memory_predator_wait_time)

        self.energy = self.prop.max_energy
        self.eating = 0
        self.wait_move = 1
        self.extra_energy = 0

        # Desires
        self.breeding_desire = 0
        self.hungry_desire = 0
        self.scape_desire = 0

        # Objetives
        self.current_path = None
        self.objetive = NOTHING
    
    def set_global_map(self, map):
        self._map = np.copy(map)
    
    ### ACTIONS ###
    def __mov(self, P : PerceptionPrey, new_position):
        new_r, new_c = new_position
        if P.position == new_position:
            if self.prop.map[new_r][new_c] == FLOOR:
                self.energy -= self.prop.lost_energy_wait
                self.wait_move = self.prop.velocity
            elif self.prop.map[new_r][new_c] == BURROW:
                self.energy -= self.prop.lost_energy_wait_burrow
                self.wait_move = self.prop.velocity
            else:
                raise Exception('Permaneciendo en un lugar invalido')
        else:
            old_r, old_c = P.position
            if self.prop.map[old_r][old_c] == FLOOR:
                self.energy -= self.prop.lost_energy_walk
                self.wait_move = self.prop.velocity
            elif self.prop.map[old_r][old_c] == BURROW:
                self.energy -= self.prop.lost_energy_walk_burrow
                self.wait_move = self.prop.velocity
            else:
                raise Exception('Intentando caminar a un lugar invalido')
        return ActionPrey(new_position= new_position, eat= False)

    def __wait_move(self, P : PerceptionPrey):
        self.wait_move -= 1
        return ActionPrey(new_position= P.position, eat= False)

    def __eat(self, P: PerceptionPrey):
        self.eating = self.prop.digestion_time
        return ActionPrey(new_position= P.position, eat= True)

    def __wait_eat(self, P: PerceptionPrey):
        self.eating -= 1
        if self.eating == 0:
            self.energy += self.prop.food_energy_ratio * self.prop.max_energy
            extra = max(0, self.energy - self.prop.max_energy)
            self.extra_energy += extra
            self.energy -= extra
        return ActionPrey(new_position= P.position, eat= False)

    ################ BRF ###################

    def brf(self, P: PerceptionPrey):

        # Olvidando Presas
        self.prey_memory.Tick()
        # Recordando Presas cercanas        
        for prey in P.close_preys.values():
            self.prey_memory.Remember(prey)

        # Olvidando Depredadores
        self.predator_memory.Tick()
        # Recordando Depredadores cercanos
        for predator in P.close_predators.values():
            self.predator_memory.Remember(predator)

        # Olvidando Comidas
        self.food_memory.Tick()
        # Recordando Posicion donde se veia comida
        count_food = len(P.close_food)
        ratio_food = float(count_food) / ((float(self.prop.vision_radius) * 2.0 + 1.0) ** 2.0)
        self.food_memory.Remember(P.position, ratio_food)

        # Actualizando avance del Camino Actual
        if self.current_path is None or len(self.current_path) == 0:
            #self.objetive == NOTHING
            self.current_path = None
        else:
            if P.position == self.current_path[0]:
                self.current_path.pop(0)
                if len(self.current_path) == 0:
                    self.current_path = None
                    self.objetive = NOTHING

    ##################### OPTIONS #############################

    def options(self, P: PerceptionPrey):
        
        self.hungry_desire = abs(self.prop.rand.normalvariate(0, self.prop.max_energy / 4))
        self.breeding_desire = abs(self.prop.rand.normalvariate(0, (0.8* self.prop.map.size) / 8))
        if len(P.close_predators) > 0:
            self.scape_desire = abs(self.prop.rand.normalvariate(0, 0.02 * self.prop.vision_radius ))
        else:
            self.scape_desire = 0
        
    ##################### FILTER ##############################

    def filter(self, P: PerceptionPrey):

        # Acciones que siempre se deben hacer en condiciones determinadas
        if self.wait_move > 0:
            Ac = self.__wait_move(P)
            return Ac
        if self.eating > 0:
            Ac = self.__wait_eat(P)
            return Ac

        # Acciones que dependen de varios factores probabilisticos
        # TODO

        #~~~ Agente Arriesgado ~~~#
        # if self.breeding_desire > 0.5 and self.hungry_desire < 0.7:
        # if self.scape_desire > 0.5:
        # if self.hungry_desire > 0.5

        #~~~ Agente Precavido ~~~#
        if self.scape_desire < len(P.close_predators):
            return self.intention_scape()
        # Hambriento
        elif self.objetive == EAT:
            if self.energy <= self.prop.max_energy * 0.8:
                self.hungry_desire = math.inf
        if self.objetive in [FIND_EAT, GO_EAT]:            
            if self.objetive == FIND_EAT:
                if P.position in P.close_food and self.energy <= self.prop.max_energy * 0.2:
                    self.objetive = EAT
                    self.current_path = None
                    return self.__eat(P)
                if len(P.close_food) > 0:
                    self.__intention_go_to_eat(P)
                    self.objetive = GO_EAT
                    return self.intention_walk_to(P)
                else:
                    return self.intention_walk_to(P)
            elif self.objetive == GO_EAT:
                if P.position in P.close_food:
                    self.objetive = EAT
                    self.current_path = None
                    return self.__eat(P)
                return self.intention_walk_to(P)
        elif self.hungry_desire >= self.energy:
            if P.position in P.close_food:
                self.objetive = EAT
                self.current_path = None
                return self.__eat(P)
            elif len(P.close_food) > 0:
                self.__intention_go_to_eat(P)
                self.objetive = GO_EAT
                return self.intention_walk_to(P)
            else:
                self.__intention_search_food(P)
                self.objetive = FIND_EAT
                return self.intention_walk_to(P)
        else:
            return self.intention_walk_random(P)
        #elif self.breeding_desire >= len(self.prey_memory):
        #    if self.objetive == GESTATE:


    #################### INTENTIONS ###########################
    def intention_walk_random(self, P: PerceptionPrey):
        r,c = P.position
        min_r = max(0, r-1)
        min_c = max(0, c-1)
        max_r = min(self.prop.map.shape[0], r+1+1)
        max_c = min(self.prop.map.shape[1], c+1+1)

        possibles = [(r,c)]
        for i in range(min_r, max_r):
            for j in range(min_c, max_c):                
                if self.prop.map[i][j] in [Plant(), Obstacle()]:
                    continue
                if P.close_preys.get((i,j), None) is not None:
                    continue
                possibles.append((i,j))
        new_position = self.prop.rand.choice(possibles)
        return self.__mov(P, new_position)
    def intention_walk_to(self, P: PerceptionPrey):
                
        if self.current_path is None or len(self.current_path) == 0:
            raise Exception('Intencion de moverse, sin camino')        

        #if len(self.current_path) > 1 and P.close_preys.get(self.current_path[1], None) is not None:
        #    if len(self.current_path) > 1:
        #        future_position = self.current_path[1]
        #    future_position = self.current_path[0]
        #    
        #    extract = util.extract_radius_matrix(self.prop.map, P.position, 1)
        #    adjacents = util.adjacent_box(extract, future_position,
        #        isValid= lambda box: not (isinstance(box, Plant) or isinstance(box, Obstacle)))
        #    adjacents.append(future_position)
        #    counts = [1]* len(adjacents)
        #    counts[-1] += (len(adjacents) - 1) * 9
        #    new_position = self.prop.rand.sample(adjacents, k= 1, counts= counts)[0]
        #    self.current_path[1] = new_position
        #else:
        #    new_position = self.current_path[0]
        #return self.__mov(P, new_position)
        return self.__mov(P, self.current_path[0])

    def intention_scape(self, P: PerceptionPrey):
        predators_matrix, path = AStarPlus(numpy_array=self.prop.map, x=P.position[0], y=P.position[1], found=lambda x, y: (x, y) in P.close_predators, obstacle=lambda cell: cell is Obstacle() or cell is Plant(), vision=1000000)
        predators_abundance_matrix = transform(predators_matrix, xpansion_distance= 1)
        (x, y) = P.position
        pounded_matrix = [[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 0, 0]] 
        maxi = max(max([array for array in predators_abundance_matrix]))
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        for i, j in positions:
            pounded_matrix[i][j] = maxi - predators_abundance_matrix[i][j] if predators_abundance_matrix[i][j] >= 0 else -1
                
        dx, dy = betterMove(pounded_matrix, rnd=True)

        new_x, new_y = x + dx -1, y + dy -1
        return self.__mov(P, (new_x, new_y))

        
    def __intention_go_to_eat(self, P: PerceptionPrey):
        food_matrix, path = AStarPlus(numpy_array=self.prop.map, x=P.position[0], y=P.position[1], found=lambda x, y: (x, y) in P.close_food, obstacle=lambda cell: cell == Obstacle() or cell == Plant(), vision= 1000000)
        print(path)
        #(x, y) = P.position
        #print(food_matrix)
        #food_abundance_matrix = transform(food_matrix, xpansion_distance=0)
        #(dx, dy) = betterMove(food_abundance_matrix)
        # 
        #sugestion = x + dx -1, y + dy -1
        self.current_path = path
        #return sugestion



    def __intention_search_food(self, P: PerceptionPrey):                
        extra = []
        while len(extra) < 4:
            new_pos = (random.randint(0, self.prop.map.shape[0] - 1), random.randint(0, self.prop.map.shape[1] - 1))
            if self.prop.map[new_pos[0]][new_pos[1]] != Obstacle() and \
                self.prop.map[new_pos[0]][new_pos[1]] != Plant() and \
                P.position != new_pos and \
                new_pos not in extra:
                extra.append(new_pos)

        nearest_memory_food_cell = self.food_memory.suggestion(extra_positions=extra, remove_position=P.position)
        print('Buscando comida', nearest_memory_food_cell)
        food_matrix, path = AStarPlus(numpy_array=self.prop.map, x=P.position[0], y=P.position[1], found=lambda x, y: (x, y) == nearest_memory_food_cell, obstacle=lambda cell: cell == Obstacle() or cell == Plant(), stop_with=1, vision=1000000)
        print(path)        
        self.current_path = path
