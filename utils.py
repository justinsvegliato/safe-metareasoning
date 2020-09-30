import random


def get_successor_state(current_state, current_action, mdp):
    probability_threshold = random.random()

    total_probability = 0

    for successor_state in mdp.states():
        total_probability += mdp.transition_function(current_state, current_action, successor_state)
        if total_probability >= probability_threshold:
            return successor_state

    return None
