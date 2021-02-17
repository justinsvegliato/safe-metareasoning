import itertools

NOMINAL_TEMPERATURE = 5
MINIMUM_TEMPERATURE = 1
MAXIMUM_TEMPERATURE = 10
WHEEL_MOTOR_TEMPERATURE = range(MINIMUM_TEMPERATURE, MAXIMUM_TEMPERATURE + 1)

WHEEL_ROTATION_RATE = ['NONE', 'LOW', 'NORMAL', 'HIGH']

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
ARM_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

WHEEL_MOTOR_TEMPERATURE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.9, 'REMAIN': 0.1, 'INCREASE': 0.0},
    'LOW': {'DECREASE': 0.7, 'REMAIN': 0.3, 'INCREASE': 0.0},
    'NORMAL': {'DECREASE': 0.05, 'REMAIN': 0.9, 'INCREASE': 0.05},
    'HIGH': {'DECREASE': 0.0, 'REMAIN': 0.3, 'INCREASE': 0.7}
}

WHEEL_ROTATION_RATE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.0, 'REMAIN': 1.0, 'INCREASE': 0.0},
    'SPEED_UP': {'DECREASE': 0.0, 'REMAIN': 0.05, 'INCREASE': 0.95},
    'SLOW_DOWN': {'DECREASE': 0.95, 'REMAIN': 0.05, 'INCREASE': 0.0}
}

SEVERITY_MAP = {
    1: 5,
    2: 4,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 4,
    10: 5
}

INTERFERENCE_MAP = {
    'NONE': 0,
    'SPEED_UP': 0,
    'SLOW_DOWN': 5,
    'STOP': 10,
    'SHIFT_LEFT': 2,
    'SHIFT_RIGHT': 2
}


class WheelMotorTemperatureMlc:
    identifier = 1

    def __init__(self):
        self.kind = 'wheel-motor-temperature-mlc'
        self.name = f'wheel-motor-temperature-mlc-{WheelMotorTemperatureMlc.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product(WHEEL_MOTOR_TEMPERATURE, WHEEL_ROTATION_RATE):
            state = ':'.join((str(state_factor) for state_factor in state_tuple))
            self.state_registry[state] = {
                'wheel_motor_temperature': state_tuple[0],
                'wheel_rotation_rate': state_tuple[1]
            }

        self.parameter_registry = {}
        for parameter_tuple in itertools.product(WHEEL_ROTATION_PARAMETERS, ARM_ROTATION_PARAMETERS, STEERING_PARAMETERS):
            parameter = ':'.join(parameter_tuple)
            self.parameter_registry[parameter] = {
                'wheel_rotation_parameter': parameter_tuple[0],
                'arm_rotation_parameter': parameter_tuple[1],
                'steering_parameter': parameter_tuple[2]
            }

        self.state_space = list(self.state_registry.keys())
        self.parameter_space = list(self.parameter_registry.keys())

        WheelMotorTemperatureMlc.identifier += 1

    def states(self):
        return self.state_space

    def parameters(self):
        return self.parameter_space

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        wheel_rotation_rate_probability = 0
        if parameter_record['wheel_rotation_parameter'] == 'STOP':
            wheel_rotation_rate_probability = 1 if successor_state_record['wheel_rotation_rate'] == 'NONE' else 0
        elif state_record['wheel_rotation_rate'] == 'NONE' and successor_state_record['wheel_rotation_rate'] == 'NONE':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['REMAIN'] + WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == 'HIGH' and successor_state_record['wheel_rotation_rate'] == 'HIGH':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['REMAIN'] + WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'NONE' and successor_state_record['wheel_rotation_rate'] == 'LOW':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'LOW' and successor_state_record['wheel_rotation_rate'] == 'NORMAL':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'NORMAL' and successor_state_record['wheel_rotation_rate'] == 'HIGH':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'LOW' and successor_state_record['wheel_rotation_rate'] == 'NONE':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == 'NORMAL' and successor_state_record['wheel_rotation_rate'] == 'LOW':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == 'HIGH' and successor_state_record['wheel_rotation_rate'] == 'NORMAL':
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == successor_state_record['wheel_rotation_rate']:
            wheel_rotation_rate_probability = WHEEL_ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['REMAIN']

        wheel_temperature_probability = 0
        if state_record['wheel_motor_temperature'] == MINIMUM_TEMPERATURE and state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature']:
            wheel_temperature_probability = WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] + WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE']
        elif state_record['wheel_motor_temperature'] == MAXIMUM_TEMPERATURE and state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature']:
            wheel_temperature_probability = WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] + WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE']
        elif state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] + 1:
            wheel_temperature_probability = WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE']
        elif state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature']:
            wheel_temperature_probability = WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN']
        elif state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] - 1:
            wheel_temperature_probability = WHEEL_MOTOR_TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE']

        return wheel_rotation_rate_probability * wheel_temperature_probability

    def severity_function(self, state, _):
        wheel_motor_temperature = self.state_registry[state]['wheel_motor_temperature']
        return SEVERITY_MAP[wheel_motor_temperature]

    # TODO: Should arm motor temperature be included in this?
    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        wheel_rotation_parameter = parameter_record['wheel_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[wheel_rotation_parameter] + INTERFERENCE_MAP[steering_parameter]

    def start_states(self):
        return [f'{NOMINAL_TEMPERATURE}:NORMAL']
