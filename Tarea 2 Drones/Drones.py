import numpy as np

benchmark = 't2_Titan.txt' # tiempo inicial 100
# benchmark = 't2_Europa.txt' # tiempo inicial 0 
# benchmark = 't2_Deimos.txt' # tiempo inicial 900
initial_time = 100
seed = 0

def fix_txt(fileName):
    with open(fileName) as f:
        lines = f.readlines()

    new_lines = []
    prev_line_length = -1

    for line in lines:
        line_length = len(line.strip().split())
        if line_length == 1:
            new_lines.append(line)
        elif line_length == 3:
            if prev_line_length != 3 and prev_line_length != 1:
                new_lines.append("\n")
            new_lines.append(line.strip())
            new_lines.append("\n")
        else:
            new_lines[-1] += line.strip() + " "
        prev_line_length = line_length

    with open(fileName, "w") as f:
        f.writelines(new_lines)

def read_file(fileName):
    with open(fileName, 'r') as f:
        droneQuantity = int(f.readline().strip())
        droneSpacing = []
        droneTimes = []
        for i in range(droneQuantity*2):
            linea = f.readline().strip().split()
            if len(linea) != 3:
                droneSpacing.append(list(map(int, linea)))
            else:
                droneTimes.append(list(map(int, linea)))
        return droneQuantity, droneSpacing, droneTimes

def print_solution(landingTimes, currentCost, assignedDrones):
    print("Tiempos de aterrizaje: ", landingTimes)
    print("Orden de aterrizaje de los drones: ", assignedDrones)
    print("Costo total: ", currentCost)
    print("\n")

fix_txt(benchmark)
droneQuantity, droneSpacing, droneTimes = read_file(benchmark)
tabuListSize = int(droneQuantity*0.2) # Tamaño de la lista tabú del 20% de la cantidad de drones

def costForGreedy(prefTimes, available, droneIndex):
    # Buscar en la lista de tuplas el tiempo preferente del dron
    for tupla in prefTimes:
        if(tupla[1] == droneIndex):
            # Calcular el costo
            cost = abs(tupla[0]-available) 
    return cost

def totalCost(assignedDrones, prefTimes, droneSpacing, initial_time, constraintsTimes):
    # Inicializar la lista de tiempos de aterrizaje, lista de índices de drones con solución factible y una variable de nuevo costo
    factibleAssignedDrones = []
    newLandingTimes = []
    costNewAssignedDrones = 0

    # Iterar hasta que se calcule el nuevo costo total
    for i in range(len(assignedDrones)):
        # Buscar la tupla del drone (en la posición 0 está el tiempo preferente y en la posición 1 el id del drone)
        tuplaNewAssignedDrones = list(filter(lambda x: x[1] == assignedDrones[i], prefTimes))[0]
        currentTime = tuplaNewAssignedDrones[0]

        if len(newLandingTimes) > 0:
            assignedTime = newLandingTimes[-1]
            spacing = droneSpacing[assignedDrones[i-1]][assignedDrones[i]]
            currentTime = max(currentTime, assignedTime + spacing)
        # Primer dron
        else:
            #Asignar tiempo inicial
            currentTime = initial_time
        # Si el tiempo pref del dron es mayor al tiempo actual, se espera al tiempo pref para evitar penalización (solo para el primer caso)
        if tuplaNewAssignedDrones[0] >= currentTime and len(newLandingTimes) == 0:
            factibleAssignedDrones.append(tuplaNewAssignedDrones[1])
            newLandingTimes.append(tuplaNewAssignedDrones[0])
         # Si el tiempo pref del dron es mayor al tiempo actual, se espera al tiempo pref para evitar penalización, sólo se puede asignar si la solución es factible
        elif tuplaNewAssignedDrones[0] >= currentTime and verifyFeasibleSolution(constraintsTimes, currentTime, tuplaNewAssignedDrones[1]):
            factibleAssignedDrones.append(tuplaNewAssignedDrones[1])
            newLandingTimes.append(tuplaNewAssignedDrones[0])
        # Si el tiempo de aterrizaje del dron es menor al tiempo actual se penaliza, sólo se puede asignar si la solución es factible
        elif tuplaNewAssignedDrones[0] < currentTime and verifyFeasibleSolution(constraintsTimes, currentTime, tuplaNewAssignedDrones[1]):
            factibleAssignedDrones.append(tuplaNewAssignedDrones[1])
            costNewAssignedDrones += abs(tuplaNewAssignedDrones[0] - currentTime)
            newLandingTimes.append(currentTime)

    return costNewAssignedDrones, newLandingTimes, factibleAssignedDrones

