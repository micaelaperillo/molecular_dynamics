# molecular_dynamics

## Predicción de Eventos

### Colisión con el recinto circular:  
Una colisión ocurre cuando la trayectoria de la partícula intersecta el círculo: 
$x^2 + y^2 = R_e^2$ \
Dada la posición actual de la partícula $(r_{xi}, r_{yi})$ y su velocidad $(v_{xi}, v_{yi})$.\
La posición futura en el tiempo $t + \Delta t$ es: $(r_{xi} + v_{xi} \cdot \Delta t,\ r_{yi} + v_{yi} \cdot \Delta t)$ \
Al sustituir en la ecuación del círculo da lugar a una ecuación cuadrática en $\Delta t$.  
Resolvemos para $\Delta t > 0$ y seleccionamos la raíz positiva más pequeña.

### Colisión con el obstáculo fijo:
De manera similar al anterior, se busca cuando la partícula intersecta: $x^2 + y^2 = R_o^2$. \
Utilizamos el mismo método: sustituimos la posición futura en la ecuación, resolvemos la cuadrática para $\Delta t > 0$, y elegimos la solución positiva más pequeña.

### Colisión con otra partícula:  
Para cada par de partículas $i$ y $j$ con posiciones $(r_{xi}, r_{yi})$, $(r_{xj}, r_{yj})$ y velocidades $(v_{xi}, v_{yi})$, $(v_{xj}, v_{yj})$, 
calculamos cuándo la distancia entre los centros es igual a $2r$: \
$\| \vec{r}_i(t + \Delta t) - \vec{r}_j(t + \Delta t) \| = 2r$ \
Esto lleva a una ecuación cuadrática en $\Delta t$. Resolvemos y seleccionamos la raíz positiva más pequeña.


**Mantener una cola de prioridad** con todos los eventos de colisión predichos, ordenados por el tiempo de ocurrencia.
Cada evento debe incluir:
- El tiempo de colisión
- El tipo de colisión (recinto, obstáculo, o partícula-partícula)
- Las partículas involucradas
