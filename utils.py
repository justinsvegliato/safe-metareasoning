import copy
import json
import logging
import os
import random
from itertools import chain, combinations

from solvers import safety_process_solver, task_process_solver

GAMMA = 0.99
POLICY_CACHE_DIRECTORY = 'policies'
POLICY_CACHE_EXTENSION = '.json'

logging.basicConfig(format='[%(asctime)s|%(module)-25s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def get_successor_state(current_state, current_action, process):
    probability_threshold = random.random()

    total_probability = 0

    for successor_state in process.states():
        total_probability += process.transition_function(current_state, current_action, successor_state)
        if total_probability >= probability_threshold:
            return successor_state

    return None


def get_safety_process_solution(safety_process, epsilon):
    file_path = os.path.join(POLICY_CACHE_DIRECTORY, safety_process.kind + POLICY_CACHE_EXTENSION)

    if not os.path.exists(file_path):
        solution = safety_process_solver.solve(safety_process, GAMMA, epsilon)
        logging.debug("Saving the policy: [safety_process=%s, file=%s]", safety_process.kind, file_path)
        with open(file_path, 'w') as file:
            json.dump(solution, file, indent=4)

    logging.debug("Loading the policy: [safety_process=%s, file=%s]", safety_process.kind, file_path)
    with open(file_path) as file:
        return json.load(file)


def get_task_process_solution(task_process):
    file_path = os.path.join(POLICY_CACHE_DIRECTORY, task_process.kind + POLICY_CACHE_EXTENSION)

    if not os.path.exists(file_path):
        solution = task_process_solver.solve(task_process, GAMMA)
        logging.debug("Saving the policy: [task_process=%s, file=%s]", task_process.kind, file_path)
        with open(file_path, 'w') as file:
            json.dump(solution, file, indent=4)

    logging.debug("Loading the policy: [task_process=%s, file=%s]", task_process.kind, file_path)
    with open(file_path) as file:
        return json.load(file)


def get_plot_specification(experiment_results_container, safety_process_count):
    safety_processes = range(safety_process_count)

    plot_specification = {
        4: [[] for _ in safety_processes],
        3: [[] for _ in safety_processes],
        2: [[] for _ in safety_processes],
        1: [[] for _ in safety_processes],
        0: [[] for _ in safety_processes],
        999: [[] for _ in safety_processes]
    }

    for experimental_results in experiment_results_container:
        for safety_process in range(safety_process_count):
            plot_specification[4][safety_process].append(experimental_results['severity_level_5'][safety_process])
            plot_specification[3][safety_process].append(experimental_results['severity_level_4'][safety_process])
            plot_specification[2][safety_process].append(experimental_results['severity_level_3'][safety_process])
            plot_specification[1][safety_process].append(experimental_results['severity_level_2'][safety_process])
            plot_specification[0][safety_process].append(experimental_results['severity_level_1'][safety_process])
            plot_specification[999][safety_process].append(experimental_results['interference'][safety_process])

    return plot_specification


def get_empty_cells(grid_world):
    empty_cells = []

    for row in range(len(grid_world)):
        for column in range(len(grid_world[0])):
            if grid_world[row][column] == 'O':
                empty_cells.append((row, column))

    return empty_cells



def get_random_empty_cells(grid_world, retention_probability):
    empty_cells = []

    for row in range(len(grid_world)):
        for column in range(len(grid_world[0])):
            if grid_world[row][column] == 'O':
                empty_cells.append((row, column))

    return random.sample(empty_cells, round(retention_probability * len(empty_cells)))


def get_grid_world_with_weather(grid_world, shady_locations):
    new_grid_world = copy.deepcopy(grid_world)
    
    for shady_location in shady_locations:
        row = shady_location[0]
        column = shady_location[1]
        new_grid_world[row][column] = 'S' 
    
    return new_grid_world


def get_grid_world_with_points_of_interest(grid_world, points_of_interest):
    new_grid_world = copy.deepcopy(grid_world)

    for shady_location in points_of_interest:
        row = shady_location[0]
        column = shady_location[1]
        new_grid_world[row][column] = 'P' 
    
    return new_grid_world


def powerset(iterable):
    set = list(iterable)
    return chain.from_iterable(combinations(set, r) for r in range(len(set) + 1))