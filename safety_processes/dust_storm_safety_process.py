import itertools

NOMINAL_DUST_STORM_LEVEL = 6
MINIMUM_DUST_STORM_LEVEL = 1
MAXIMUM_DUST_STORM_LEVEL = 10
DUST_STORM_LEVEL = range(MINIMUM_DUST_STORM_LEVEL, MAXIMUM_DUST_STORM_LEVEL + 1)

ROVER_MODE = ['IS_NOT_STOPPED', 'IS_STOPPED']

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

DUST_STORM_INCREASE_PROBABILITY = 0.2
DUST_STORM_REMAIN_PROBABILITY = 0.6
DUST_STORM_DECREASE_PROBABILITY = 0.2

SEVERITY_MAP = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 2,
    8: 3,
    9: 4,
    10: 5
}

INTERFERENCE_MAP = {
    'NONE': 0,
    'SPEED_UP': 1,
    'SLOW_DOWN': 5,
    'STOP': 10,
    'SHIFT_LEFT': 2,
    'SHIFT_RIGHT': 2
}

class DustStormSafetyProcess:
    identifier = 1

    def __init__(self):
        self.kind = 'dust-storm-safety-process'
        self.name = f'dust-storm-safety-process-{DustStormSafetyProcess.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product(DUST_STORM_LEVEL, ROVER_MODE):
            state = ':'.join((str(state_factor) for state_factor in state_tuple))
            self.state_registry[state] = {
                'dust_storm_level': state_tuple[0],
                'rover_mode': state_tuple[1]
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

        DustStormSafetyProcess.identifier += 1

    def states(self):
        return self.state_space

    def parameters(self):
        return self.parameter_space

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        dust_storm_level_probability = 0
        if state_record['dust_storm_level'] == MINIMUM_DUST_STORM_LEVEL and state_record['dust_storm_level'] == successor_state_record['dust_storm_level']:
            dust_storm_level_probability = DUST_STORM_REMAIN_PROBABILITY + DUST_STORM_DECREASE_PROBABILITY
        elif state_record['dust_storm_level'] == MAXIMUM_DUST_STORM_LEVEL and state_record['dust_storm_level'] == successor_state_record['dust_storm_level']:
            dust_storm_level_probability = DUST_STORM_REMAIN_PROBABILITY + DUST_STORM_INCREASE_PROBABILITY
        elif state_record['dust_storm_level'] == successor_state_record['dust_storm_level'] + 1:
            dust_storm_level_probability = DUST_STORM_DECREASE_PROBABILITY
        elif state_record['dust_storm_level'] == successor_state_record['dust_storm_level']:
            dust_storm_level_probability = DUST_STORM_REMAIN_PROBABILITY
        elif state_record['dust_storm_level'] == successor_state_record['dust_storm_level'] - 1:
            dust_storm_level_probability = DUST_STORM_INCREASE_PROBABILITY

        if parameter_record['wheel_rotation_parameter'] == 'STOP' and successor_state_record['rover_mode'] == 'IS_STOPPED':
            return dust_storm_level_probability

        if parameter_record['wheel_rotation_parameter'] != 'STOP' and successor_state_record['rover_mode'] == 'IS_NOT_STOPPED':
            return dust_storm_level_probability

        return 0

    def severity_function(self, state, _):
        dust_storm_level = self.state_registry[state]['dust_storm_level']
        rover_mode = self.state_registry[state]['rover_mode']

        if rover_mode == 'IS_STOPPED':
            return 1

        return SEVERITY_MAP[dust_storm_level]

    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        wheel_rotation_parameter = parameter_record['wheel_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[wheel_rotation_parameter] + INTERFERENCE_MAP[steering_parameter]

    def start_states(self):
        return [f'{NOMINAL_DUST_STORM_LEVEL}:IS_STOPPED', f'{NOMINAL_DUST_STORM_LEVEL}:IS_NOT_STOPPED']
