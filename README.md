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

- `self.hungry_desire`: Deseo de comer $X \sim Beta(\alpha=2, \beta\in [1,20])$
- `self.breeding_desire`: Deseo de reproducirse $|X| \sim N(\mu = 0, \sigma \in [1, 10])$
- `self.scape_desire`: Deseo de Escapar $X \sim Exp(\lambda \in [0,2]) + 1$

mientras que el depredador cuenta con los 2 primeros de igual forma y con el mismo intervalo de los parámetros pero particular para los depredadores.

Estas distribuciones pueden visualizarse a continuación con algunos parámetros fijados, para varias generaciones de forma discreta y continua:

#### $X \sim Beta(\alpha=2, \beta=6)$
![$X \sim Beta(\alpha=2, \Beta=6)$](/img/Beta6.png)

#### $X \sim |N(\mu = 0, \sigma = 4)|$
![$X \sim |N(\mu = 0, \sigma = 4)|$](/img/Norm4.png)

#### $X \sim Exp(\lambda = 1)$
![Discretización de $X \sim Exp(\lambda = 1$](/img/ExpLambd1.png)

*FILTER*

Aquí entonces de las posibles opciones que tenemos filtraremos qué hacer. Es decir generaremos una nueva intención o seguiremos la misma. Desde otro punto de vista aquí decidiremos si cambiamos de objetivo o no. En la definición de cada agente ([simulator_03/agent_prey.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulators/simulator_03/agent_prey.py) y [simulator_03/agent_predator.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulators/simulator_03/agent_predator.py)), hay una implementación bastnate entendible y legible de la lógica de toma de decisiones. Primero se revisan los objetivos e intenciones actuales, y si no se puede generar un nuevo cambio por la naturaleza de este, nos mantenemos. Este tipo de acciones son las que consideramos como acciones deterministas y son necesarias para poder simular comportamientos como la digestión, la velocidad y la gestación.

Luego es que se ejecuta como tal la selección de las acciones. Hay que tener en cuenta que por comodidad hablaremos en terminos generales de *Reproducirse*, *Comer* y *Huir*, pero realmente cada uno de estos comportamientos conlleva una serie de acciones e intenciones, como por ejemplo, para comer, si no se sabe dónde hay comida, entoces hay que explorar el área para encontrarla; si a veces está al alcance vamos a ir por ella; si estamos arriba de una comida y muy hambriento nos la comemos. Es decir la lógica detrás de esto es complicada y es un árbol de acciones. Entonces necesitamos abstraernos a estos términos más abarcadores para explicar las reglas que los agentes seguirán.

### Reglas para ambas especies
Siendo $X_1$, $X_2$, las variables aleatorias de los deseos ya vistas, tales que:

- $X_1 \sim Beta(\alpha, \beta)$
- $X_2 \sim |N(\mu, \sigma)|$

Entoces las reglas para comer y reproducirse son:

- $Energía Máxima \cdot X_1 \ge Energía \Rightarrow Comer $
- $Agentes Recordados \le X_2 \Rightarrow Reproducirse $

Desde cierto punto de vista luce una arquitectura de Brooks pero ahora influyen más factores no deterministas. Otras reglas que tiene la presa es con $X_3 \sim Exp(\lambda)$:

- $Cantidad Depredadores > 0 y Cantidad Depredadores \ge X_3 \Rightarrow Huir$

Por último hablemos de la reproducción. En esta simulación la reproducción se produce cuando el agente queire reproducirse y a generado bastante energía extra para reproducirse. La energía extra se genera, al comer y sobrepasar la energía máxima que se puede tener. Este excedente se va acumulando en otro indicador que al llenar o sobrepasarse, se está listo para reproducirse pero debe ser el agente el que decida esto.

En el caso de los depredadores la reproducción se concibió unitaria. Es decir un individuo tendrá a lo sumo un cría al reproducirse. Para el caso de las presas, se creó una distribución de probabilidad propia, que su forma general es:

$$ X \sim D_1(l,\alpha,\sigma,\gamma)$$

Que asemeja el comportamientoa una distribución triangular pero que puede ser truncada en sus colas. De hecho se podría decir que la dsitribución triangular sería una particularización de esta. La función de densidad para sus parámetros prefijados, sería:

$$X \sim D_1(l=1,\alpha=6,\sigma =2,\gamma=0)$$

![lo](/img/D_1d.png)

![jj](/img/D_1.png)

Esta distribución se usa para la generación de las presas, instpirado en la reproducción de los conejos, donde de un rango común de nacimiento, algunos van muriendo posteriormente en sus etapas tempranas de vida. En nuestro caso, $alpha$ sería la moda de reproducción.


## Inteligencia en Agentes

### Búsqueda en el mapa

Los agentes en el Medio tienen la capacidad de moverse, sea con cualquier fin. Sin embargo tanto agentes con arquitectura de Brooks, como BDI, basan sus acciones en condiciones previas (con sus particularidades). En base a esto es necesario definir un comportamiento para el movimiento en cada caso. A continuación se explicará de forma general cuál sería la base del movimiento estándar, y luego explicaremos las particularidades para cada agente.

Como parte de la simulación de la predicción que poseen los animales para el movimiento, utilizamos un algoritmo compuesto por dos fases.
1. Utilización del algoritmo `A*` con función de costo igual a la longitud del camino y heurística igual a la distancia de Manhatan hasta los puntos deseados a alcanzar. También se le pasan dos funciones como parámetro, ambas a la vez reciben como parámetro una posición de la matriz(x, y), y retornan si existe, un objeto buscado, y un obstáculo, respectivamente. Esta función devuelve una matriz de proximidad al agente, que contiene 9 casillas(3x3), 8 de ellas válidas, que incluyen en cada una de las posiciones, una lista de números donde:
   - Cada número implica que desde la casilla donde está se partió y alcanzó un camino, de forma óptima en distancia.
   - Devuelve -1 en las casillas próximas al agente donde se encontraba un obstáculo, según la función de detección de obstáculos en sus parámetros
2. Aplicación del algoritmo `transform`. Este **va de la mano con el resultado del algoritmo `A*`** modificado que describimos. Toma la matriz de 3x3 que se retornó y se tienen en cuenta los siguientes aspectos y transformaciones:
   1. Hará una **expansión** de las casillas válidas, o sea, que no hayan contenido obstáculos en ellas.
   2. La **expansión** es de forma intuitiva vista como: si una casilla me indica el camino para llegar a una posición que estoy buscando, las casillas adyacentes a esta, también son buenas, aunque en una menor medida...
   3. Se devolverá de este algoritmo, una matriz nuevamente de 3x3, pero en este caso ya no tendrá una lista de números en cada casilla, sino, un número por casilla.
   4. Se obtiene una 1ra matriz. Cada número de dicha matriz es la sumatoria de los números de la lista devuleta en la misma posición, pero en la matriz devuelta por el A*.
   5. Como estos números constituyen distancias, y queremos dar, a mayor distancia menor peso y viceversa, siempre hayaremos en lo que sigue, una 2da matriz que es el **valor inverso** a la distancia; este proceso en cada casilla.
   6. Se obtiene una 3da matriz constituida por la **expansión** de las casillas de la matriz anterior. 
   7. La **expansión** está constituida por la suma de todas las casillas adyacentes según el **factor de expansión** que se le pase como parámetro. El siguiente fragmento de pseudo-código es una descripción de lo que se hace a grandes rasgos para obtener estas tres matrices.


```python
positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)] # no incluye (1, 1) porque es la posición del agente
matriz_1 = matriz_2 = matriz3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

for i, j in positions:
    matriz_1[i][j] = sum(Matriz_A*_[i][j])

for i, j in positions:
    # Esto se hace para invertir el número pero mantenerlo en el rango [min_m1, max_m1]
    matriz_2 = max(matriz_1) - matriz_1[i][j] + min(matriz_1)   

factor_de_expansion = 2
for i, j in positions:
    for o, p in positions:
        # Se hace si la distancia es menor que el factor de expansión y si la esta última resta es mayor que 0. Se excluye de la suma la casilla del agente y la misma casilla
        continue if (i == o and o == p) or (distancia( (i, j), (o, p) ))  >  factor_de_expansion) or (matriz_2[i][j] - distancia( (i, j), (o, p) )  > 0)
        matriz_3[i][j] += matriz_2[o][p] - distancia( (i, j), (o, p) )  
```


   8. Luego de hacer esto se obtendrá una última matriz que es la suma de `matriz_2` y `matriz_3`, que sería la matriz de expansión
Luego de este proceso, se seleccionará el mejor moviemiento como la casilla con mayor valor(o una posición aleatoria entre las de máximo e igual valor) de las 8 casillas de la matriz de expansión; siendo esta posición la devuelta...


Todos los agentes necesitan comer, aunque lo que represente *la comida* para ambos no sea lo mismo.
 
- En el caso de las **Presas de Brooks**, como son puramente reactivas solo se generará la próxima casilla adyacente hacia donde se moverán. Para esto se utiliza la Matriz de Expansión. Las presas, necesitan comer y no ser comidas por los depredadores; por este último motivo, además de calcular la *Matriz de Expansión Invertida de Comida* ( $M_C$ ) se hallará la *Matriz de Expansión de Depredadores* ( $M_D$ ) que prioriza zonas donde haya menos depredadores (usando igualmente *`A*`* en la búsqueda). Finalmente se obtiene la *Matriz Final de Movimiento* ( $M_F$ ):
$$M_F =   c \cdot M_C + (1 - c)\cdot M_D$$
Aquí se añade una constante parametrizable $c$ para gestionar qué se priorizará más, si el comer o el huir.
 
- Las **Presas BDI** en contraste con las otras se plantean objetivos, aunque no están ajenos de modificarlos. Su proactividad se traduce en buscar un camino hacia una zona de comida, o un objeto comida en específico. En el momento de seleccionar el objeto comida en específico se utiliza la misma estrategia anterior descrita, solamente considerando la $M_C$, salvo que en este caso se genera una ruta hacia alguna de las comidas a las que se pueden acceder desde la casilla adyacente con mayor prioridad. Note que una vez teniendo el camino, no tiene que volver a hacerse este cálculo, ya que se tiene un objetivo fijado; sin embargo, el agente puede replantearse de nuevo sus objetivos y dicho caso, si lo que AÚN QUIERE es comer entonces se hace nuevamente este proceso.  
Con respecto a la huida de este agente, esta será reactiva con un movimiento similar al de la Presa Brooks, considerando en vez de la *Matriz de Comida*, la *Matriz de Madrigueras* que no es más que una *Matriz de Expansión Inversa de Madrigueras*.
$$M_F =   c \cdot M_M + (1 - c)\cdot M_D$$

- Los **Depredadores Brooks** para comer se comportan iguales a las Presas de Brooks, lo que su *Matriz de Prioridad Final* está dada por la *Matriz de Expansión Inversa de Depredadores*.
$$M_F = M_P$$
- Los **Depredadores BDI** se comportan análogos a las Presas BDI solamente para comer, ya que estos no necesitan huir; y claramente la selección de la zona de presas, o una presa específica, lo que tiene en cuenta para la ruta, es la *Matriz de Presas*.

La combinación de estas estrategias, más las pequeñas bases de conocimiento que poseen los agentes que explicaremos a continuación, permiten hacer el diseño de la *Planificación* de los agentes BDI, que se explicará al final.

### Conocimiento en los agentes

Los agentes BDI en su propia estructura requieren un conjunto de creencias en la teoría. En la práctica había varias formas de plasmar estas creencias, y una forma de estas era generando alguna especie de conocimiento particularizado a lo que a cada agente le importe. Los agentes procesan las percepciones que reciben, y a estos DATOS puede dársele una interpretación momentánea generando conocimiento. En la práctica esto se hace para los Agentes Brooks pero note que realmente no es un conocimiento que se pueda almacenar, ni reutilizar para deducir *algo*. En cambio con los Agentes BDI, la estrategia fue diferente: estos de las percepciones recibidas generan nuevos datos para incorporarlos a una base de conocimientos que llamaremos *Memoria*, y luego utilizan esta memoria para inferir ciertas informaciones.

La intención era crear una especie de memoria para los agentes similar a como funciona (en parte) el cerebro animal para recordar, inspirado un poco en la capacidad que tienen los humanos para esto. El conocimiento que se quiere generar es sobre las zonas de comida de ambos agentes (los objetos comida para las Presas, y las Presas para los Depredadores). La idea general para modelar esto se basa en:

- Recordar un objeto, un evento, o algo (en sentido general) tiene un grado de importancia.
- El conjunto de elementos recordados (recuerdos almacenados) es limitado
- Cuando la capacidad de la base de conocimientos está llena, se hace necesario eliminar alguna de las informaciones almacenadas para permitir que se incorpore información nueva.
- Con el tiempo el conocimiento que se tiene se va desgastando (se eliminan recuerdos)
- El conocimiento desechado por lo general debe ser el menos relevante.

En el caso particular de nuestros agentes lo que se almacena en su *Memmoria* es las posiciones en las que estando ellos parados, pudieron ver una mayor cantidad de comida en su área de visión. Y la importancia de recordar esta posición estará dada por la proporción de comida con respecto a su área de visión, es decir, mientras más comida hay en su área de visión, mayor será la importancia atribuida a la posición actual. Note que una primera idea era recordar exactamente las posiciones de la comida pero realmente creemos que nosotros como humanos recordaríamos (en casos similares a este), regiones donde hay comida, y no justo el lugar donde hay comida; la ventaja de recordar el área es que sabremos que por lo general, cerca de la posición encontraremos comida, mientras que solo recordando las posiciones de la comida y a cudiendo particularmente a ella, tendremos más probabilidad de no encontrar lo que buscames y que cerca de dicha posición, tampoco encontremos nada que nos interese. Llevado a la vida real, si estamos en un centro comercial, sabemos que tendremos opciones cercanas de puestos de comida en el área del patio de comida, en cambio si recordamos que en algún pasillo de este había un puesto de dulces y nos dirijimos a este, corremos el riesgo de que esté cerrado, o ya no exista, y estaremos lejos de los restantes puestos de comida del centro comercial.

A continuación se explicará a profundidad detalles de la implementación de la *Memoria de Comida* y las reglas que sigue para recordar y olvidar (agregar y eliminar conocimiento).

#### Memoria
- La memoria está constituida básicamente por una estructura que contiene 4 `slots` o espacios, los cuales tienen diferente prioridad para recordar.
- Cada uno de los `slots`: 0, 1, 2 y 3; tienen de mayor a menor prioridad para recordar, en ese orden, siendo el slot 0 el que más prioridad tiene.
- El funcionamiento tiene los siguientes aspectos:
  1. Al introducir un evento en la memoria, esta pide un **factor de importancia** atribuido al evento, este determina en cual de los `slots` de la memoria estará adjunto dicho evento a recordar.
  2. El **factor de importancia (f)** es un número entre 0 y 1, y se asignará un evento a un slot según la siguiente tabla:

        |<center>0</center>|<center>1</center>|<center>2</center>|<center>3</center>|
        |-|-|-|-|
        |0.25 $\leq$ f $\leq$ 1|0.2 $\leq$ f < 0.25|0.1 $\leq$ f < 0.2|0 < f < 0.1|
    3. Fijarse que con esto simulamos el aspecto realista de la memoria para recordar más, un evento de mayor significación o importancia.
    4. También hemos decidido que solo se olvide a lo sumo un recuerdo a la vez para hacer balance entre la acción de olvidar con el tamaño pequeño de la memoria.
    5. La memoria, al igual que la simulación en general pasa por unidades de tiempo o **Ticks**. Para olvidar un evento se hará de la siguiente forma según el slot donde esté ubicado cada evento: 
        |<center>Slot</center>|<center>Multiplicidad del Tick</center>|
        |---------------------|------------------------------|
        |**0**|8|
        |**1**|4|
        |**2**|2|
        |**3**|1|
        Así que por ejemplo:
        - en el **tick número 16 se olvidará el evento más antiguo del slot 0** 
        - en el **tick 12 se olvidará el evento más antiguo del slot 1** 
        - en el **tick 3 se olvidará el evento más antiguo del slot 3**
        - en el **tick 6 se olvidará el evento más antiguo del slot 2**
    
        De forma que se puede decir que la memoria olvida el recuerdo más antiguo del slot con una multiplicidad igual al máximo común divisor entre 8 y el tick actual :)

