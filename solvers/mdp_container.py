MAXIMUM_SEVERITY = 5

class MdpContainer:
    def __init__(self, mlc):
        self.mlc = mlc

    def states(self):
        return self.mlc.states()

    def actions(self):
        return self.mlc.parameters()

    def transition_function(self, state, action, successor_state):
        return self.mlc.transition_function(state, action, successor_state)

    def reward_function(self, state, action):
        return MAXIMUM_SEVERITY - self.mlc.severity_function(state, action)

    def start_state_function(self, state):
        start_states = self.mlc.start_states()
        return 1.0 / len(start_states) if state in start_states else 0
