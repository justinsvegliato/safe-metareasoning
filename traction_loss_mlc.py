class TractionLossMlc:
    def __init__(self):
        pass

    def meta_level_states(self):
        return ['HIGH', 'MEDIUM', 'LOW']

    def meta_level_actions(self):
        return ['STOP', 'SLOW', 'NULL']

    def severity_function(self, state, action):
        if state == 'HIGH':
            if action == 'STOP':
                return 1

            if action == 'SLOW':
                return 3

            if action == 'NULL':
                return 5

        if state == 'MEDIUM':
            if action == 'STOP':
                return 1

            if action == 'SLOW':
                return 1

            if action == 'NULL':
                return 3

        if state == 'LOW':
            if action == 'STOP':
                return 1

            if action == 'SLOW':
                return 1

            if action == 'NULL':
                return 1

        return False

    def interference_function(self, _, action):
        if action == 'STOP':
            return 10

        if action == 'SLOW':
            return 5

        if action == 'NULL':
            return 0

        return False

    def recommend(self, state):
        return {action: (self.severity_function(state, action), self.interference_function(state, action)) for action in self.meta_level_actions()}