#### Reemplazo de Recuerdos

La memoria no siempre tiene que agregar y quitar las posiciones que recuerda el agente, ya que estaríamos olvidando o lugares lejanos al actual en el que sabemos que hay mucha comida, o estaremos agregando repetidamente lugares en la misma zona para especificar que hay comida. Para eso agregamos una heurística de reemplazo de recuerdos.

La idea principal es, que si recuerdo que cerca de aquí hay comida, reemplazo la posición vieja de comida por la actual restaurando su *tiempo* en ser eliminada. Note que de esta manera, preservamos lugares distantes, y evitamos la inundación de la memoria de comida con valores muy similares. Ahora bien, la heurística creada en la práctica usó la distribución creada por nosotros comentada arriba pero ahora con los parámetros siguientes:

$$ X \sim D_1(l=2,\alpha = 6,\sigma = 1,\gamma=0)$$

Su distribución puede verse así:

![Memoria](/img/D_1Memoria.png)

Una vez distribuida esta variable, se comprueba que:

$$Manhathan(actual, vieja) \le X $$

y de ser así se reemplaza. Note que siempre se reemplazarán las distancias menores o iguales a 2. Y además tenga en cuenta que el reemplazo, reinicia el conteo de eliminación.

#### Recomendación de la Memoria
 
