import logging

import numpy as np

from solvers.mdp_container import MdpContainer
from solvers.memory_mdp_container import MemoryMdpContainer

ROUNDER = 3
MINIMUM_SEVERITY = 1
MAXIMUM_SEVERITY = 5

logging.basicConfig(format='[%(asctime)s|%(module)-25s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def value_iteration(memory_mdp_container, gamma, epsilon, severity=False, forbidden_state_action_pairs=False):
    states = memory_mdp_container.states
    actions = memory_mdp_container.actions

    reward_matrix = -1.0 * np.array(memory_mdp_container.rewards).astype('float32')
    transition_probability_matrix = np.array(memory_mdp_container.transition_probabilities).astype('float32')

    if severity:
        reward_matrix[reward_matrix > -severity] = 0
        reward_matrix[reward_matrix < -severity] = 0
        reward_matrix[reward_matrix == -severity] = -1

    if forbidden_state_action_pairs:
        for banned_state, banned_action in forbidden_state_action_pairs:
            reward_matrix[banned_state, banned_action] = -10000

    state_values = np.array([0.0 for s in range(len(states))]).astype('float32').reshape(-1, 1)
    action_values = np.array([[0.0 for a in range(len(actions))] for s in range(len(states))]).astype('float32')

    dimension_array = np.ones((1, transition_probability_matrix.ndim), int).ravel()
    dimension_array[2] = -1

    while True:
        action_values = reward_matrix + gamma * (np.sum(transition_probability_matrix * state_values.reshape(dimension_array), axis=2))
        new_state_values = np.amax(action_values, axis=1)

        if np.max(abs(new_state_values - state_values)) < epsilon:
            state_values = new_state_values
            break

        state_values = new_state_values

    state_values *= -1.0
    action_values *= -1.0

    return {
        'state_values': {state: float(state_values[state_index]) for state_index, state in enumerate(states)},
        'action_values': {state: {action: float(action_values[state_index][action_index]) for action_index, action in enumerate(actions)} for state_index, state in enumerate(states)},
        'policy': {state: actions[np.argmin(action_values[state_index])] for state_index, state in enumerate(states)}
    }


def get_empty_severity_state_values(safety_process):
    return {state: {severity: 0 for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1))} for state in safety_process.states()}


def get_empty_severity_parameter_values(safety_process):
    return {state: {parameter: {severity: 0 for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1))} for parameter in safety_process.parameters()} for state in safety_process.states()}


def get_rounded_interference_state_values(safety_process, state_values):
    return {state: round(state_values[state], ROUNDER) for state in safety_process.states()}


def get_rounded_interference_parameter_values(safety_process, action_values):
    return {state: {parameter: round(action_values[state][parameter], ROUNDER) for parameter in safety_process.parameters()} for state in safety_process.states()}


def solve(safety_process, gamma, epsilon):
    logging.info("Solving the safety process: [safety_process=%s]", safety_process.kind)

    severity_state_values = get_empty_severity_state_values(safety_process)
    severity_parameter_values = get_empty_severity_parameter_values(safety_process)

    severity_memory_mdp_container = MemoryMdpContainer(MdpContainer(safety_process, 'severity'))
    size = severity_memory_mdp_container.n_states * severity_memory_mdp_container.n_actions

    forbidden_state_action_pairs = set()
    for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1)):
        logging.info("Performing value iteration: [severity=%d, size=%d]", severity, size - len(forbidden_state_action_pairs))

        solution = value_iteration(severity_memory_mdp_container, gamma, epsilon, severity, forbidden_state_action_pairs)

        for state in safety_process.states():
            severity_state_values[state][severity] = round(solution['state_values'][state], ROUNDER)
            for parameter in safety_process.parameters():
                severity_parameter_values[state][parameter][severity] = round(solution['action_values'][state][parameter], ROUNDER)

        for state_index, state in enumerate(severity_parameter_values):
            minimum_severity_value = min([severity_parameter_values[state][parameter][severity] for parameter in severity_parameter_values[state]])
            for parameter_index, parameter in enumerate(severity_parameter_values[state]):
                if severity_parameter_values[state][parameter][severity] > minimum_severity_value:
                    forbidden_state_action_pairs.add((state_index, parameter_index))

    logging.info("Performing value iteration: [interference, size=%d]", size - len(forbidden_state_action_pairs))

    interference_memory_mdp_container = MemoryMdpContainer(MdpContainer(safety_process, 'interference'))
    solution = value_iteration(interference_memory_mdp_container, gamma, epsilon, False, forbidden_state_action_pairs)

    interference_state_values = get_rounded_interference_state_values(safety_process, solution['state_values'])
    interference_parameter_values = get_rounded_interference_parameter_values(safety_process, solution['action_values'])

    return {
        'severity_state_values': severity_state_values,
        'severity_parameter_values': severity_parameter_values,
        'policy': solution['policy'],
        'interference_state_values': interference_state_values,
        'interference_parameter_values': interference_parameter_values
    }
