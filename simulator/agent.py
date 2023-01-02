class Agent():
    '''
    Clase Abstracta de un Agente Estandar. Este agente solo ejecuta
    acciones dado un conjunto de percepciones
    '''

    def action(self, P):
        '''
        Dada las percepciones del medio, el agente decide que accion realizar

        `P`: Conjunto de percepciones recibidas

        `return`: Accion que el agente quiere realizar
        '''
        raise NotImplementedError()

class StateAgent(Agent):
    '''
    Una clase abstracta de Agentes de Estado. Este tiene estados internos y antes de generar
    una accion, cambia sus estados internos, basado en las percepciones que reciba.
    '''

    def next(self, P):        
        '''
        Dada las percepciones del medio, el agente hace cambios en sus estados internos

        `P`: Conjunto de percepciones recibidas

        `return`: None
        '''
        raise NotImplementedError()

    def action(self):
        '''
        Segun los estados internos, el agente decide que accion realizar. Puede modificar los estados internos

        `return`: Accion que el agente quiere realizar
        '''
        raise NotImplementedError()

class BrooksAgent(StateAgent):

    def __init__(self) -> None:
        self.behaviors = []

    def action(self, P):
        for condition, rule_action in self.behaviors:
            if condition(self, P):
                return rule_action(self, P)
        return None
    

class ProactiveAgent(Agent):

    def __init__(self) -> None:
        super().__init__()

    def brf(self, P):
        '''
        Dada la percepcion actual, y disponiendo de las creencias actuales
        se formulan nuevas creencias
        '''
        raise NotImplementedError()

    def options(self, P):
        '''
        Dada la percepcion actual, y disponiendo de las creencias e intenciones
        actuales, se formulan nuevos deseos
        '''
        raise NotImplementedError()

    def filter(self, P):
        '''
        Dada la percepcion actual y disponiendo de las creencias, deseos e intenciones actuales,
        se formulan nuevos intenciones y se ejecuta la accion
        '''
        raise NotImplementedError()

    def action(self, P):        
        self.brf(P)
        self.options(P)
        Ac = self.filter(P)
        return Ac
