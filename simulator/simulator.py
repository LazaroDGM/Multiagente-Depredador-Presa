class Simulator():
    '''
    Clase generica de un Simulador por pasos de tiempo
    '''

    def __init__(self, ClassEnvironment) -> None:
        self.class_enviroment = ClassEnvironment

    def StartSimulation(self, stop_steps, *args, **kvargs):
        '''
        Funcion que comienza la simulacion y genera un conjunto de salidas
        que son las variables observables.

        `stop_steps`: Minima cantidad de unidades de tiempo que deben ocurrir en la simulacion
        para que esta finalice.

        `*args`: Parametros posicionales de entrada del Medio
        `**kvargs`: Parametros llave-valor de entrada del Medio

        `return`: Tupla de 2 elementos, donde:
            `return[0]`: La instancia del medio ambiente actual
            `return[1]`: El conjunto de variables observables
        '''
        environment = self.class_enviroment(*args, **kvargs)
        outputs = []
        step = 0
        while step < stop_steps:
            environment.next_step()
            outputs.append(environment.outputs())
            step += 1
        return environment, outputs

    def StartManySimulations(self, count_simulations, stop_steps, *args, **kvargs):
        simulations = []
        for _ in range(count_simulations):
            outputs = self.StartSimulation(stop_steps, *args, **kvargs)            
            simulations.append(outputs)
        return simulations

    



        

