import math


def get_values(mdp, gamma, epsilon):
    values = {state: 0.0 for state in mdp.states()}

    while True:
        delta = 0

        for state in mdp.states():
            best_value = float('-inf')

            for action in mdp.actions():
                immediate_reward = 5 - mdp.reward_function(state, action)

                expected_future_reward = 0
                for successor_state in mdp.states():
                    expected_future_reward += mdp.transition_function(state, action, successor_state) * values[successor_state]

                value = immediate_reward + gamma * expected_future_reward
                if best_value < value:
                    best_value = value

            new_value = best_value

            delta = max(delta, math.fabs(new_value - values[state]))

            values[state] = new_value

        print('Delta', delta)

        if delta < epsilon:
            return values


def get_policy(mdp, values, gamma):
    policy = {}

    for state in mdp.states():
        best_action, best_action_value = None, None

        for action in mdp.actions():
            immediate_reward = 5 - mdp.reward_function(state, action)

            expected_future_reward = 0
            for successor_state in mdp.states():
                expected_future_reward += mdp.transition_function(state, action, successor_state) * values[successor_state]

            action_value = immediate_reward + gamma * expected_future_reward

            if best_action_value is None or action_value > best_action_value:
                best_action = action
                best_action_value = action_value

        policy[state] = best_action

    return policy
 

def solve(mdp, gamma, epsilon):
    values = get_values(mdp, gamma, epsilon)
    policy = get_policy(mdp, values, gamma)

    return {
        'values': values,
        'policy': policy
    }
  