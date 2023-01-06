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

En la 1era Arquiectura solo se tuvo en cuenta Agentes Puramente Reactivos, es decir, agentes que solo con la Percepción actual del medio reaccionan antes sus cambios sin considerar una historia. El resultado de esta simulación realmente no fue malo, pero solo se consideraba una especie animal, sin embargo en los resúmenes explicaremos que realmente esta modelación de un animal, en realidad se comporta como el modelo analítico Depredador-Presa, donde el depredador es este animal, y la presa es la comida. En la 2da Arquitectura también se consideraron agentes reactivos, con algunos heurísticas en sus comportamientos pero predominando un comportamiento reactivo. Ya en la 3era Arquitectura se hizo una aptación de arquitecturas de capas donde los agentes ahora son


## Arquitectura 2
### Basada en la Arquitectura Brook


