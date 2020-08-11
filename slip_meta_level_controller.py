class SlipMetaLevelController:
    def __init__(self):
        pass

    def meta_level_states(self):
        return []

    def meta_level_actions(self):
        return []

    def meta_level_transition_function(self, state, action, successor_state):
        return 1

    def severity_function(self, state, action):
        return 0

    def interference_function(self, state, action):
        return 0

    def recommend(self, state):
        return {action: (self.severity_function(state, action), self.interference_function(state, action)) for action in self.meta_level_actions()}
