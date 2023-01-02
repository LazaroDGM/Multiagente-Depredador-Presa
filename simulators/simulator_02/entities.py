class HidePlace(object):
    '''
    Entidad que modela los escondites de las presas. Es una clase Singleton
    para evitar el abuso innecesario de memoria
    '''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HidePlace, cls).__new__(cls)
        return cls.instance

    def __repr__(self) -> str:
        return 'f'