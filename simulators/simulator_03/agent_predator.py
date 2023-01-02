from simulator.agent import ProactiveAgent
import numpy as np
import random

################################################################
###################### PREDATOR ################################
################################################################

######################### PARAMS ###############################
class ParamsPredator():
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
class PredatorAgentPropierties:
    '''
    Clase contenedora de parametros de una Presa. Es una clase singleton y
    la contienen como propiedad todas las presas creadas
    '''
    def __new__(cls, params: ParamsPredator, map):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PredatorAgentPropierties, cls).__new__(cls)
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
class PredatorAgent(ProactiveAgent):
    '''
    Clase para modelar una presa. Contiene las propiedades locales de la presa y las globales
    '''
    def __init__(self, propierties: PredatorAgentPropierties) -> None:
        super().__init__()
        self.prop = propierties

        self.energy = self.prop.max_energy
        self.eating = 0
    
    def set_global_map(self, map):
        self._map = np.copy(map)
