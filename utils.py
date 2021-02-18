import json
import logging
import os
import random

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
        logging.info("Saving the policy: [safety_process=%s, file=%s]", safety_process.kind, file_path)
        with open(file_path, 'w') as file:
            json.dump(solution, file, indent=4)

    logging.info("Loading the policy: [safety_process=%s, file=%s]", safety_process.kind, file_path)
    with open(file_path) as file:
        return json.load(file)


def get_task_process_solution(task_process):
    file_path = os.path.join(POLICY_CACHE_DIRECTORY, task_process.kind + POLICY_CACHE_EXTENSION)

    if not os.path.exists(file_path):
        solution = task_process_solver.solve(task_process, GAMMA)
        logging.info("Saving the policy: [task_process=%s, file=%s]", task_process.kind, file_path)
        with open(file_path, 'w') as file:
            json.dump(solution, file, indent=4)

    logging.info("Loading the policy: [task_process=%s, file=%s]", task_process.kind, file_path)
    with open(file_path) as file:
        return json.load(file)