Un aspecto que no se ha mencionado es que la *Memoria* almacena conocimiento, pero no hemos hablado de cómo se infiere un conocimiento de esta. La intención de guardar información de zonas de abundancia de comida, es para poder después deducir lugares con alta probabilidad de encontrar comida al estar el agente sometido a diversas condiciones pero que en su raíz parte de la necesidad de buscar comida (tanto para comer por hambre o por reproducción). La *Memoria* realiza una recomendación de las mejores zonas principalmente. Para ello reparte las porciones de memoria como si fuera una ruleta, es decir, se le asignará a cada bloque un valor de importancia (entero positivo, $I(bloque)$) y la probabilidad de seleccionar un bloque $X = {1,2,3,4}$, será $\frac{I(X)}{I(1) + I(2) + I(3)+ I(4)}$. Luego del bloque candidato se selecciona uniformemente al azar una posición y esta pasa a ser la posición recomendada.

Adicionalmente la recomendación se amplía si la memoria recibe (opcionalmente) un conjunto de posiciones extras, categorizadas como posiciones de baja importancia y que en la práctica son posiciones aleatorias del terreno donde no se sabe realmente información de la existencia de comida. Si este conjunto no es vacío, a la función de probabilidad mencionada solo habrá que agregarle un sumando $I(5)$ en el denominador, y $X = {1,...,5}$, siendo $X=5$ el conjunto de posiciones extras. Note que esta opción lo que permite es incitar exploración de zonas desconocidas, y tendrá más peso cuando la *Memoria* esté ligeramente vacía.

