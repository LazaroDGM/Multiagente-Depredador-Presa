from simulator.agent import ProactiveAgent
from simulators.simulator_03.memory import PreyMemory, PredatorMemory, FoodMemory
from simulators.simulator_03.entities import Plant, Obstacle
import Algorithms.util as util
import numpy as np
import random

BURROW = 'BURROW'
FLOOR = None

EAT = 'EAT'
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
        self.lost_energy_wait = lost_energy_wait,
        self.lost_energy_walk = lost_energy_walk,
        self.lost_energy_wait_burrow = lost_energy_wait_burrow,
        self.lost_energy_walk_burrow = lost_energy_walk_burrow,
        self.memory_prey_wait_time = memory_prey_wait_time,
        self.memory_predator_wait_time = memory_predator_wait_time,
        self.forget_tick = forget_tick
        self.weight_memory_food = weight_memory_food,
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
            cls.lost_energy_wait = params.lost_energy_wait,
            cls.lost_energy_walk = params.lost_energy_walk,
            cls.lost_energy_wait_burrow = params.lost_energy_wait_burrow,
            cls.lost_energy_walk_burrow = params.lost_energy_walk_burrow,
            cls.memory_prey_wait_time = params.memory_prey_wait_time,
            cls.memory_predator_wait_time = params.memory_predator_wait_time,
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

        # Objetives
        self.current_path = []
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
        ratio_food = count_food / ((self.prop.vision_radius * 2 + 1) ** 2)
        self.food_memory.Remember(P.position, ratio_food)

        # Actualizando avance del Camino Actual
        if self.current_path is not None:
            if P.position != self.current_path[0]:                
                self.current_path.pop(0)
                if len(self.current_path) > 0:
                    if self.current_path[0] != P.position:
                        raise Exception('Se hizo un movimiento fuera del camino actual')

    ##################### OPTIONS #############################

    def options(self, P):
        raise NotImplementedError()

    ##################### FILTER ##############################

    def filter(self, P):

        # Acciones que siempre se deben hacer en condiciones determinadas
        if self.wait_move > 0:
            Ac = self.__wait_move(P)
            return Ac
        if self.eating > 0:
            Ac = self.__wait_eat(P)
            return Ac

        # Acciones que dependen de varios factores probabilisticos
        # TODO
        raise NotImplementedError()

    #################### INTENTIONS ###########################

    def intention_walk_to(self, P : PerceptionPrey):
                
        if self.current_path is None or len(self.current_path) == 0:
            raise Exception('Intencion de moverse, sin camino')        

        
        if P.close_preys.get(self.current_path[1], None) is not None:
            if len(self.current_path) > 1:
                future_position = self.current_path[1]
            future_position = self.current_path[0]
            
            extract = util.extract_radius_matrix(self.prop.map, P.position, 1)
            adjacents = util.adjacent_box(extract, future_position,
                isValid= lambda box: not (isinstance(box, Plant) or isinstance(box, Obstacle)))
            adjacents.append(future_position)
            counts = [1]* len(adjacents)
            counts[-1] += (len(adjacents) - 1) * 9
            new_position = self.prop.rand.sample(adjacents, k= 1, counts= counts)[0]
            self.current_path[1] = new_position
        else:
            new_position = self.current_path[0]
        return self.__mov(P, new_position)

    def intention_scape(self, P: PerceptionPrey):
        
        raise NotImplementedError()
        