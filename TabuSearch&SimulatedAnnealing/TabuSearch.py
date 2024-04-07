import random
import time


def read_input(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            nr_object = lines[0]
            values = []
            weights = []
            for line in lines[1:-1]:
                parts = line.split()
                values.append(int(parts[1]))
                weights.append(int(parts[2]))
            knapsack_weight = int(lines[-1])
        return nr_object, values, weights, knapsack_weight
    except FileNotFoundError:
        print("File not found.")
        return None


def init_tabu_memory(current_solution):
    return [0] * len(current_solution)


def update_memory(memory, index, k_tabu):
    for i in range(len(memory)):
        if i == index:
            memory[i] = k_tabu
        elif memory[i] != 0:
            memory[i] = memory[i] - 1
    return memory


def calculate_fitness_or_weights(solution, used_list):
    return sum(solution[i] * used_list[i] for i in range(len(used_list)))


def best_non_tabu_n(current_solution, values, weights, knapsack_weight, memory):
    index = 0
    best_neighbour = []
    best_neighbour_value = -1

    for j in range(0, len(current_solution)):
        if memory[j] == 0:
            neighbour = current_solution[:]
            neighbour[j] = 1 - neighbour[j]

            neighbour_value = calculate_fitness_or_weights(neighbour, values)
            neighbour_weight = calculate_fitness_or_weights(neighbour, weights)

            if neighbour_weight <= knapsack_weight:
                if neighbour_value > best_neighbour_value:
                    best_neighbour = neighbour[:]
                    best_neighbour_value = neighbour_value
                    index = j
    return best_neighbour, best_neighbour_value, index


def tabu_search(k, k_tabu, weights, values, knapsack_weight):
    while True:
        random_solution = [random.randint(0, 1) for _ in range(len(weights))]
        if calculate_fitness_or_weights(random_solution, weights) <= knapsack_weight:
            break

    current_solution = random_solution[:]
    memory = init_tabu_memory(current_solution)
    best_solution = current_solution[:]
    best_val = calculate_fitness_or_weights(best_solution, values)

    for _ in range(k):

        neighbour, neighbour_value, index = best_non_tabu_n(current_solution, values, weights, knapsack_weight, memory)
        memory = update_memory(memory, index, k_tabu)
        if neighbour_value > best_val:
            best_solution = neighbour[:]
            best_val = neighbour_value

        current_solution = neighbour[:]
    return best_solution, best_val


def main():
    while True:
        average_time = 0
        best_value_global = 0
        average_value = 0
        best_list = []
        file_path = input("Enter the file path you want to use: ")
        if file_path:
            input_data = read_input(file_path)
            if input_data is None:
                return
            nr_object, values, weights, knapsack_weight = input_data
        else:
            values, weights, knapsack_weight = [10, 20, 30, 40, 50], [1, 2, 3, 4, 5], 10
        k = int(input("Enter the number of iterations you want to use for algorithms: "))
        k_tabu = int(input("Enter the number of iterations tabu you want to use for algorithms: "))
        num_runs = 10
        for _ in range(num_runs):
            start_time = time.time()
            best_solution, best_val = tabu_search(k, k_tabu, weights, values, knapsack_weight)
            time_stamp = time.time() - start_time
            print("Time stamp:", time_stamp)
            average_time += time_stamp
            print("Best solution:", best_solution)

            print("Best fitness:", best_val)
            if best_val > best_value_global:
                best_value_global = best_val
                best_list = best_solution
            average_value += best_val
        average_time /= num_runs

        print("The maximum value is: ", best_value_global)
        print("The average value is: ", average_value // num_runs)
        print("The best solution is: ", best_list)
        print("Average time is:", average_time, "seconds", "\n\n")


if __name__ == '__main__':
    main()