La importancia dada por bloque es la siguiente:

- $I(1) = 8$
- $I(2) = 5$
- $I(3) = 3$
- $I(4) = 2$
- $I(5) = 1$

La implementación de la memoria se encuentra en [memory.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/simulators/simulator_03/memory.py) con todos los detalles antes comentados.

Por último y no menos importante de a forma en que está definida la Memoria puede ser considerado un Sistema Experto dedicado a la sugerencia de zonas de interés para los agentes. Hay que tener claro que sus características lo vuelvan un sistema basado en reglas, pero con detalles probabilísticos, por lo que no debería considerarse un sistema completamente puro. Y a nuestro criterio la caractéristica principal que no lo hace un sistema experto típico, es la constante y AUTOMÁTICA actualización de su base de conocimientos, que aunque muchos sitemas tienen actualizaciones de esta, por lo general no son completamente automáticas y retroalimentadas.

Nota: Una mejora que se le pudiera hacer al sistema, o que se puede tener en cuenta para otros proyectos similares, es en la *Modificación de Recuerdos*, incluir la eliminación o modificación de recuerdos corruptos. El concepto de recuerdo corrupto se inclinaría a información en la base de conocimiento que ya no es correcta, lo cual en nuestro caso sería que para una posición (muy) cercana a la actual haya un recuerdo en la memoria en un bloque muy diferente al que se puede *suponer* que pertenecería. Por ejemplo, un recuerdo corrompido de una posición cercana a la actual, es que en la percepción actual la proporción de comida sea nula, y dicha posición esté categorizada como de abundante comida; en este caso no se puede asegurar que esa posición sea de proporción nula igualemente, pero sí se podría SUPONER que ya NO ES de gran abundancia. Esta mejora tiene sentido agregarla con reglas basadas en probabilidades bayesianas. Sin embargo note que la Modificación de Recuerdos actual limpia datos corruptos pero solo de la posición actual.

