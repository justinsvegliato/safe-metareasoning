class MdpContainer:
    def __init__(self, mlc, objective):
        self.mlc = mlc
        self.objective = objective

    def states(self):
        return self.mlc.states()

    def actions(self):
        return self.mlc.parameters()

    def transition_function(self, state, action, successor_state):
        return self.mlc.transition_function(state, action, successor_state)

    def reward_function(self, state, action):
        if self.objective == 'severity':
            return self.mlc.severity_function(state, action)

        if self.objective == 'interference':
            return self.mlc.interference_function(state, action)

        return None

    def start_state_function(self, state):
        start_states = self.mlc.start_states()
        return 1.0 / len(start_states) if state in start_states else 0
