class MdpContainer:
    def __init__(self, safety_process, objective):
        self.safety_process = safety_process
        self.objective = objective

    def states(self):
        return self.safety_process.states()

    def actions(self):
        return self.safety_process.parameters()

    def transition_function(self, state, action, successor_state):
        return self.safety_process.transition_function(state, action, successor_state)

    def reward_function(self, state, action):
        if self.objective == 'severity':
            return self.safety_process.severity_function(state, action)

        if self.objective == 'interference':
            return self.safety_process.interference_function(state, action)

        return None

    def start_state_function(self, state):
        start_states = self.safety_process.start_states()
        return 1.0 / len(start_states) if state in start_states else 0