### Planificando Intenciones

Luego de explicado todo lo anterior estamos preparados para unificar todas estas en la arquitectura BDI de los agentes. Como sabemos el último paso decisivo de estos tipos de agentes es la selección de una intención o seguimiento del objetivo que ya tenía. La intención se puede ver como un conjunto de acciones que se deben llevar a cabo con un fin objetivo, por lo tanto implícitamente el agente cae en un problema de Planificación.

Para seleccionar qué intención realizar, cuando no se tiene objetivo, se emplean tanto las creencias (lo cual incluye la *Memoria de Comida*) y la visión actual, así como otras informaciones internas del agente. Visto como un todo, incluso el esquema puede concebirse como un problema de planificación pero con la característica de que muchas precondiciones para realizar una acción están dadas por parámetros probabilísiticos. Sin embargo, no lo veamos desde este punto, y enfoquémonos en los lugares donde se usa la planificación explícitamente, pero adaptada a nuestra implementación de agentes.

Estamos hablando de cada una de las intenciones que el agente puede realizar. Estas intenciones son por separado un problema de planificación, donde los objetivos finales son: comer o reproducirse. Note que para el caso de la Presa, *HUIR* es una intención pero como su resolución es puramente reactiva, no se incluye aquí como Planificación. En la práctica cada acción que puede ejecutar requiere precondiciones para poder cumplirse, y poscondiciones luego de realizada estas acciones. Particularmente en la implementación de los agentes, las precondiciones incluyen factores internos del agente pero también factores externos (como algunas de las variables probabilísticas comentadas en el proceso de simulación). En cuanto a las poscondiciones, son cambios internos del agente y del Medio, pero hay una peculiaridad, el Mundo puede bloquear la actualización de las postcondiciones del agente. Esto sucede cuando la acción que ejecuta el agente no lo puede hacer:

