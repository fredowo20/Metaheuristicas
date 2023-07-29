# Tarea 1

El objetivo de esta tarea es plantear la resolución de un Nonograma como un Problema de Satisfacción de Restricciones (CSP), implementar el algoritmo de Forward Checking para resolverlo y comparar los resultados obtenidos con una heurística de selección de variable. 

![nonogram](https://github.com/fredowo20/Metaheuristicas/assets/103700122/cd4a6475-585a-41af-9b1b-5069c02e939a)

## Resolución del Nonograma como un CSP

- Variables: Cada celda del tablero representa una variable, las cuales pueden ser representadas como X_ij, donde i es el índice de la fila y j es el índice de la columna.

- Dominio: Cada celda puede estar en uno de dos estados: {0,1}, donde 0 representa un recuadro en blanco o no pintado y 1 un cuadrado pintado.

- Restricciones: Las restricciones son las mismas para filas y columnas, para cada una de estas se debe seguir una lista de pistas que representan el número y longitud de secuencias que deben ser marcadas de forma consecutiva.
Entre las secuencias de celdas marcadas consecutivas en una fila o columna debe haber al menos una celda no marcada. Además, para cada secuencia de celdas marcadas consecutivas en una columna, la suma de los valores de las variables correspondientes a esas celdas debe ser igual a la longitud de la secuencia.

## Comparación de resultados obtenidos de ambas estrategias respecto a los nodos generados y el tiempo de CPU

Ambos códigos resuelven el nonograma indicado inicialmente utilizando la técnica de Forward Checking. Sin embargo, el segundo código también utiliza una heurística adicional de selección de variable basada en el menor dominio. Luego de ejecutar ambos códigos, se presentan los siguientes casos respectivamente:

![nonogram1](https://github.com/fredowo20/Metaheuristicas/assets/103700122/2ecab6ce-17da-4860-a60b-a9ab75bdef72)
![nonogram2](https://github.com/fredowo20/Metaheuristicas/assets/103700122/e23418b9-b45a-464d-9377-3721b4820216)

En donde se puede observar que la segunda técnica, que utiliza forward checking junto con la heurística de selección variable "menor dominio", ha generado menos nodos (91) en comparación con la primera técnica (100) que solo utiliza Forward Checking. Esto indica que la segunda técnica es más eficiente en términos de la cantidad de nodos generados, lo que podría resultar en un menor tiempo de ejecución y una mayor rapidez en la resolución del nonograma.

Por lo tanto, para analizar el tiempo de CPU de ambos códigos se realizan múltiples ejecuciones. Esto permitirá obtener un promedio confiable que refleje el rendimiento real de los códigos en términos de eficiencia temporal. Se registraron los tiempos de ejecución de cada código en cada iteración, y se calculó el promedio para tener una visión más precisa de su desempeño, lo cual arroja los resultados mostrados a continuación.

![nonogram_table](https://github.com/fredowo20/Metaheuristicas/assets/103700122/0108effe-ea4c-483c-ac8a-ee96608a26c0)

Se puede observar que el tiempo promedio de CPU de la segunda técnica es de 61.1411 segundos, el cual es menor en comparación con el tiempo promedio de CPU de la primera técnica, obteniendo en esta última 61.7747 segundos. Esto indica que la segunda técnica, además de ser más eficiente respecto a los nodos generados, también es más rápida en términos de tiempo de CPU requerido para resolver el nonograma. Sin embargo, cabe destacar que la diferencia en tiempos de ejecución entre ambos enfoques es mínima.

En algunos casos se pudo ver que la técnica que solo utiliza Forward Checking resultó ser más rápida que la técnica de Forward Checking con la heurística de selección de variable basada en el menor dominio, lo cual se puede deber a que la técnica Look-Ahead utilizada no garantiza seguir siempre el mismo árbol de búsqueda para resolver un problema. Forward Checking trabaja de forma incremental, asignando valores de variables, en donde estos valores que se asignan en cada paso pueden influir en el árbol de búsqueda generado y en la eficiencia del algoritmo. El segundo algoritmo utiliza la heurística de selección variable de "menor dominio”. Esta selecciona la variable con el dominio más pequeño como próxima variable a asignar. En el caso de que exista más de una variable que tenga el mismo tamaño, la heurística no especifica el orden en que se deben seleccionar, lo que puede causar variaciones en el orden en que se asignan entre las diferentes ejecuciones del código.

Por lo mencionado anteriormente, para determinar con certeza que el segundo algoritmo creado es más eficiente en términos de tiempo en la resolución del nonograma, es necesario utilizar un problema más grande para así obtener diferencias de tiempo más notables. También es importante tener en cuenta que ambos códigos no necesariamente seguirán el mismo árbol de búsqueda cada vez que se ejecuten, lo cual es el motivo de que se tuvieran diferentes tiempos de CPU en las distintas ejecuciones que se realizaron.  

La hipótesis inicial fue que la heurística utilizada en la segunda técnica, "menor dominio", ayudaría a reducir el tiempo de ejecución en comparación con la primera técnica que no utiliza ninguna heurística adicional, debido a que la cantidad de nodos generados puede ser disminuída (como fue en este caso), y  Forward Checking no considera el dominio al momento de elegir la siguiente variable a asignar, resultando en una mayor cantidad de nodos que se exploran. Sin embargo, a partir de los resultados obtenidos de los experimentos realizados, se puede concluir que si un algoritmo reduce la cantidad de nodos que genera, no necesariamente va a disminuir el tiempo de ejecución.

Al utilizar la técnica de “menor dominio”, se puede generar una eficiencia en el recorrido de las ramas del árbol de búsqueda, debido a que esta técnica elige la variable con menor dominio, lo cual provocaría una mayor probabilidad de encontrar restricciones, implicando así que la cantidad de nodos disminuya. Por lo tanto, en este caso fue más eficiente utilizar una heurística de selección variable en conjunto con Forward Checking, ya que redujo la cantidad de opciones a explorar en cada nivel del árbol de búsqueda y, con esto, la cantidad de nodos generados.