def verifyFeasibleSolution(constraintsTimes, availableTime, droneIndex):
    # Comprbar que el tiempo actual está dentro de los rangos de aterrizaje del drone
    feasibleTimeInterval = list(filter(lambda tripletas: droneIndex in tripletas, constraintsTimes))
    return True if availableTime >= feasibleTimeInterval[0][0] and availableTime <= feasibleTimeInterval[0][1] else False

def deterministic_greedy(droneSpacing, droneTimes, initial_time):
    # Obtener el número de drones
    numDrones = len(droneTimes)
    # Inicializar variable para costo
    totalCost = 0
    
    # Crear una lista de tuplas con los tiempos preferentes de aterrizaje y los índices de los drones
    prefTimes = [(droneTimes[i][1], i) for i in range(numDrones)]
    
    # Ordenar la lista de preferencias de aterrizaje por orden ascendente de tiempo preferente
    prefTimes.sort()
    
    # Inicializar la lista de tiempos de aterrizaje y la lista de drones asignados
    landingTimes = []
    assignedDrones = []
    
    # Iterar sobre cada drone por orden de preferencia
    for prefTime, droneIndex in prefTimes:
        # Obtener los tiempos de aterrizaje temprano, preferente y tardío del drone
        earlyTime, preferentialTime, lateTime = droneTimes[droneIndex]
        availableTime = preferentialTime

        if len(assignedDrones) > 0:
            # Obtener el tiempo en el que aterrizó el último drone
            assignedTime = landingTimes[-1]
            # Obtener el tiempo de separación requerido entre los drones
            spacing = droneSpacing[assignedDrones[-1]][droneIndex]
            # Actualizar el tiempo de aterrizaje más temprano disponible, se compara el tiempo de aterrizaje del último drone con el tiempo preferente del dron que aterrizará
            availableTime = max(availableTime, assignedTime + spacing)
        # Primer dron
        else:
            #Asignar tiempo inicial
            availableTime = initial_time

        # Si el tiempo pref del dron es mayor al tiempo actual, se espera al tiempo pref para evitar penalización
        if prefTime >= availableTime:
            landingTimes.append(prefTime)
            assignedDrones.append(droneIndex)
        # Si el tiempo de aterrizaje del dron es menor al tiempo actual se penaliza
        else:
            mincost = costForGreedy(prefTimes, availableTime, droneIndex)
            totalCost +=  mincost
            assignedDrones.append(droneIndex)
            landingTimes.append(availableTime)

    return landingTimes, totalCost, assignedDrones