- Caminar hacia una posición donde hay otro agente de su misma especie, es decir, choca. En este caso el Medio sabe diferenciar qué movimientos permitirá en los agentes, para que no ocurra la colisión, por lo tanto bloqueará la acción del agente.
- O por un cambio inconsistente de estado, en cuyo caso, computacionalmente será detectado mediante una especie de **contratos** implementados, y cerrará la simulación. Realmente esto se puso para testear que la implementación de la planificación fuera consistente. Actualmente un error de este tipo no debe ocurrir, solo se comenta para conocimiento del lector.

Con respecto a lo primero se podrá preguntar por qué el agente quisiera moverse hacia una posición ocupada por un agente de su misma especie. Pues la respuesta es sencilla y tiene varios motivos. El primero es que en su camino objetivo actual fue interceptado por otro agente. El segundo es que para formar un camino el agente no tiene en cuenta a los demás agentes como obstáculos, ya que de ser así muchas veces no podría planificar un camino a seguir hasta su objetivo final, por simple obstrucción, pudiendo realmente moverse y detenerse solo si la obstrucción continúa. Con respecto a esto se agrega una heurística muy sencilla en el movimiento que se explica en **Caminata Inteligente**.

Teniendo estas consideraciones, cuando el Medio Ambiente prohibe a un agente una acción, la forma que tiene de no provocar un estado inconsistente del propio agente es *decirle* que se mantenga en su estado actual, lo que en otras palabras sería, que el agente nunca haga la acción, manteniendo la consistencia.

Otra característica de concebir una planificación con algunas reglas en parte casi secuenciales como para la intención comer (un ejemplo a modo general):

- Buscar comida :- Si se desconoce de una fuente de comida
- Ir hacia la comida (generar un camino y seguirlo) :- Si sabemos de la existencia de comida
- Ir hacia la comida (generar un camino y seguirlo) :- Si hay comida visible y el hambre es DEMASIADA
- Moverse por el camino objetivo :- Si estoy iendo a comer
- Comer :- Si estoy justo donde hay comida

es que el árbol de secuencias de acciones es poco ancho y más profundo. Esto facilita recorrelo con algoritmos sencillos y menos complejos sin mucho problema. En nuestro caso se explora de forma parecida a un BFS. Por cada nivel se evaluan precondiciones para seleccionar la próxima acción, y una vez seleccionada siempre se garantiza que se podrá llegar al objetivo, porque los nodos finales, serían objetivos tambíen, pero lo que cambia es la forma de cómo llegar a cada uno. Luego en la nueva capa se vuelve a comprobar las condiciones y seleccionar y así sucesivamente. Como la cantidad de condiciones es poca en eficiencia no se pierde mucho, ya que sería casi lineal el recorrido suponiendo que tenemos una cantidad de fija de ramas por nodo, lo cual se garantiza.

Algo interesante es que el agente cambie de objetivo, lo cuál es muy posible por el parámetro `bold` que tienen los agentes para replantearse sus objetivos o no. En este caso la planificación actual se cancela o se reinicia; es decir, se debe elegir nuevamente si se quiere *comer*, *reproducirse*, *huir* o *caminar aleatorio*, y si casualemente volvemos a caer en *comer* o *reproducirse* ejecutamos la planificación.

La implementación de todas las intenciones de cada agente están en sus respectivas clases, bien delimitados con comentarios separadores, al igual que las acciones que puede hacer cada agente.

### Caminata Inteligente

Tanto depredadores como presas, cuando se plantean recorrer un camino, este puede ser interceptado por otro agente de su misma especie con el que colicionará. Si colisiona tendrá que esperar un tiempo para poder proseguir, o tendrá que recalcular su nueva ruta. Para evitar el corte en el flujo del tráfico intraagente, se diseñó una heurística de reconstrucción de camino. Esta es muy sencilla e intuitiva.

Cuando en el camino objetivo, la casilla a la que el agente se va a mover en este momento está ocupada, este considerá cambiar su ruta modificando la siguiente casilla, a una adyacente tanto a la actual en la que se encuentra, como a la que en el turno despues del siguiente debe moverse. De esta forma el camino queda igual de consistente. Increíblemente los mejores resultados dieron con probabilidades bastantes altas para cambiar de camino.

- 50% seguir en la actual y 25% para cambiar a dos posibles adyacentes
- 66% actual y 33% para cambiara a una sola posible adyacente

## Resultados Finales obtenidos

Luego de todo lo antes explicado se fijaron varios paráemtros y se corrienron simulaciones para observar la cantidad de presas, depredadores y comida a lo largo del tiempo, así como la esperanza de vida de ambas poblaciones, y los mapas de calor de las zonas más visitadas en el mapa. Los parámetros variables se muestran a continuación y son aquellos de los que depende la toma de decisiones de los agentes. Empezaremos con el vector que propusimos probar y luego se explicarán cómo se mejoran los resultados, nuevamente haciendo uso de la inteligencia artificial y esta vez con metaheurísticas.

