import time
import pygame
import threading
import multiprocessing
class Simulator():
    '''
    Clase generica de un Simulador por pasos de tiempo
    '''

    def __init__(self, ClassEnvironment) -> None:
        self.class_enviroment = ClassEnvironment

    def StartSimulation(self, stop_steps, reset= True, *args, **kvargs):
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
        if reset:
            environment.reset()
        return environment, outputs

    def StartManySimulations(self, count_simulations, stop_steps, reset= True, *args, **kvargs):
        simulations = []
        for _ in range(count_simulations):
            outputs = self.StartSimulation(stop_steps, reset, *args, **kvargs)            
            simulations.append(outputs[1])
        return simulations

    def ThreadSimulations(self, conn, count_simulations, stop_steps, *args, **kvargs):
        results = self.StartManySimulations(count_simulations, stop_steps, reset=False, *args, **kvargs)
        conn.send(results)

    def StartManySimulationsThreading(self, stop_steps, *args, **kvargs):
        simulations1 = []
        simulations2 = []
        simulations3 = []
        simulations4 = []


        parent_conn1, child_conn1 = multiprocessing.Pipe()
        thread1 = multiprocessing.Process(
            target= self.ThreadSimulations,
            args=(child_conn1, 8, stop_steps, *args),
            kwargs=kvargs, daemon= True)

        parent_conn2, child_conn2 = multiprocessing.Pipe()
        thread2 = multiprocessing.Process(
            target= self.ThreadSimulations,
            args=(child_conn2, 8, stop_steps, *args),
            kwargs=kvargs, daemon= True)

        parent_conn3, child_conn3 = multiprocessing.Pipe()
        thread3 = multiprocessing.Process(
            target= self.ThreadSimulations,
            args=(child_conn3, 7, stop_steps, *args),
            kwargs=kvargs, daemon= True)   

        parent_conn4, child_conn4 = multiprocessing.Pipe()
        thread4 = multiprocessing.Process(
            target= self.ThreadSimulations,
            args=(child_conn4, 7, stop_steps, *args),
            kwargs=kvargs, daemon= True)       

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        simulations1 = parent_conn1.recv()
        simulations2 = parent_conn2.recv()
        simulations3 = parent_conn3.recv()
        simulations4 = parent_conn4.recv()

        thread1.join()
        thread2.join()
        thread3.join()        
        thread4.join()

        return simulations1 + simulations2 + simulations3 + simulations4

class Simulator2D(Simulator):

    def __init__(self, ClassEnvironment) -> None:
        super().__init__(ClassEnvironment)

    def StartSimulation(self, tick, stop_steps, *args, **kvargs):
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
        pygame.init()
        h, w = environment.shape_map
        screen = pygame.display.set_mode((w * 40, h * 40))
        pygame.display.flip()
        while step < stop_steps:
            time.sleep(tick)
            environment.next_step()
            output = environment.outputs()
            outputs.append(output)
            self.draw(environment, screen)
            print(step, output)
            step += 1
        return environment, outputs

    def draw(self, environment, screen):
        raise NotImplementedError()



        


