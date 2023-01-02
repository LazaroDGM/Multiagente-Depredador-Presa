from simulator.agent import ProactiveAgent
import numpy as np
import random

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
        ) -> None:
        self.digestion_time = digestion_time
        self.max_energy = max_energy
        self.velocity = velocity
        self.vision_radius = vision_radius

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
    
    def set_global_map(self, map):
        self._map = np.copy(map)