Con los parámetros iniciales supuestos

- alpha: 6
- gamma: 0
- lambda: 1
- beta_prey: 6
- beta_predator: 9
- sigma_prey: 4
- sigma_predator: 2
- bold_prey: 0.8
- bold_predator: 0.8

obtuvimos los siguietes resultados:

Presas en el tiempo

![](/img/test4Preys.png)

Depredadores en el tiempo

![](/img/test4Predators.png)

Mapa de exploración de las Presas

![](/img/test4HeatMapPreys.png)

Mapa de exploración de los Depredadores

![](/img/test4HeatMapPredators.png)

Presas y depredadores al pasar el tiempo

![](/img/test4Circ.png)

Además la esperanza de vida fue de:

- Presa: 1790
- depredadores: 2951

#### Interpretación de las observaciones realizadas

El mapa cuenta con obstáculos que son los cuadros completamente negros en los mapas de calor. De estos obstáculos hay plantas en las posiciones (12,2), (11,15), (8,24), y (3,18). Así como refugios en las zonas casi cerradas, superior izquierda e inferior derecha. Como el parámetro de la huida de las presas es bastante alto, consideran más en huir por lo que tiene sentido que la zona más concurrida es la de la madriguera y sus alrededores, así como que tiene más sentido la preferencia de la inferior a la superior por la cercanía a más plantas e implícitamente alimentos. También se puede notar que alrededor de la planta (12,2) hay una zona bastante visitada. Con respecto a los depredadores se puede notar que las zonas más visitadas son alrededor del refugio inferior de las presas, lo cual tiene sentido ya que son un área concurrida de las presas. Además se puede notar que los depredadores tienden a dejar un rastro en el mapa de calor del camino principal que toman para cambiar de una entrada de la madriguera a otra, al tener que dar la vuelta para obviar obstáculos.

De las gráficas de presas y depredadores en función del tiempo, se puede notar que hubo muchas simulaciones donde no se alcanzó el equilibrio y al menos alguna de las 2 especies murió. Se puede notar que el promedio de los resultados de los depredadores que la población de esta especie tiende a desaparecer con el tiempo.

### Más Inteligencia Artificial

Como queremos mejorar los resultados obtenidos, utilizamos metahurísticas para generar varios vectores de parámetros que en un principio proporcionaran la mayor cantidad de equilibrio al sistema. Para ello se implementaron varios algoritmos de metaheurísticas, entre ellos la búsqueda aleatoria, y el ascenso de colina. Con ellos primero generamos varios conjuntos de 10 simulaciones para cada corrida y utilizamos una función de fitness que considerara el promedio de equilibrio de todas las simulaciones. La intención era generar primero algunas buenas soluciones aletorias y luego hacer el ascenso de colina. Para ello utilizamos las 10 mejores soluciones que nos dio el algoritmo para 25 generaciones de vectores. E hicimos ascenso de colina. El resultado fue el siguiente para uno de los 10 vectores nuevos:

- alpha: 2.9
- gamma: 0.82
- lambda: 0.5
- beta_prey: 5.9
- beta_predator: 1.26
- sigma_prey: 8.25
- sigma_predator: 2.6
- bold_prey: 0.85
- bold_predator: 0.13

Presas en el tiempo

![Presas en el tiempo](/img/test9Preys.png)

Depredadores en el tiempo

![Depredadores en el tiempo](/img/test9Predators.png)

Mapa de exploración de las Presas

![Mapa de exploración de las Presas](/img/test9HeatMapPreys.png)

Mapa de exploración de los Depredadores

![Mapa de exploración de los Depredadores](/img/test9HeatMapPredators.png)

Presas y depredadores al pasar el tiempo

![](/img/test9Circ.png)

La principal desventaja que tenía la combinación anterior era que nos limitábamos a lo sumo a obtener 10 máximos locales, que podían ser menos si algún vector durante el ascenso cambiaba de región convexa. Sin emabrgo para los 10 resultados obtenidos hubo 4 vectores que su valor fue máximo ya que como la función fitness se basaba en el promedio del tiempo en que estuvieron en equilibrio, el máximo que se podía obtener era 30 000 unidades de tiempo que era lo que duró cada simulación. De estos 4, se hicieron 32 simulaciones nuevamente (ya que antes solo se hacían 10 por vector para agilizar un poco la búsqueda), y el vector con los siguientes parámetros:

- alpha: 5.38
- gamma: 0.62
- lambda: 0.25
- beta_prey: 10.8
- beta_predator: 16.82
- sigma_prey: 9.34
- sigma_predator: 6.72
- bold_prey: 0.78
- bold_predator: 0.17

