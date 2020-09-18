import cplex
import numpy as np


class MemoryMDP:
    def __init__(self, mdp):
        self.states = mdp.states()
        self.actions = mdp.actions()

        self.n_states = len(self.states)
        self.n_actions = len(self.actions)

        self.rewards = np.zeros(shape=(self.n_states, self.n_actions))
        for state in range(self.n_states):
            for action in range(self.n_actions):
                self.rewards[state, action] = mdp.reward_function(self.states[state], self.actions[action])

        self.transition_probabilities = np.zeros(shape=(self.n_states, self.n_actions, self.n_states))
        for state in range(self.n_states):
            for action in range(self.n_actions):
                for successor_state in range(self.n_states):
                    self.transition_probabilities[state, action, successor_state] = mdp.transition_function(self.states[state], self.actions[action], self.states[successor_state])

        self.start_state_probabilities = np.zeros(self.n_states)
        for state in range(self.n_states):
            self.start_state_probabilities[state] = mdp.start_state_function(self.states[state])


def validate(memory_mdp):
    assert memory_mdp.n_states is not None
    assert memory_mdp.n_actions is not None

    assert memory_mdp.states is not None
    assert memory_mdp.actions is not None
    assert memory_mdp.rewards is not None
    assert memory_mdp.transition_probabilities is not None
    assert memory_mdp.start_state_probabilities is not None

    assert memory_mdp.rewards.shape == (memory_mdp.n_states, memory_mdp.n_actions)
    assert memory_mdp.transition_probabilities.shape == (memory_mdp.n_states, memory_mdp.n_actions, memory_mdp.n_states)
    assert memory_mdp.start_state_probabilities.shape == (memory_mdp.n_states,)


def set_variables(program, memory_mdp):
    program.variables.add(types=[program.variables.type.continuous] * memory_mdp.n_states)


def set_objective(program, memory_mdp):
    program.objective.set_linear([(i, memory_mdp.start_state_probabilities[i]) for i in range(memory_mdp.n_states)])
    program.objective.set_sense(program.objective.sense.minimize)


def set_constraints(program, memory_mdp, gamma):
    lin_expr = []
    rhs = []

    variables = range(memory_mdp.n_states)

    for i in range(memory_mdp.n_states):
        for j in range(memory_mdp.n_actions):
            coefficients = []

            for k in range(memory_mdp.n_states):
                if k != i:
                    coefficient = - gamma * memory_mdp.transition_probabilities[i, j, k]
                else:
                    coefficient = 1 - gamma * memory_mdp.transition_probabilities[i, j, k]

                coefficients.append(coefficient)

            lin_expr.append([variables, coefficients])
            rhs.append(float(memory_mdp.rewards[i, j]))

    program.linear_constraints.add(lin_expr=lin_expr, rhs=rhs, senses=["G"] * len(rhs))


def get_policy(values, memory_mdp, gamma):
    policy = []

    for i in range(memory_mdp.n_states):
        best_action, best_action_value = None, None

        for j in range(memory_mdp.n_actions):
            action_value = memory_mdp.rewards[i, j] + gamma * np.sum(memory_mdp.transition_probabilities[i, j] * values)
            if best_action_value is None or action_value > best_action_value:
                best_action = j
                best_action_value = action_value

        policy.append(best_action)

    return policy


def solve(mdp, gamma):
    memory_mdp = MemoryMDP(mdp)

    validate(memory_mdp)

    program = cplex.Cplex()

    set_variables(program, memory_mdp)
    set_objective(program, memory_mdp)
    set_constraints(program, memory_mdp, gamma)

    print("===== Program Details =============================================")
    print("{} variables".format(program.variables.get_num()))
    print("{} sense".format(program.objective.sense[program.objective.get_sense()]))
    print("{} linear coefficients".format(len(program.objective.get_linear())))
    print("{} linear constraints".format(program.linear_constraints.get_num()))

    print("===== CPLEX Details ===============================================")
    program.solve()
    print("===================================================================")

    objective_value = program.solution.get_objective_value()
    values = program.solution.get_values()
    policy = get_policy(values, memory_mdp, gamma)

    return {
        'objective_value': objective_value,
        'values': {memory_mdp.states[state]: value for state, value in enumerate(values)},
        'policy': {memory_mdp.states[state]: memory_mdp.actions[action] for state, action in enumerate(policy)}
    }
