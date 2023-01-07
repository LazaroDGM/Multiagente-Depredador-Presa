# Multiagente-Depredador-Presa

En este proyecto se hace una implementaación de un posible modelo Depredador-Presa, usando simulacion en un entorno multiagente. Para ello nos basamos primeramente en el modelo de ecuaciones diferenciales de Lotka-Volterra en el que se consideran solamente dos tipos de animales, cuyas ecuaciones de crecimiento poblacional están dadas por:

$$ p^{\prime} = \alpha p - \beta pd $$

$$ d^{\prime} = \delta pd - \gamma d $$

El modelo se basa en la evolución de las especies y las interacciones entre ellas,  siendo $p$ el número de presas y $d$ el número de depredadores. La interpretación de la primera ecuación es que el crecimiento de la población de presas viene dado proporcionalmente al propio tamaño de esta, y inversamente proporcional a los encuentros con depredadores. Análogamente la segunda ecuación se interpreta como que el crecimiento de los depredadores está dado proporcional a los encuentros con las presas e inversamente proporcional a su propia pobablación (esto último puede verse como el enfrentamiento entre ellos al escacear su comida, es decir, las presas).

Si bien la idea analítica es bastante sencilla, llevar esto a una simulación multiagente es un proceso más complejo. En este proyecto se implementaron 3 arquitecturas para modelar esto de diferentes formas. Solo se explicarán la 2da y 3ra ya que la 1era es muy similar a la 2da pero menos compleja, y solo contaba con una población de presas.

## Ideas generales del Medio Ambiente

El Medio Ambiente será el espacio donde los agentes ejercerán su autonomía. Dependiendo sus características este podrá ser más o menos compeljo. Pero las características principales que se tuvieron en cuenta fueron:

- Pequeña y Medianamente Accesible (2da Arq y 3ra Arq resp)
- No determnista
- Dinámico
- Episódico
- Continuo (dentro de lo que cabe el uso del término ya que en el fondo la continuidad en la práctica hay que discretizarla)

Como se puede observar estas características complejizan bastante la implementación del Medio Ambiente. Las diferentes caraterísticas en cada una de las Arquitecturas se comentarán en su apartado, pero a rasgo general se comentarán algunas.

El Medio Ambiente cuenta con un mapa donde los agentes se moverán, comerán, se reproducirán e interacturán. Este terreno puede contar con obstáculo, y en las últimas arquitecturas se añadieron escondites (que son zonas seguras para las presas). La Percepción de los Agentes será la visión con la que cuentan en cada instante de tiempo. Esta visión es modificable, y se configura como el radio a la redonda de la posición en la que se encuentra el agente. Realmente a la redonda, es una forma de decir, ya que será un cuadrado centrado en el agente. Esta visión cuenta con la comida, presas y depredadores que hay en la zona de visión, y es una percepción común para tanto agentes presas, como depredadores, salvo que los depredadores detectan los escondites como obstáculos y no lo saben diferenciar. La producción de comida para las presas será un evento episódico, con distribución Exponencial con media igual a la media de frecuencia de producción de comida que se desee (este parámetro es modificable, pero se recomienda fijarlo). La reproducción en la 1era y 2da Arquitetura se concibieron también episódicas, pero en la 3era Arquitectura esto sufre un cambio radical.

La arquitectura del Medio Ambiente (base) en la práctica tiene una estructura abstracta como se puede ver en [environment.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulator/environment.py) donde se debe definir la función `transform` que será ala que con las acciones de los agentes hará cambios en su estado. Además con la función `next_step`, lo que se debe hacer es ejecutar una unidad de tiempo en el sistema. Ambas son particulares para los Medios que se implementen. Por comodidad se agregaron unas funciones `see(self, agent)` y `get_see_function(self, type_agent)` para facilitar la creación de las funciones de Percepciones de los agentes. Estas ya están implementadas, solo se necesita definir un diccionario `_see_functions` como propiedad de la clase que tenga como llaves, los tipos de los agentes, y como valor la función de percepción del tipo de agente. De esta forma será muy fácil trabajar con la función `see(self, agent)`. Supongamos que `AgenteX` y `seeAgentX` (con X= 1, 2,3) son los tipos (clases) de agentes y funciones de percepción de los tipos de agente respectivamente entonces con definir:

