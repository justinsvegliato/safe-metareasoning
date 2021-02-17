import random


def get_successor_state(current_state, current_action, task_process):
    probability_threshold = random.random()

    total_probability = 0

    for successor_state in task_process.states():
        total_probability += task_process.transition_function(current_state, current_action, successor_state)
        if total_probability >= probability_threshold:
            return successor_state

    return None