def stochastic_greedy(droneSpacing, droneTimes, initial_time, seed):
    #Random seed
    np.random.seed(seed)
    
    # Obtener el número de drones
    numDrones = len(droneTimes)
    # Inicializar variable para costo
    totalCost = 0
    
    # Crear una lista de tuplas con los tiempos preferentes de aterrizaje y los índices de los drones
    prefTimes = [(droneTimes[i][1], i) for i in range(numDrones)]
    prefTimes = np.array(prefTimes, dtype=[('x', int), ('y', int)])
    
    # Crear una lista que solo contenga los Ids de los drones
    valuesDrone = prefTimes['y']

    # Inicializar la lista de tiempos de aterrizaje y la lista de drones asignados
    landingTimes = []
    assignedDrones = []

    # Iterar sobre cada drone
    for prefTime, droneIndex in prefTimes:
        # Otorgar una probabilidad a cada uno de los drones
        probs = np.exp(0.01*(valuesDrone - np.min(valuesDrone)))
        # Normalizar los probabilidades
        probs /= np.sum(probs)
        # Escoger al azar un drone (random seed)
        roulette = np.random.choice(valuesDrone, p = probs)

        # Buscar el dron escogido en la lista de tuplas
        for tupla in prefTimes:
            if tupla[1] == roulette:
                # Obtener el tiempo preferente del drone escogido (roulette)
                availableTime = tupla[0]
                if len(assignedDrones) > 0:
                    # Obtener el tiempo en el que aterrizó el último drone
                    assignedTime = landingTimes[-1]
                    # Obtener el tiempo de separación requerido entre los drones
                    spacing = droneSpacing[assignedDrones[-1]][tupla[1]]
                    # Actualizar el tiempo de aterrizaje más temprano disponible, se compara el tiempo de aterrizaje del último drone con el tiempo preferente del dron escogido (roulette)
                    availableTime = max(availableTime, assignedTime + spacing)
                # Primer dron
                else:
                    #Asignar tiempo inicial
                    availableTime = initial_time

                # Si el tiempo preferente del dron es mayor al tiempo actual, se espera al tiempo pref para evitar penalización     
                if tupla[0] >= availableTime:
                    landingTimes.append(tupla[0])
                    assignedDrones.append(tupla[1])   
                # Si el tiempo de aterrizaje del dron es menor al tiempo actual se penaliza
                else:
                    mincost = costForGreedy(prefTimes, availableTime, tupla[1])
                    totalCost +=  mincost
                    assignedDrones.append(tupla[1]) 
                    landingTimes.append(availableTime)
        
        # Eliminar el drone escogido (roulette) para eliminar su probabilidad de selección
        valuesDrone = np.delete(valuesDrone, np.where(valuesDrone == roulette))

    return landingTimes, totalCost, assignedDrones

def simple_hill_climbing(droneTimes, landingTimes, assignedDrones, totalCostGreedy, droneSpacing, initial_time):
    # Establecer el costo obtenido con el Greedy como costo actual
    currentCost = totalCostGreedy
    # Crear una lista de tuplas con los tiempos preferentes de aterrizaje y los índices de los drones
    prefTimes = [(droneTimes[i][1], i) for i in range(len(assignedDrones))]
    # Crear una lista de tripletas con los tiempos mínimos y máximos de aterrizaje, con su respectivo índice de drone
    constraintsTimes = [(droneTimes[i][0], droneTimes[i][2], i) for i in range(len(droneTimes))]

    # Iterar en las nuevas soluciones generadas modificando el vecindario
    for i in range(len(assignedDrones) - 1):
        newassignedDrones = assignedDrones.copy()
        # Intercambiar los tiempos de aterrizaje de drones consecutivos
        newassignedDrones[i], newassignedDrones[i+1] = newassignedDrones[i+1], newassignedDrones[i]
        # Calcular el costo con el nuevo orden de llegada de los drones y la lista de índices de drones actualizados (aquellos que cumplan con la restricción de tiempo)
        newCost,  newLandingTimes, newassignedDrones = totalCost(newassignedDrones, prefTimes, droneSpacing, initial_time, constraintsTimes)
        
        # Si el nuevo costo es mejor que el anterior se realiza el cambio
        if newCost < currentCost and newCost != 0:
            assignedDrones = newassignedDrones
            landingTimes = newLandingTimes
            currentCost = newCost
            break

    return landingTimes, currentCost, assignedDrones