```
self._see_functions = {
    Agent1: seeAgent1,
    Agent2: seeAgent2,
    Agent3: seeAgent3
}
```

se puede hacer un uso sencillo de `see(self, agent)` para generar la Percepción del Agente `agent` independiente del tipo de agente que sea.

## Ideas generales en la simulación de los agentes

Los agentes inteligentes se pueden agrupar en 3 grandes grupos:

- Reactivos: Percibe el medio ambiente y responde antes sus cambios
- Proactivos: Se define objetivos a cumplir
- Sociables: Interactuan con otros agentes

Para las simulaciones realizadas nos enfocamos en los 2 primeros tipos de agente, aunque para la 3ra Arquitectura, los agentes cuentan con pinceladas de sociabilización desde un punto de vista más conceptual y sencillo, pero no se podría categorizar como sociables del todo.

En la 1era Arquiectura solo se tuvo en cuenta Agentes Puramente Reactivos, es decir, agentes que solo con la Percepción actual del medio reaccionan antes sus cambios sin considerar una historia. El resultado de esta simulación realmente no fue malo, pero solo se consideraba una especie animal, sin embargo en los resúmenes explicaremos que realmente esta modelación de un animal, en realidad se comporta como el modelo analítico Depredador-Presa, donde el depredador es este animal, y la presa es la comida. En la 2da Arquitectura también se consideraron agentes reactivos, con algunos heurísticas en sus comportamientos pero predominando un comportamiento reactivo. Ya en la 3era Arquitectura se hizo una aptación de arquitecturas de capas donde los agentes ahora eran principalmente proactivo, donde se definía un objetivo y perseguían este; sin embargo contaban con algunas características reactivas, de acorde a las circunstancias.

Antes de seguir debemos llamar la atención en que trabajamos con agentes con estados internos por lo que se definió un clase Abstracta para representar este tipo de agente. Los agentes de por sí deben tener la función `action(self, P)` que dada las percepciones genere una acción. Esto se puede ver en la clase `Agent`. Pero como queremos ahora agregar stados internos, entonces creamos otra clase abstracta `AgentState` que además cuenta con la función `next(self, P)`, la cual recibe las percepciones del medio, realiza cambios, y luego al ejecutar `action` se genera una acción. Ver [agent.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulator/agent.py).

## Arquitectura 2
----------
### Basada en la Arquitectura Brooks

Para agentes puramente reactivos vimos conveniente implementar una arquitectura de agente basada en Brooks. En esta se definen conductas de la forma:

$$<predicado, acción> $$

y se establece un ordenamiento estricto. Luego para saber qué acción debe ejecutar un agente se evaluan los predicados de las conductas ordenadas, y para el primero que sea cierto, se ejecuta la acción correspondiente.

Para tener una mayor comodidad a la hora de trabajar a lo largo del tiempo, se definió primeramente la base abstracta de un Agente de Brooks en [agent.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulator/agent.py) como `BrooksAgent` y tiene este comportamiento ya implementado, solo bastaría con definir una lista ordenada por prioridad como propiedad del agente con el nombre `self.behaviors`. Esta lista debería contener tuplas de la forma, ya explicada, y deben ser funciones, que en el primer caso sería un predicado o condicional, y en el segundo, lo que produce es una acción. Ambas funciones deben recibir las percepciones que fueron captadas.

Por ejemplo:
```
cls._behaviors = [                
                (condicion_para_esconderse, accion_de_esconderse),
                (condicion_para_buscar_escondite, accion_de_buscar_escondite),
                (condicion_para_huir, accion_de_huir),                
                (condicion_para_comer, accion_de_comer),
                (condicion_para_buscar_comida, accion_de_buscar_comida),
                (condicion_para_caminar, accion_de_caminar),                
            ]
```

