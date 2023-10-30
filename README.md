<div align="center">
  <a href="https://github.com/H4RRY73/tf-algorithmic-complexity">
    <img src="./UPC_logo_transparente.png" width="200px">
  </a>
  
  <h1 align="center">TSP</h1>

  <p align="center">
    Peruvian University of Applied Sciences.
    <br />
    Computacional Mathematics.
    <br />
    Teacher: Luis Daniel Muñoz Ramos
  </p>
</div>

### Integrantes
| Apellidos y Nombres        | Codigo     | Coevaluacion |
|----------------------------|------------|--------------|
| Juanante Rodriguez, Josfer | u202214778 | 3            |
| Morales Oliveros, Tarik    | u202210472 | 0            |
| Palomino Mayta, Luis       | U202111111 | 0            |
| Vilchez Marin, Rody        | U202216562 | 0            |

Introducción 

El Problema del Agente Viajero (PAV) es un desafío clásico en el campo de la optimización combinatoria y la teoría de la computación. Este problema involucra a un agente (o viajero) que debe visitar un conjunto de ciudades exactamente una vez, regresando al punto de partida, minimizando la distancia total recorrida. El PAV tiene aplicaciones prácticas en la planificación de rutas, la logística, el diseño de circuitos, y diversas áreas de la ingeniería y la ciencia de la computación.

El PAV presenta un escenario altamente desafiante debido a su naturaleza combinatoria, donde la cantidad de posibles soluciones crece de manera exponencial con el número de ciudades. A medida que se agregan más ciudades al problema, encontrar la solución óptima se convierte en una tarea computacionalmente costosa. Este problema ha motivado la creación y desarrollo de diversas técnicas y algoritmos de optimización.

En este informe, se presenta un programa implementado en Python que resuelve el problema del agente viajero, a partir de una matriz simétrica.  Para ejecutar el programa se debe instalar los paquetes de tkinter, random, networkx y matplotlib, con la finalidad de generar una interfaz de usuarios donde el usuario pueda interactuar con dicho programa. 

Al finalizar el proyecto, la herramienta desarrollada para abordar el Problema del Agente Viajero (PAV) proporciona una herramienta eficiente para calcular rutas óptimas. Estas aplicaciones prácticas pueden tener un impacto significativo en la eficiencia y la toma de decisiones en una variedad de contextos.

## Objetivos

1. **Desarrollar un programa informático que resuelva el problema del agente viajero** 
2. **Facilitar la planificación de rutas óptimas:** 
3. **Validar el programa mediante ejemplos y casos de estudio** 
4. ** Proporcionar una Interfaz intuitiva y amigable:** 

## Aplicaciones 
El problema del agente viajero se aplica en diversos campos debido a su funcionalidad de optimización.A continuación se detallan algunas aplicaciones: . 


1. **Logística y Distribución:** El PAV se utiliza para optimizar las rutas de entrega de vehículos, minimizando la distancia recorrida. Esto ahorra costos de combustible y tiempo.
El artículo de Laporte proporciona una visión general de los algoritmos utilizados en la resolución del PAV, destacando su aplicación en logística y distribución.

2. **Planificación de Circuitos Integrados:** En la industria de semiconductores, el PAV se aplica para planificar rutas de máquinas que conectan puntos en circuitos integrados, minimizando la longitud de los cables y mejorando la eficiencia.
 El artículo de Paterson se centra en la aplicación del PAV en la planificación de circuitos integrados, demostrando su relevancia en la industria de semiconductores.

3. **Optimización de Rutas de Vehículos:** Además de la logística, el PAV se aplica en la optimización de rutas de vehículos en campos como el transporte público, la gestión de flotas y la planificación de viajes.
 El libro de Toth y Vigo proporciona una visión completa de la aplicación del PAV en la optimización de rutas de vehículos, con enfoque en problemas reales y métodos de resolución.

4. **Secuenciación de ADN:** En bioinformática, el PAV se utiliza para determinar el orden óptimo de secuenciación de fragmentos de ADN en la secuenciación de genomas, fundamental para la genómica y la medicina.
 El artículo de Pevzner y colaboradores presenta un enfoque innovador para la secuenciación de ADN basado en el PAV, destacando su importancia en la genómica.

5. **Planificación de Circuitos de PCB:** En electrónica, el PAV se aplica a la planificación de rutas de pistas en circuitos impresos (PCB), minimizando la longitud de las conexiones eléctricas.
El libro de Hachtel y Somenzi aborda la aplicación del PAV en la planificación de PAV desde una perspectiva de diseño electrónico.

6. **Optimización de Viajes Turísticos:** En el turismo, el PAV se utiliza para diseñar rutas turísticas que visiten múltiples destinos de manera eficiente, ahorrando tiempo y recursos.
El libro de Applegate y colaboradores ofrece una guía completa sobre la aplicación del PAV en la optimización de viajes turísticos, destacando su utilidad en el sector del turismo.

Estas aplicaciones del PAV en diversos campos muestran su versatilidad y relevancia en la resolución de problemas de optimización relacionados con la planificación de rutas y secuenciación. 




## Problema:
>Dado n ∈ [5, 15] ingresado por el usuario, el programa debe generar
aleatoriamente una matriz simétrica n × n (con elementos positivos) o
solicitar el ingreso de cada elemento de la matriz (según decisión del
usuario). Además, debe calcular y mostrar un ciclo hamiltoniano que
minimice la distancia total de la ruta o el tiempo total del recorrido.


                             OCUTBRE 2023
