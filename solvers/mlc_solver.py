import logging

import numpy as np

from solvers.mdp_container import MdpContainer
from solvers.memory_mdp import MemoryMdp

ROUNDER = 3
MAXIMUM_SEVERITY = 5
MINIMUM_SEVERITY = 1

logging.basicConfig(format='[%(asctime)s|%(module)-20s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def value_iteration(memory_mdp, gamma, epsilon, severity=False, suboptimal_state_action_pairs=False):
    states = memory_mdp.states
    actions = memory_mdp.actions

    reward_matrix = -1.0 * np.array(memory_mdp.rewards).astype('float32')
    transition_probability_matrix = np.array(memory_mdp.transition_probabilities).astype('float32')

    if severity:
        reward_matrix[reward_matrix > -severity] = 0
        reward_matrix[reward_matrix < -severity] = 0
        reward_matrix[reward_matrix == -severity] = -1

    if suboptimal_state_action_pairs:
        for banned_state, banned_action in suboptimal_state_action_pairs:
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

    v = {state: float(state_values[state_index]) for state_index, state in enumerate(states)}
    q = {state: {action: float(action_values[state_index][action_index]) for action_index, action in enumerate(actions)} for state_index, state in enumerate(states)}
    policy = {state: actions[np.argmin(action_values[state_index])] for state_index, state in enumerate(states)}

    return {'state_values': v, 'action_values': q, 'policy': policy}


def get_empty_severity_state_values(mlc):
    return {state: {severity: 0 for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1))} for state in mlc.states()}


def get_empty_severity_parameter_values(mlc):
    return {state: {parameter: {severity: 0 for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1))} for parameter in mlc.parameters()} for state in mlc.states()}


def solve(mlc, gamma, epsilon):
    mdp_container = MdpContainer(mlc, True)
    memory_mdp = MemoryMdp(mdp_container)

    severity_state_values = get_empty_severity_state_values(mlc)
    severity_parameter_values = get_empty_severity_parameter_values(mlc)

    suboptimal_state_action_pairs = set()
    for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1)):
        logging.info("Performing value iteration for severity: [%d]", severity)

        solution = value_iteration(memory_mdp, gamma, epsilon, severity, suboptimal_state_action_pairs)
        state_values = solution['state_values']
        action_values = solution['action_values']
        policy = solution['policy']

        for state in mlc.states():
            severity_state_values[state][severity] = round(state_values[state], ROUNDER)
            for parameter in mlc.parameters():
                severity_parameter_values[state][parameter][severity] = round(action_values[state][parameter], ROUNDER)

        for state_index, state in enumerate(severity_parameter_values):
            minimum_severity_value = min([severity_parameter_values[state][parameter][severity] for parameter in severity_parameter_values[state]])
            for parameter_index, parameter in enumerate(severity_parameter_values[state]):
                if severity_parameter_values[state][parameter][severity] > minimum_severity_value:
                    suboptimal_state_action_pairs.add((state_index, parameter_index))

        logging.info("Suboptimal state action pairs: [%d]", len(suboptimal_state_action_pairs))

    mdp_container = MdpContainer(mlc, False)
    memory_mdp = MemoryMdp(mdp_container)

    solution = value_iteration(memory_mdp, gamma, epsilon, False, suboptimal_state_action_pairs)
    state_values = solution['state_values']
    action_values = solution['action_values']
    policy = solution['policy']

    interference_state_values = {state: round(state_values[state], ROUNDER) for state in mlc.states()}
    interference_parameter_values = {state: {parameter: round(action_values[state][parameter], ROUNDER) for parameter in mlc.parameters()} for state in mlc.states()}

    return {
        'severity_state_values': severity_state_values,
        'severity_parameter_values': severity_parameter_values,
        'policy': policy,
        'interference_state_values': interference_state_values,
        'interference_parameter_values': interference_parameter_values
    }
