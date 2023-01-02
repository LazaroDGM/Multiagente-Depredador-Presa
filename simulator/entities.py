class Food(object):
    '''
    Entidad que modela la Comida. Es una clase Singleton para evitar el 
    abuso innecesario de memoria
    '''
    def __new__(cls, energy_ratio = 1.0):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Food, cls).__new__(cls)
            cls.energy_ratio = energy_ratio
        return cls.instance

    @classmethod
    def delete(cls):
        if hasattr(cls, 'instance'):
            delattr(cls, 'instance')
            cls.energy_ratio = 0

    def __repr__(self) -> str:
        return 'f'

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