esta es una forma válida de definir las conductas del agente presa. Solamente es necesario ahora tener bien definidas las funciones de condiciones y las de acciones. En [/simulator_02/agent.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulators/simulator_02/agent.py) se encuentra la definición completa de todas las reglas, ya que aquí solo se presentaron estas para una mejor visualización; pero en la práctica hay otras conductas pero más internas relacionadas con los estados del agente. A continuación se mostrarán las reglas escogidas para estos agentes.

*Presa*:

- Comiendo $\Rightarrow$ Seguir Comiendo
- Hay depredadores cerca y hay escondite $\Rightarrow$ Quedarse escondido
- Hay depredadores cerca $\Rightarrow$ huir
- Hay comida y Energía $\le \alpha$ Energía Máxima $\Rightarrow$ Comer
- Energía $\le \beta$ Energía Máxima $\Rightarrow$ Buscar comida
- `True` $\Rightarrow$ Moverse Aleatorio

*Depredador*:

- Comiendo $\Rightarrow$ Seguir Comiendo
- Hay comida y Energía $\le \alpha$ Energía Máxima $\Rightarrow$ Comer
- Energía $\le \beta$ Energía Máxima $\Rightarrow$ Buscar comida
- `True` $\Rightarrow$ Moverse Aleatorio

Note que con estas reglas sencillas se puede empezar a hacer simulaciones a ver el comportamiento de los agentes.

Con respecto al *Medio Ambiente* hay que tener en cuenta que la reproducción de comidas para las presas se hacía de forma uniforme en todo el terreno, según un périodo de tiempo premedio distribuido con una función exponencial, y en una proporción del área. Estos parámetros son regulables. Por otro lado la reproducción de las especies estaba dada por también eventos episódicos discretos (distribuidos con función exponencial igualmente, y variable). Sin embargo la reproducción tenía la característica de ser en proporción a la población, lo cual es lógico, pero solamente y de forma única para las presas, si nos basamos en el modelo diferencial. Sin embargo el crecimiento de los depredadores dismuniye con la población de estas. Para hacer esto más real, se agregó un factor de energía para reproducirse, donde a la hora de reproducir a la población de cualquier agente, solo crecerá la población proporcional a la catidad de agentes con la enrgía suficiente para esto. Este parámetro es controlable y tambíen el índice de densidad de reproducción.

NOTA: Esto último es una consideración super imortante del modelo, ya que se podría dar el caso de que se acaben las presas, y que con una población muy grande de depredadores el crecimietno de los depredadores sea casi constante o incremental sin alimentación, debido a que aunque nunca ganan energía, estos se pueden reproducir en grandes cantidades.

## Arquitectura 3
----------
### Basada en Belives-Desires-Intentions (BDI)

En la 3ra Arquitectura los agentes ahora dejaron de ser complemente reactivos, y se volvieron principalmente reacctivos. Estos agentes son ahora de Razonamiento Práctico, es decir, deciden qué objetivos quieren lograr, y planifican cumplir su objetivo. Sin embargo tienen la capacidad de replantearse sus obejtivos.

En la práctica se implementó la arquitectura BDI como base para este tipo de agente. La implementación base se encuentra en la clase `ProactiveAgent` dentro de [agent.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulator/agent.py). En esta se conciben 3 funciones principales:

- `brf(self, P)`: Que disponiendo de las creencias actuales se formulan nuevas creencias.
- `options(self, P)`: De las creencias e intenciones actuales, se formulan nuevos deseos.
- `filter(self, P)`: De las creencias, deseos e intenciones actuales, se formulan nuevos intenciones y se ejecuta una nueva acción

Podemos entenderlo mejor con el siguiente mapa conceptual:
![Razonamiento Práctico](/img/RazonamientoPractico.png)

