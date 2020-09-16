import math

MAXIMUM_SEVERITY = 5


def get_severity_state_values(mdp, gamma, epsilon):
    severity_state_values = {state: 0.0 for state in mdp.states()}

    while True:
        delta = 0

        for state in mdp.states():
            best_severity_value = float('-inf')

            for action in mdp.actions():
                immediate_severity = MAXIMUM_SEVERITY - mdp.severity_function(state, action)

                expected_future_severity = 0
                for successor_state in mdp.states():
                    expected_future_severity += mdp.transition_function(state, action, successor_state) * severity_state_values[successor_state]

                severity_value = immediate_severity + gamma * expected_future_severity

                if best_severity_value < severity_value:
                    best_severity_value = severity_value

            delta = max(delta, math.fabs(best_severity_value - severity_state_values[state]))
            severity_state_values[state] = best_severity_value

        print('Delta:', delta)
        if delta < epsilon:
            return severity_state_values


def get_interference_state_values(mdp, gamma, epsilon, policy):
    interference_state_values = {state: 0.0 for state in mdp.states()}

    while True:
        delta = 0

        for state in mdp.states():
            immediate_interference = MAXIMUM_SEVERITY - mdp.interference_function(state, policy[state])

            expected_future_interference = 0
            for successor_state in mdp.states():
                expected_future_interference += mdp.transition_function(state, policy[state], successor_state) * interference_state_values[successor_state]

            new_interference_value = immediate_interference + gamma * expected_future_interference
            delta = max(delta, math.fabs(new_interference_value - interference_state_values[state]))
            interference_state_values[state] = new_interference_value

        print('Delta:', delta)
        if delta < epsilon:
            return interference_state_values


def get_severity_action_values(mdp, gamma, severity_state_values):
    severity_action_values = {}

    for state in mdp.states():
        severity_action_values[state] = {}

        for action in mdp.actions():
            immediate_severity = MAXIMUM_SEVERITY - mdp.severity_function(state, action)

            expected_future_severity = 0
            for successor_state in mdp.states():
                expected_future_severity += mdp.transition_function(state, action, successor_state) * severity_state_values[successor_state]

            severity_action_values[state][action] = immediate_severity + gamma * expected_future_severity

    return severity_action_values


def get_interference_action_values(mdp, gamma, interference_state_values):
    interference_action_values = {}

    for state in mdp.states():
        interference_action_values[state] = {}

        for action in mdp.actions():
            immediate_interference = mdp.interference_function(state, action)

            expected_future_interference = 0
            for successor_state in mdp.states():
                expected_future_interference += mdp.transition_function(state, action, successor_state) * interference_state_values[successor_state]

            interference_action_values[state][action] = immediate_interference + gamma * expected_future_interference

    return interference_action_values


def get_policy(mdp, gamma, severity_state_values):
    policy = {}

    for state in mdp.states():
        best_action = None
        best_action_value = None

        for action in mdp.actions():
            immediate_severity = MAXIMUM_SEVERITY - mdp.severity_function(state, action)

            expected_future_severity = 0
            for successor_state in mdp.states():
                expected_future_severity += mdp.transition_function(state, action, successor_state) * severity_state_values[successor_state]

            action_value = immediate_severity + gamma * expected_future_severity

            if best_action_value is None or action_value > best_action_value:
                best_action = action
                best_action_value = action_value

        policy[state] = best_action

    return policy


def solve(mdp, gamma, epsilon):
    severity_state_values = get_severity_state_values(mdp, gamma, epsilon)
    severity_action_values = get_severity_action_values(mdp, gamma, severity_state_values)

    policy = get_policy(mdp, gamma, severity_state_values)

    interference_state_values = get_interference_state_values(mdp, gamma, epsilon, policy)
    interference_action_values = get_interference_action_values(mdp, gamma, interference_state_values)

    return {
        'severity_state_values': severity_state_values,
        'severity_action_values': severity_action_values,
        'interference_state_values': interference_state_values,
        'interference_action_values': interference_action_values,
        'policy': policy
    }
  