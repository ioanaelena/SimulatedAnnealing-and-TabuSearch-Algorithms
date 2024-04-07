import math
import random
import numpy as np
import time


def read_tsp_file(file_path):
    nodes = {}
    with open(file_path, 'r') as file:
        start_processing = False
        for line in file:
            if line.strip() == 'NODE_COORD_SECTION':
                start_processing = True
                continue
            if start_processing:
                parts = line.split()
                if len(parts) == 3:
                    node = int(parts[0])
                    x_coord = int(parts[1])
                    y_coord = int(parts[2])
                    nodes[node] = (x_coord, y_coord)
    return nodes


def create_distance_matrix(nodes):
    num_nodes = len(nodes)
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            x1, y1 = nodes[i + 1]  # Nodes start from index 1
            x2, y2 = nodes[j + 1]
            distance_matrix[i][j] = int(round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))
    return distance_matrix


def get_fitness(current_list, distance_matrix):
    total_distance = 0
    num_nodes = len(current_list)
    for i in range(num_nodes - 1):
        total_distance += distance_matrix[current_list[i] - 1][current_list[i + 1] - 1]
    total_distance += distance_matrix[current_list[-1] - 1][current_list[0] - 1]
    return total_distance


def two_opt(state):
    pos_one = random.choice(range(len(state)))
    pos_two = random.choice(range(len(state)))
    start_index = min(pos_one, pos_two)
    end_index = max(pos_one, pos_two)
    state[start_index:end_index+1] = list(reversed(state[start_index:end_index+1]))
    return state


def simulated_annealing_algorithm(k, temperature, min_t, alpha, distance_matrix):
    num_nodes = len(distance_matrix)
    current_solution = np.random.permutation(num_nodes) + 1  # Generate a random permutation of nodes
    while temperature > min_t:
        for _ in range(k):
            neighbor_list = two_opt(current_solution.copy())
            delta = get_fitness(neighbor_list, distance_matrix) - get_fitness(current_solution, distance_matrix)
            if delta < 0:
                current_solution = neighbor_list
            elif random.random() < math.exp(float(-delta / temperature)):
                current_solution = neighbor_list
        temperature = alpha * temperature
    return current_solution


def main():
    file_path = 'rat99.tsp'
    nodes = read_tsp_file(file_path)
    distance_matrix = create_distance_matrix(nodes)
    num_runs = 10
    average_time = 0
    average_value = 0
    best_list = []
    best_value_global = 10000
    iterations = int(input("Alegi numarul de iteratii: "))
    initial_temp = int(input("Alegeti temperatura initiala: "))
    min_t = int(input("Alegeti temperatura de oprire: "))
    alpha = float(input("Alegeti rata de racire: "))
    for _ in range(num_runs):
        start_time = time.time()
        best_solution = simulated_annealing_algorithm(iterations, initial_temp, min_t, alpha, distance_matrix)
        time_stamp = time.time() - start_time
        print("Time stamp:", time_stamp)
        average_time += time_stamp
        print("Best solution:", best_solution)
        best_fitness = get_fitness(best_solution, distance_matrix)
        print("Best fitness:", best_fitness)
        if best_fitness < best_value_global:
            best_value_global = best_fitness
            best_list = best_solution
        average_value += best_fitness
    average_time /= num_runs  # calculez timpul mediu de executie pentru numarul de executii

    print("Valoarea minima globala este: ", best_value_global)
    print("Valoarea medie globala este: ", average_value // num_runs)
    print("Solutia cea mai buna globala este: ", best_list)
    print("Timpul mediu de execuție este:", average_time, "secunde", "\n\n")


if __name__ == '__main__':
    main()
