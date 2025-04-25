# Event Driven Molecular Dynamics

Este proyecto simula un sistema molecular bidimensional donde partículas se mueven dentro de un contenedor circular y colisionan elásticamente entre sí, con las paredes del contenedor y, opcionalmente, con un obstáculo fijo en el centro. La simulación permite estudiar el comportamiento dinámico del sistema y calcular la presión ejercida por las partículas.

## Parámetros

- `particlesAmount`: cantidad total de partículas que se van a simular dentro del recinto.

- `particlesSpeed`: velocidad inicial de todas las partículas.

- `particlesRadius`: radio de cada partícula.

- `maxSimulationTime`: tiempo máximo que va a durar la simulación (en segundos).

- `obstaclePresent`: indica si hay o no un obstáculo fijo en el centro del contenedor (booleano: true o false).