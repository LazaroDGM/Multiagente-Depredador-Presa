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