def steepest_ascent_hill_climbing(droneTimes, landingTimes, assignedDrones, totalCostGreedy, droneSpacing, initial_time):
    # Inicializar variable que enumera las iteraciones que se realizan para luego implementarlas en el Tabú Search
    iterations = 0
    # Establecer el costo obtenido con el Greedy como costo actual
    currentCost = totalCostGreedy
    # Crear una lista de tuplas con los tiempos preferentes de aterrizaje y los índices de los drones
    prefTimes = [(droneTimes[i][1], i) for i in range(len(assignedDrones))]
    # Crear una lista de tripletas con los tiempos mínimos y máximos de aterrizaje, con su respectivo índice de drone
    constraintsTimes = [(droneTimes[i][0], droneTimes[i][2], i) for i in range(len(droneTimes))]

    # Iterar hasta que exista la mejor mejora
    while True:
        iterations+=1
        for i in range(len(assignedDrones) - 1):
            newassignedDrones = assignedDrones.copy()
            # Intercambiar los tiempos de aterrizaje de drones consecutivos
            newassignedDrones[i], newassignedDrones[i+1] = newassignedDrones[i+1], newassignedDrones[i]
            # Calcular el costo con el nuevo orden de llegada de los drones y la lista de índices de drones actualizados (aquellos que cumplan con la restricción de tiempo)
            newCost,  newLandingTimes, newassignedDrones = totalCost(newassignedDrones, prefTimes, droneSpacing, initial_time, constraintsTimes)

            # Si el nuevo costo es mejor que el anterior se realiza el cambio
            if newCost < currentCost and newCost != 0:
                assignedDrones = newassignedDrones
                landingTimes = newLandingTimes 
                currentCost = newCost
                break
        # Si no existen mejores mejoras salir del ciclo
        else:
            break

    return landingTimes, currentCost, assignedDrones, iterations

def tabu_search(droneTimes, landingTimes, assignedDrones, totalCostGreedy, droneSpacing, tabuListSize, iterations, initial_time):
    currentCost = totalCostGreedy
    prefTimes = [(droneTimes[i][1], i) for i in range(len(assignedDrones))]
    constraintsTimes = [(droneTimes[i][0], droneTimes[i][2], i) for i in range(len(droneTimes))]
    
    # Lista Tabú para almacenar movimientos prohibidos
    tabuList = []  
    # inicializar la mejor solución actual y el mejor costo
    bestSolution = landingTimes.copy()
    bestCost = currentCost
    
    # Iterar en las nuevas soluciones generadas modificando el vecindario
    for _ in range(iterations):
        bestNeighbor = None
        bestNeighborCost = float('inf')
        bestNeighborDrones = assignedDrones.copy()
        
        for i in range(len(assignedDrones) - 1):
            newassignedDrones = assignedDrones.copy()
            # Intercambiar los tiempos de aterrizaje de drones consecutivos
            newassignedDrones[i], newassignedDrones[i+1] = newassignedDrones[i+1], newassignedDrones[i]
            # Calcular el costo con el nuevo orden de llegada de los drones y la lista de indices de drones actualizados (aquellos que cumplan con la restricción de tiempo)
            newCost, newLandingTimes, newassignedDrones = totalCost(newassignedDrones, prefTimes, droneSpacing, initial_time, constraintsTimes)

            # Verificar si el movimiento mejora la mejor solución anterior y no esté en la tabu list
            if newCost < bestNeighborCost and newassignedDrones not in tabuList and newCost != 0:
                bestNeighbor = newLandingTimes
                bestNeighborCost = newCost
                bestNeighborDrones = newassignedDrones
        
        # Actualizar la solución actual con la mejor solución vecina encontrada
        if bestNeighbor:
            assignedDrones = bestNeighborDrones
            landingTimes = bestNeighbor
            currentCost = bestNeighborCost
            # Agregar el movimiento a la lista Tabú
            tabuList.append(newassignedDrones)  
            
            # Mantener el tamaño de la lista Tabú dentro del tamaño establecido
            if len(tabuList) > tabuListSize:
                # Eliminar el movimiento más antiguo de la lista Tabú
                tabuList.pop(0)  
            
            # Actualizar la mejor solución
            if bestNeighborCost < bestCost:
                bestSolution = bestNeighbor
                bestCost = bestNeighborCost
                # Actualizar assignedDrones con los drones de la mejor solución vecina
                assignedDrones = bestNeighborDrones

    return bestSolution, bestCost, assignedDrones

