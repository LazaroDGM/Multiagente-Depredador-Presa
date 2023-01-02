class Obstacle(object):
    '''
    Entidad que modela un Obstaculo. Es una clase Singleton para evitar el 
    abuso innecesario de memoria
    '''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Obstacle, cls).__new__(cls)            
        return cls.instance

    def __repr__(self) -> str:
        return 'o'

class Food(object):
    '''
    Entidad que modela la comida. Es una clase Singleton para evitar el 
    abuso innecesario de memoria
    '''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Food, cls).__new__(cls)            
        return cls.instance

    def __repr__(self) -> str:
        return 'f'

class Plant(object):
    '''
    Entidad que modela una Planta. Es una clase Singleton para evitar el 
    abuso innecesario de memoria
    '''
    def __init__(self) -> None:
        pass

class Burrow():

    def __init__(self) -> None:
        self.agent = None

    def isEmpty(self):
        return self.agent is None

    def Add(self, agent):
        if not self.isEmpty():
            raise Exception('Annadiendo agente en una madriguera ocupada')
        self.agent = agent

    def Remove(self):
        if self.isEmpty():
            raise Exception('Eliminando agente de una madriguera vacia')
        agent = self.agent
        self.agent = None
        return agent

class Floor(object):

    def __init__(self) -> None:
        self.food = None
        self.prey = None
        self.predator = None

    def isEmpty(self):
        return self.food is None and self.prey is None and self.predator is None

    def hasAgent(self):
        return self.prey is not None or self.predator is not None

    def hasPrey(self):
        return self.prey is not None

    def hasPredator(self):
        return self.predator is not None
    
    def hasFood(self):
        return self.food is not None

    def AddFood(self):
        if self.hasFood():
            raise Exception('Annadiendo comida en suelo con comida')
        self.food = Food()

    def AddPrey(self, prey):
        if self.hasPrey():
            raise Exception('Annadiendo una presa en suelo con presa')
        self.prey = prey

    def AddPredator(self, predator):
        if self.hasPredator():
            raise Exception('Anndiendo un depredador a una casilla con depredador')
        self.predator = predator

    def RemoveFood(self):
        if not self.hasFood():
            raise Exception('Eliminando comida de un suelo sin comida')
        self.food = None

    def RemovePrey(self):
        if not self.hasPrey():
            raise Exception('Eliminando presa de un suelo sin presa')
        agent = self.prey
        self.prey = None
        return agent

    def RemovePredator(self):
        if not self.hasPredator():
            raise Exception('Eliminando depredador de un suelo sin depredador')
        agent = self.predator
        self.predator = None
        return agent