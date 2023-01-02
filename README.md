<style>
    .line{
        height: 1px;
        background-color: red;
        width: 100%;
        position: relative;
        top: -15px
    }
</style>



# Multiagente-Depredador-Presa

[Repositorio](https://github.com/LazaroDGM/Multiagente-Depredador-Presa.git) 
Perfiles de GitHub: [Lzaro Daniel Gonzalez](https://github.com/lazaroDGM), [Francisco Ayra Caceres](https://github.com/frankayra)



## Descripcion general del problema
<div class="line"></div>

Nuestro trabajo va acerca de simular el comportamiento de animales en su habitat natural. Trabajaremos sobre la busqueda de simulaciones cada vez un poco mas inclusivas en cuanto a acciones inherentes a los animales, principalmente la interaccion entre un animal de tipo presa y un animal de tipo depredador de dicha presa, con parametros como la velocidad de moviemiento de cada raza, sus frecuencias de reproduccion, su rango de vision, etc


## Caracteristicas especificas
<div class="line"></div>

#### Simulacion 
Se busca tambien implementar lo mas inteligentemente posible el comportamiento de los animales, por ejemplo, que puedan deliberar a la hora de buscar comida, cual es la comida mas cercana para ellos, y puedan ir a su busqueda, si tienen hambre.

Ademas, queremos encontrar una manera de establecer "miedo" en las presas, y que se tenga un comportamiento de huida 

Otro factor que evidentemente puede influir en la supervivencia como factor clave es la forma en que se genera comida en el terreno. Para ello buscaremos distibuir comida en el mapa lo mas realista posible.

#### IA
En el entorno de simulacion sera necesario buscar una forma en que todas las entidades sean capaces de "ver" un espacio alrededor de ellas, y deducir de acuerdo a su comportamiento y sus prioridades, que hacer.
Por tanto, su hace necesario buscar formas de hacer inteligenemente las busquedas de comida, y de agentes o entidades de interes para el movimiento y cambio de estado interno de cada animal



## Objetivo
El objetivo final de nuestro proyecto es buscar el mayor equilibrio posible entre las dos poblaciones a lo largo del tiempo a partir de la simulacion con diferentes parametros de la interaccion entre las razas.