Llevarlo a la práctica realmente es lo complicado, ya que había que materializar estas abstracciones. Para ello explicaremos las cosnideraciones por cada una de estas funciones. Antes de hacer esto comentaremos la estructura de este nuevo Medio Ambiente.

*Medio Ambiente*

Ahora el Medio Ambiente es un poco más complejo. La reproducción de los agentes solo será permitida individualmente por agente, y no global y episódica sino más dinámica. La reproducción de comida ahora tampoco será global pero sí episódica, pero con un nuevo elemento que se suma: **Planta**. Este componente puede verse como un agente pero realmente fue concebido como una entidad que servirá de referencia al Medio para generar comida. Además su comportamiento no llegar a ser tan inteligente como el de los otros agentes (haciendo abuso de la palabra inteligencia). Las plantas tendrán un radio de producción de comida y una media de tiempo de reproducción que serán variables, pero global para todas las plantas. Estas a su vez se considerarán obstáculos para ambas especies animales, y estas la percebirán como un obstáculo, y no como una planta, así que no tendrán una idea (inicial) de que ellas producen los alimentos. Por otra parte ahora el terreno también cuenta con zonas de madriguera (o cueva, o escondite, o como zona de madriguera). Estas porciones del mapa solo son percibidas como tal por las presas, y pueden ser transitadas por estas. En cambio los depredadores solo las perciben como obstáculos incluso si dentro tienen una presa.

Por último la percepción de los agentes en el resto de aspectos sigue siendo igual que en las anteriores arquitecturas, solo con implementaciones más optimizadas para ahorrar recursos. Sin embargo algo que debemos señalar que antes ningún agente tenía idea del mapa completo a no ser que su visión fuera lo suficieentemente grande. En esta nueva arquitectura, todos los agentes conocen el terreno entero, pero solo saben las entidades y agentes que hay dentro de su rango de visión. Esto es una ventaja que tienen ahora ambas especies a su favor en cierta medida. Además se añadió para hacer más interesante la búsqueda de rutas con el algoritmo A* que se explicará más adelante.

*BRF*:

En esta función debemos generar nuevas creencias, pero qué se considerará una creencia? Luego de pensar en varias posibles respuestos, concluímos que se debía concebir como el conocimiento que el agente puede tener del mundo y las entidades y agentes que lo rodean, producto de las percepciones que recibe. Para ello se creó un concepto de memoria inspirado en la mente de nosotros los humanos. Esta memoria es capaz de guardar cierta cantidad de información y desecharla con el tiempo considerando varias heurísticas, que se explicarán en el apartado **Inteligencia en Agentes**. Las presas tendrán una memoria de comida y una memoria presas (también cuentan con una de depredadores pero realmente no se le da mucho uso). Y los depredadores también cuetan con memoria pero solo 2: la memoria de comida (o de presas) y la de depredadores.

Por lo tanto aquí se actualizarán estas memorias con las percepciones captadas, además de actualizar el avance por un camino si se logró caminar. Esto último, es producto de la proactividad de los agentes, los cuales, pueden plantearse recorrer un camino, por diferentes razones.

*OPTIONS*:

Aquí se deben generar los nuevos deseos. Pero volvemos a la interrogante de qué sería un deseo? Los deseos se deben ver como un indicador de cuánto quiere un agente ahcer una cosa. Tenemos que aclarar que tener mucho deseo de hacer algo no implica directamente que se haga eso, ya que las necesidades y deseos no siempre concuerdan, sin embargo debemos tener en cuenta que los deseos van a influir mucho en las intenciones que se formulen. En la práctica se concibió entonces los deseos como valores numéricos que dependen de las creencias, intenciones actuales y algunos factores aleatorios. Los deseos de las presas son:

- self.hungry_desire: Deseo de comer $X \sim Beta(\alpha=2, \Beta\in [1,20])$
- self.breeding_desire: Deseo de reproducirse $|X| \sim N(\mu = 0, \sigma \in [1, 10])$
- self.scape_desire: Deseo de Escapar $X \sim Exp(\lambda \in [0,2]) + 1$

