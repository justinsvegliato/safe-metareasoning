import math


def get_severity_state_values(mlc, gamma, epsilon):
    severity_state_values = {state: 0.0 for state in mlc.states()}

    while True:
        delta = 0

        for state in mlc.states():
            best_severity_value = float('inf')

            for parameter in mlc.parameters():
                immediate_severity = mlc.severity_function(state, parameter)

                expected_future_severity = 0
                for successor_state in mlc.states():
                    expected_future_severity += mlc.transition_function(state, parameter, successor_state) * severity_state_values[successor_state]

                severity_value = immediate_severity + gamma * expected_future_severity

                if best_severity_value > severity_value:
                    best_severity_value = severity_value

            delta = max(delta, math.fabs(best_severity_value - severity_state_values[state]))
            severity_state_values[state] = best_severity_value

        print('Delta:', delta)
        if delta < epsilon:
            return severity_state_values


def get_interference_state_values(mlc, gamma, epsilon, policy):
    interference_state_values = {state: 0.0 for state in mlc.states()}

    while True:
        delta = 0

        for state in mlc.states():
            immediate_interference = mlc.interference_function(state, policy[state])

            expected_future_interference = 0
            for successor_state in mlc.states():
                expected_future_interference += mlc.transition_function(state, policy[state], successor_state) * interference_state_values[successor_state]

            new_interference_value = immediate_interference + gamma * expected_future_interference
            delta = max(delta, math.fabs(new_interference_value - interference_state_values[state]))
            interference_state_values[state] = new_interference_value

        print('Delta:', delta)
        if delta < epsilon:
            return interference_state_values


def get_severity_parameter_values(mlc, gamma, severity_state_values):
    severity_parameter_values = {}

    for state in mlc.states():
        severity_parameter_values[state] = {}

        for parameter in mlc.parameters():
            immediate_severity = mlc.severity_function(state, parameter)

            expected_future_severity = 0
            for successor_state in mlc.states():
                expected_future_severity += mlc.transition_function(state, parameter, successor_state) * severity_state_values[successor_state]

            severity_parameter_values[state][parameter] = immediate_severity + gamma * expected_future_severity

    return severity_parameter_values


def get_interference_parameter_values(mlc, gamma, interference_state_values):
    interference_parameter_values = {}

    for state in mlc.states():
        interference_parameter_values[state] = {}

        for parameter in mlc.parameters():
            immediate_interference = mlc.interference_function(state, parameter)

            expected_future_interference = 0
            for successor_state in mlc.states():
                expected_future_interference += mlc.transition_function(state, parameter, successor_state) * interference_state_values[successor_state]

            interference_parameter_values[state][parameter] = immediate_interference + gamma * expected_future_interference

    return interference_parameter_values


def get_policy(mlc, gamma, severity_state_values):
    policy = {}

    for state in mlc.states():
        best_parameter = None
        best_parameter_value = None

        for parameter in mlc.parameters():
            immediate_severity = mlc.severity_function(state, parameter)

            expected_future_severity = 0
            for successor_state in mlc.states():
                expected_future_severity += mlc.transition_function(state, parameter, successor_state) * severity_state_values[successor_state]

            parameter_value = immediate_severity + gamma * expected_future_severity

            if best_parameter_value is None or parameter_value < best_parameter_value:
                best_parameter = parameter
                best_parameter_value = parameter_value

        policy[state] = best_parameter

    return policy


def solve(mlc, gamma, epsilon):
    severity_state_values = get_severity_state_values(mlc, gamma, epsilon)
    severity_parameter_values = get_severity_parameter_values(mlc, gamma, severity_state_values)

    # import json
    # print(json.dumps(severity_parameter_values, indent=4))

    policy = get_policy(mlc, gamma, severity_state_values)
    # print(json.dumps(policy, indent=4))

    # exit()

    interference_state_values = get_interference_state_values(mlc, gamma, epsilon, policy)
    interference_parameter_values = get_interference_parameter_values(mlc, gamma, interference_state_values)

    return {
        'severity_state_values': severity_state_values,
        'severity_parameter_values': severity_parameter_values,
        'interference_state_values': interference_state_values,
        'interference_parameter_values': interference_parameter_values,
        'policy': policy
    }
  