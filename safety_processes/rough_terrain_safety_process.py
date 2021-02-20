import itertools

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

SEVERITY_MAP = {
}

INTERFERENCE_MAP = {
    'NONE': {'NONE': 0, 'SHIFT_LEFT': 10, 'SHIFT_RIGHT': 10},
    'SPEED_UP': {'NONE': 5, 'SHIFT_LEFT': 15, 'SHIFT_RIGHT': 15},
    'SLOW_DOWN': {'NONE': 5, 'SHIFT_LEFT': 15, 'SHIFT_RIGHT': 15},
    'STOP': {'NONE': 20, 'SHIFT_LEFT': 25, 'SHIFT_RIGHT': 30},
}


class RoughTerrainSafetyProcess:
    identifier = 1

    def __init__(self):
        self.kind = 'rough-terrain-safety-process'
        self.name = f'rough-terrain-safety-process-{RoughTerrainSafetyProcess.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product():
            state = ':'.join(state_tuple)
            self.state_registry[state] = {
            }

        self.parameter_registry = {}
        for parameter_tuple in itertools.product(WHEEL_ROTATION_PARAMETERS, STEERING_PARAMETERS):
            parameter = ':'.join(parameter_tuple)
            self.parameter_registry[parameter] = {
                'wheel_rotation_parameter': parameter_tuple[0],
                'steering_parameter': parameter_tuple[1]
            }

        self.state_space = list(self.state_registry.keys())
        self.parameter_space = list(self.parameter_registry.keys())

        RoughTerrainSafetyProcess.identifier += 1

    def states(self):
        return self.state_space

    def parameters(self):
        return self.parameter_space

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]
        return 1

    def severity_function(self, state, _):
        state_record = self.state_registry[state]
        return 1

    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        wheel_rotation_parameter = parameter_record['wheel_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[wheel_rotation_parameter][steering_parameter]

    def start_states(self):
        start_states = []
        return start_states
