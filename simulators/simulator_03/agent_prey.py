from simulator.agent import ProactiveAgent
import numpy as np
import random

BURROW = 'BURROW'
FLOOR = None

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
        ) -> None:
        self.digestion_time = digestion_time
        self.max_energy = max_energy
        self.velocity = velocity
        self.vision_radius = vision_radius
        self.lost_energy_wait = lost_energy_wait,
        self.lost_energy_walk = lost_energy_walk,
        self.lost_energy_wait_burrow = lost_energy_wait_burrow,
        self.lost_energy_walk_burrow = lost_energy_walk_burrow,

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

        self.energy = self.prop.max_energy
        self.eating = 0
        self.wait_move = 1
    
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
        self.eating =  self.prop.digestion_time
        return ActionPrey(new_position= P.position, eat= True)

    def __wait_eat(self, P: PerceptionPrey):
        self.eating -= 1
        return ActionPrey(new_position= P.position, eat= False)

    