fue el que en promedio alcanzó el mejor equilibrio, pero esta vez tuvo 1 fallo de las 32 simulaciones, donde murieron los depredadores casi desde el inicio. Por lo tanto aunque alcanzó el máximo global en la función de fitness, si hubiéramos cambiado dicha función a hacer las 32 simulaciones, no hubiera alcanzado ese máximo. Sin embargo los resultados fueron los mejores. Note que esta vez, se estabilizan comportándose casi constante en el tiempo el promedio de las poblaciones de presas y depredadores. Además algo interesante es que este vector no prioriza tanto la huida las presas y estas reflejan en el mapa de calor mayor concurrencia cerca de las plantas. Los depredadores por otra parte se focalizan en zonas de tránsito de las presas entre plantas y plantas, o plantas y refugios.

Presas en el tiempo

![](/img/test8Preys.png)

Depredadores en el tiempo

![](/img/test8Predators.png)

Mapa de exploración de las Presas

![](/img/test8HeatMapPreys.png)

Mapa de exploración de los Depredadores

![](/img/test8HeatMapPredators.png)

Presas y depredadores al pasar el tiempo

![](/img/test8Circ.png)

Presas y depredadores al pasar el tiempo en equilibrio

![](/img/test8CircFinal.png)

### Inferencia de funciones

Algo notable es que de los vectores obtenidos 4 fueron máximos globales-locales, que tal vez para una función fitness mucho más detallada no tenían que ser los máximos globales. Sin embargo lo curioso es que de los 4 hay, 3 muy parecidos entre ellos, incluído el vector anterior:

- [5.38, 0.62, 0.25, 10.8, 16.82, 9.34, 6.72, 0.78, 0.17] (Vector anterior presentado)
- [5.17, 0.46, 0.36, 12.5, 15.88, 7.30, 6.74, 0.85, 0.30]
- [5.89, 0.48, 0.28, 11.5, 16.52, 9.23, 7.00, 0.78, 0.16]

En sentido general como se tuvo 10 máximos locales, es posible que la función objetivo tenga muchos focos de altura, y posiblemente gran cantidad de máximos locales. Sin embargo al ver estos vectores se puede suponer que haya algunas zonas de *mesetas*, lo que en este caso particular, sería una meseta máximo global, pero que no tiene en primer lugar ni que ser cierto en este escenario, ya que a pesar de la cercanía pueden ser máximos locales de diferentes focos, y en segundo lugar como la función fitness tenía menos simulaciones, lo más probable es que como pasó con el vector anterior, puedan tener algún fallo y no ser máximos globales para un fitness que considere 32 simulaciones. Lo que sí se puede estar casi seguro es que la función actual debe tener muy probablemente muchos máximos locales y tal vez algún tipo de meseta ocasional.

### Algoritmo genético

Es evidente la mejora pero, pero luego quisimos tratar de probar otra estrategia y utilizamos un algoritmo génetico para mezclar soluciones y obtener nuevas, considerenado principalmente el promedio entre soluciones, y una combinación de valores. Realmente no se tuvo buenos resultados al hacer esto, y suponemos que por dos motivos fundamentales:

- Al considerar el promedio de valores se está explotando implícitamente.
- No hay mutación en la población, lo cual le quita muchísimo de exploración al algoritmo

Una forma de mejorar esto es añadiendo directamente la generación de nuevos vectores aleatorios y excluyendo algunos de los mejores de la población. Lo primero se añadió a la implementación pero no se han hecho las simulaciones pertinentes para dar nuevos resultados (Ver [/metaheuristics/genetic.py](https://github.com/LazaroDGM/Multiagente-Depredador-Presa/blob/main/metaheuristics/genetic.py)). Sin embargo el resultado que hemos alcanzado con el proyecto nos es muy satisfactorio, no tan solo porque logramos alcanzar en promedio el equilibrio del sistema, o porque pudimos predecir comportamientos en los agentes según las lógica de accionar que les dimos, sino porque también aprendimos bastante en sentido general de muchos aspectos fundamentalmente prácticos de las Disciplinas de Simulación e Inteligencia Artificial. Por lo tanto para finalizar mostraremos un ejemplo de una sola simulación con el último vector de parámetros que se explicó anteriormente.

## Ejemplo de una sola simulación

Ahora que ya vimos el comportamiento del sistema de forma general veamos los resultados particulares para alguna de las simulaciones (Población de presas (azules) y depredadores (naranja) en función del tiempo).

![](/img/test8Particular.png)

si tomamos los valores a partir de los cuales se comienza a equilibrar el sistema, el gráfico sería:

![](/img/test8ParticularNoFood.png)

De esta forma podemos concluir el proyecto de forma exitosa cumpliendo los objetivos que queríamos alcanzar!!!