landingTimes_deterministic_greedy, totalCost_deterministic_greedy, assignedDrones_deterministic_greedy = deterministic_greedy(droneSpacing, 
                                                                                                                              droneTimes, 
                                                                                                                              initial_time)
print("GREEDY DETERMINÍSTICO")
print_solution(landingTimes_deterministic_greedy, totalCost_deterministic_greedy, assignedDrones_deterministic_greedy)

landingTimes_stochastic_greedy, totalCost_stochastic_greedy, assignedDrones_stochastic_greedy = stochastic_greedy(droneSpacing, 
                                                                                                                  droneTimes, 
                                                                                                                  initial_time,
                                                                                                                  seed)
print("GREEDY ESTOCÁSTICO")
print_solution(landingTimes_stochastic_greedy, totalCost_stochastic_greedy, assignedDrones_stochastic_greedy)

landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing = simple_hill_climbing(droneTimes, 
                                                                                                           landingTimes_deterministic_greedy, 
                                                                                                           assignedDrones_deterministic_greedy, 
                                                                                                           totalCost_deterministic_greedy, 
                                                                                                           droneSpacing, 
                                                                                                           initial_time)
print("HILL CLIMBING ALGUNA-MEJORA (Greedy Determinístico)")
print_solution(landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing)

landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing, iterations = steepest_ascent_hill_climbing(droneTimes, 
                                                                                                                                landingTimes_deterministic_greedy, 
                                                                                                                                assignedDrones_deterministic_greedy, 
                                                                                                                                totalCost_deterministic_greedy, 
                                                                                                                                droneSpacing, 
                                                                                                                                initial_time)
print("HILL CLIMBING MEJOR-MEJORA (Greedy Determinístico)")
print_solution(landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing)

landingTimes_tabu_search, currentCost_tabu_search, assignedDrones_tabu_search, = tabu_search(droneTimes, 
                                                                                             landingTimes_deterministic_greedy, 
                                                                                             assignedDrones_deterministic_greedy, 
                                                                                             totalCost_deterministic_greedy, 
                                                                                             droneSpacing, 
                                                                                             tabuListSize, 
                                                                                             iterations, 
                                                                                             initial_time)
print("TABU SEARCH (Greedy Determinístico)")
print_solution(landingTimes_tabu_search, currentCost_tabu_search, assignedDrones_tabu_search)

landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing = simple_hill_climbing(droneTimes, 
                                                                                                           landingTimes_stochastic_greedy, 
                                                                                                           assignedDrones_stochastic_greedy, 
                                                                                                           totalCost_stochastic_greedy, 
                                                                                                           droneSpacing, 
                                                                                                           initial_time) 
print("HILL CLIMBING ALGUNA-MEJORA (Greedy Estocástico)")
print_solution(landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing)

landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing, iterations = steepest_ascent_hill_climbing(droneTimes, 
                                                                                                                                landingTimes_stochastic_greedy, 
                                                                                                                                assignedDrones_stochastic_greedy, 
                                                                                                                                totalCost_stochastic_greedy, 
                                                                                                                                droneSpacing, 
                                                                                                                                initial_time)
print("HILL CLIMBING MEJOR-MEJORA (Greedy Estocástico)")
print_solution(landingTimes_hill_climbing, currentCost_hill_climbing, assignedDrones_hill_climbing)

landingTimes_tabu_search, currentCost_tabu_search, assignedDrones_tabu_search, = tabu_search(droneTimes, 
                                                                                             landingTimes_stochastic_greedy, 
                                                                                             assignedDrones_stochastic_greedy, 
                                                                                             totalCost_stochastic_greedy, 
                                                                                             droneSpacing, 
                                                                                             tabuListSize, 
                                                                                             iterations,
                                                                                             initial_time)
print("TABU SEARCH (Greedy Estocástico)")
print_solution(landingTimes_tabu_search, currentCost_tabu_search, assignedDrones_tabu_search)