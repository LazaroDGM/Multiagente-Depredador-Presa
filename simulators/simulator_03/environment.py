from simulator.environment import Environment
from simulators.simulator_03.entities import Food, Obstacle, Plant, Burrow, Floor
from simulators.simulator_03.agent_prey import ParamsPrey, PreyAgentPropierties, PerceptionPrey, PreyAgent
from simulators.simulator_03.agent_predator import ParamsPredator, PredatorAgentPropierties, PerceptionPredator, PredatorAgent
import numpy as np
import random

VOID = 0
FOOD = 1
OBSTACLE = -1
HIDING_PLACE = -2

class Environment03(Environment):

    def __init__(self,
        map,
        plant_radius,
        food_ratio,
        food_generation_period,
        initial_count_prey,
        initial_count_predator,
        params_prey : ParamsPrey,
        params_predator : ParamsPredator,
    ) -> None:
        self.plant_radius = plant_radius
        self.food_ratio = food_ratio
        self.food_generation_period = food_generation_period
        self.initial_count_prey = initial_count_prey
        self.initial_count_predator = initial_count_predator
        self.prop_prey = PreyAgentPropierties(params_prey, map)
        self.prop_predator = PredatorAgentPropierties(params_predator, map)
        
        self._see_functions = {
            PreyAgent: self.seePrey,
            PredatorAgent: self.seePredator
        }


        self.food = Food()
        self.obstacle = Obstacle()
        self._rand = random.Random()

        # Diccionario de plantas-(posicion, proxima reproduccion)
        self.plants = {}

        # Diccionario de presas-posicion
        self.preys = {}

        # Diccionario de depredadores-posicion
        self.predators = {}

        # Variables contadoras
        self.cicle = 0 # Tiempo actual del Medio
        self.count_foods = 0
        
        self._init_map(map)

    
    def _init_map(self, map):
        row, col =  map.shape
        self._map = np.array([set() for i in range(0, row*col)])
        self._map.resize((row, col))
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                if isinstance(map[i,j], (Obstacle, Plant)):
                    self._map[i][j] = map[i,j]
                    if isinstance(map[i][j], Plant):
                        self.plants[(i,j)] = 1
                elif map[i][j] == 'BURROW':
                    self._map[i][j] = Burrow()
                elif map[i][j] is None:
                    self._map[i][j] = Floor()
        self.shape_map = self._map.shape

        count_preys = self.initial_count_prey
        while count_preys > 0:
            new_pos = (random.randint(0, self.shape_map[0] - 1), random.randint(0, self.shape_map[1] - 1))
            box = self._map[new_pos[0]][new_pos[1]]
            if box != Obstacle() and \
                box != Plant() and \
                isinstance(box, (Floor, Burrow)) and \
                not box.hasPrey():
                prey = PreyAgent(self.prop_prey)
                box.AddPrey(prey)
                self.preys[prey] = new_pos
                count_preys -= 1
        
        count_predators = self.initial_count_predator
        while count_predators > 0:
            new_pos = (random.randint(0, self.shape_map[0] - 1), random.randint(0, self.shape_map[1] - 1))
            box = self._map[new_pos[0]][new_pos[1]]
            if box != Obstacle() and \
                box != Plant() and \
                isinstance(box, (Floor)) and \
                not box.hasPrey() and \
                not box.hasPredator():
                predator = PredatorAgent(self.prop_predator)
                box.AddPrey(predator)
                self.preys[prey] = new_pos
                count_predators -= 1

    
    def free_for_food(self, s):
        '''
        Funcion para saber si una casilla esta libre para generar una comida
        '''
        if isinstance(s, Floor):
            return not s.hasFood()
        return False

    def _gen_food(self, count, matrix):
        '''
        Genera aleatoriamente uniforme, en lugares sin obstaculos, comida.
        La cantidad de comida generada es en proporcion al mapa.
        '''
        reshaped = matrix.reshape(matrix.size)
        #food = Food()

        emptys = np.array(list(filter(self.free_for_food, reshaped)))
        emptys.resize(emptys.size)
        #selection = self._rand.sample(emptys,k = min(, emptys.size))

        # int(self.food_ratio * self.shape_map[0]*self.shape_map[1])
        idx = np.random.choice(emptys.shape[0], min(count, emptys.size), replace=False)
        selection = emptys[idx]
        for s in selection:            
            s.AddFood()
        self.count_foods += len(selection)

    def gen_food(self):
        # Generacion de Comida
        for (r, c), cicle_food in self.plants.items():
            if self.cicle == cicle_food:
                #self._remove_food()                
                min_r = max(0, r-self.plant_radius)
                min_c = max(0, c-self.plant_radius)
                max_r = min(self._map.shape[0], r+self.plant_radius+1)
                max_c = min(self._map.shape[1], c+self.plant_radius+1)
                extract = self._map[min_r:max_r, min_c:max_c]

                self._gen_food(int(self.food_ratio*extract.size), extract)
                cicle_food = int(self._rand.expovariate(1/self.food_generation_period)) + self.cicle + 1
                #print('Nueva produccion de comida en: ', cicle_food)
                self.plants[(r,c)] = cicle_food

    def seePrey(self, prey):
        r, c = self.preys[prey]
        min_r = max(0, r-self.prop_prey.vision_radius)
        min_c = max(0, c-self.prop_prey.vision_radius)
        max_r = min(self._map.shape[0], r+self.prop_prey.vision_radius+1)
        max_c = min(self._map.shape[1], c+self.prop_prey.vision_radius+1)        

        close_preys = {}
        close_predators = {}
        close_food = []
        
        for i in range(min_r, max_r):
            for j in range(min_c, max_c):
                box = self._map[i][j]
                if isinstance(box, Floor):
                    if box.hasPrey():
                        close_preys[(i,j)] = box.prey
                    if box.hasPredator():
                        close_predators[(i,j)] = box.predator
                    if box.hasFood():
                        close_food.append((i,j))
                elif isinstance(box, Burrow):
                    if box.hasPrey():
                        close_preys[(i,j)] = box.prey
        return PerceptionPrey(
            position=(r,c),
            close_preys= close_preys,
            close_predators= close_predators,
            close_food= close_food
        )
    
    def seePredator(self, predator):
        r, c = self.preys[predator]
        min_r = max(0, r-self.prop_prey.vision_radius)
        min_c = max(0, c-self.prop_prey.vision_radius)
        max_r = min(self._map.shape[0], r+self.prop_prey.vision_radius+1)
        max_c = min(self._map.shape[1], c+self.prop_prey.vision_radius+1)        

        close_preys = {}
        close_predators = {}
        close_food = {}
        
        for i in range(range(min_r, max_r)):
            for j in range(min_c, max_c):
                box = self._map[i][j]
                if isinstance(box, Floor):
                    if box.hasPrey():
                        close_preys[(i,j)] = box.prey
                    if box.hasPredator():
                        close_predators[(i,j)] = box.predator
                    if box.hasFood():
                        close_food[(i,j)] = box.food
        
        return PerceptionPredator(
            position= (r,c),
            close_preys= close_preys,
            close_food= close_food
        )

    def remove_dead_agents(self):
        delete_preys = []
        for prey, (i, j) in self.preys.items():
            prey : PreyAgent
            if prey.energy <= 0:
                delete_preys.append(prey)
                box = self._map[i][j]
                if isinstance(box, (Burrow, Floor)):
                    if not box.hasPrey():
                        raise Exception('Presa lista para morir, no esta en la casilla')
                    box.RemovePrey()
                else:
                    raise Exception('Presa lista para morirse, que no esta en ningun lugar')
        for prey in delete_preys:
            self.preys.pop(prey)
        del(delete_preys)

        delete_predators = []
        for predator, (i, j) in self.predators.items():
            predator : PredatorAgent
            if predator.energy <= 0:
                delete_predators.append(predator)
                box = self._map[i][j]
                if isinstance(box, Floor):
                    if not box.hasPredator():
                        raise Exception('Depredador lista para morir, no esta en la casilla')
                    box.RemovePredator()
                else:
                    raise Exception('Predator lista para morirse, que no esta en ningun lugar')
        for predator in delete_predators:
            self.predators.pop(predator)
        del(delete_predators)
    
    def gen_preys(self, actions_preys):        
        for prey, action in actions_preys:            
            if action.reproduce:                
                r, c = self.preys[prey]
                min_r = max(0, r-1)
                min_c = max(0, c-1)
                max_r = min(self._map.shape[0], r+1+1)
                max_c = min(self._map.shape[1], c+1+1) 
                emptys = []
                for i in range(min_r, max_r):
                    for j in range(min_c, max_c):
                        box= self._map[i][j]
                        if box == Plant() or box == Obstacle():
                            continue
                        if box.hasPrey():
                            continue
                        emptys.append((i,j))
                news_positions = self._rand.sample(emptys, min(len(emptys), 1))
                for position in news_positions:
                    prey = PreyAgent(self.prop_prey)
                    self._map[position[0]][position[1]].AddPrey(prey)
                    self.preys[prey] = position                


    def transform(self, actions_predators, actions_preys):
        
        self.gen_preys(actions_preys)

        delete_prey = []
        new_positions_predators = {}
        for predator, action in actions_predators:
            new_position = action.new_position
            eat = action.eat
            new_r, new_c = new_position
            old_r, old_c = old_position = self.predators[predator]
            box = self._map[old_r][old_c]
            if not (isinstance(box, Floor) and box.predator == predator):
                raise Exception('Depredador en mapa, no coincide con el depredador actual')
            if abs(new_r - old_r) > 1 or abs(new_c - old_c) > 1:
                raise Exception('Movimiento errado del depredador')
            
            if eat == True:
                if new_position != old_position:
                    raise Exception('Depredador que se mueve y come a la vez')
                if not box.hasPrey():
                    raise Exception('Depredador comiendo en una casilla sin Presa')
                prey = box.RemovePrey()
                delete_prey.append(prey)
                new_positions_predators[new_position] = predator
            elif new_position == old_position:
                new_positions_predators[new_position] = predator
            elif new_positions_predators.get(new_position, None) is None and \
                    self._map[new_position[0]][new_position[1]].hasPredator():
                new_positions_predators[new_position] = predator

        for new_position, predator in new_positions_predators.items():
            if new_position != self.predators[predator]:
                old_r, old_c = self.predators[predator]
                self._map[old_r][old_c].RemovePredator()
        for (new_r, new_c), predator in new_positions_predators.items():
            if (new_r, new_c) != self.predators[predator]:              
                self._map[new_r][new_c].AddPredator(predator)
                self.predators[predator] = (new_r, new_c)

        new_positions_preys = {}
        for prey, action in actions_preys:
            new_position = action.new_position
            eat = action.eat
            if prey in delete_prey:
                self.preys.pop(prey)
                continue

            new_r, new_c = new_position
            old_r, old_c = old_position = self.preys[prey]
            box = self._map[old_r][old_c]
            if not isinstance(box, (Floor, Burrow)):
                raise Exception('La presa no esta ni en el suelo ni en la madriguera')
            if not box.prey == prey:
                raise Exception('Presa en mapa, no coincide con la presa actual')
            if abs(new_r - old_r) > 1 or abs(new_c - old_c) > 1:
                raise Exception('Movimiento errado de la presa')
            if eat == True:
                if new_position != old_position:
                    raise Exception('Presa que se mueve y come a la vez')
                if not box.hasFood():
                    raise Exception('Presa comiendo en una casilla sin Comida')
                box.RemoveFood() 
                self.count_foods -=1               
                new_positions_preys[new_position] = prey
            elif new_position == old_position:
                new_positions_preys[new_position] = prey
            elif new_positions_preys.get(new_position, None) is None and \
                    not self._map[new_position[0]][new_position[1]].hasPrey():
                new_positions_preys[new_position] = prey

        for new_position, prey in new_positions_preys.items():
            if new_position != self.preys[prey]:
                old_r, old_c = self.preys[prey]
                self._map[old_r][old_c].RemovePrey()
        for (new_r, new_c), prey in new_positions_preys.items():
            if (new_r, new_c) != self.preys[prey]:              
                self._map[new_r][new_c].AddPrey(prey)
                self.preys[prey] = (new_r, new_c)  
                
        del(new_positions_preys)
        del(new_positions_predators)
        del(delete_prey)
            


    def next_step(self):
        self.cicle += 1
        self.remove_dead_agents()        
        self.gen_food()        

        actions_predators = []
        for predator in self.predators.keys():            
            P = self.see(predator)
            action = predator.action(P)
            actions_predators.append((predator, action))

        actions_preys = []
        for prey in self.preys.keys():  
            P = self.see(prey)
            action = prey.action(P)
            actions_preys.append((prey, action))

        self.transform(actions_predators=actions_predators, actions_preys=actions_preys)


    def outputs(self):
        return len(self.preys), self.count_foods

    def reset(self):
        self.prop_prey.delete()
        self.prop_predator.delete()        