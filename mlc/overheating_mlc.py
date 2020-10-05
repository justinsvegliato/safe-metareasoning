import itertools

NOMINAL_TEMPERATURE = 3
MINIMUM_TEMPERATURE = 1
MAXIMUM_TEMPERATURE = 5
WHEEL_MOTOR_TEMPERATURE = range(MINIMUM_TEMPERATURE, MAXIMUM_TEMPERATURE + 1)
ARM_MOTOR_TEMPERATURE = range(MINIMUM_TEMPERATURE, MAXIMUM_TEMPERATURE + 1)

WHEEL_ROTATION_RATE = ['NONE', 'LOW', 'NORMAL', 'HIGH']
ARM_ROTATION_RATE = ['NONE', 'LOW', 'NORMAL', 'HIGH']

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN']
ARM_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

TEMPERATURE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.9, 'REMAIN': 0.1, 'INCREASE': 0.0},
    'LOW': {'DECREASE': 0.7, 'REMAIN': 0.3, 'INCREASE': 0.0},
    'NORMAL': {'DECREASE': 0.05, 'REMAIN': 0.9, 'INCREASE': 0.05},
    'HIGH': {'DECREASE': 0.0, 'REMAIN': 0.3, 'INCREASE': 0.7}
}

ROTATION_RATE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.0, 'REMAIN': 1.0, 'INCREASE': 0.0},
    'SPEED_UP': {'DECREASE': 0.0, 'REMAIN': 0.05, 'INCREASE': 0.95},
    'SLOW_DOWN': {'DECREASE': 0.95, 'REMAIN': 0.05, 'INCREASE': 0.0},
}

INTERFERENCE_MAP = {
    'NONE': 0,
    'SPEED_UP': 0,
    'SLOW_DOWN': 5,
    'SHIFT_LEFT': 2,
    'SHIFT_RIGHT': 2
}


class OverheatingMlc:
    identifier = 1

    def __init__(self):
        self.kind = 'overheating-mlc'
        self.name = f'overheating-mlc-{OverheatingMlc.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product(WHEEL_MOTOR_TEMPERATURE, ARM_MOTOR_TEMPERATURE, WHEEL_ROTATION_RATE, ARM_ROTATION_RATE):
            state = ':'.join((str(state_factor) for state_factor in state_tuple))
            self.state_registry[state] = {
                'wheel_motor_temperature': state_tuple[0],
                'arm_motor_temperature': state_tuple[1],
                'wheel_rotation_rate': state_tuple[2],
                'arm_rotation_rate': state_tuple[3]
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

        OverheatingMlc.identifier += 1

    def states(self):
        return self.state_space

    def parameters(self):
        return self.parameter_space

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        wheel_rotation_rate_probability = 0
        if state_record['wheel_rotation_rate'] == 'NONE' and successor_state_record['wheel_rotation_rate'] == 'NONE':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['REMAIN'] + ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == 'HIGH' and successor_state_record['wheel_rotation_rate'] == 'HIGH':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['REMAIN'] + ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'NONE' and successor_state_record['wheel_rotation_rate'] == 'LOW':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'LOW' and successor_state_record['wheel_rotation_rate'] == 'NORMAL':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'NORMAL' and successor_state_record['wheel_rotation_rate'] == 'HIGH':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['INCREASE']
        elif state_record['wheel_rotation_rate'] == 'LOW' and successor_state_record['wheel_rotation_rate'] == 'NONE':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == 'NORMAL' and successor_state_record['wheel_rotation_rate'] == 'LOW':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == 'HIGH' and successor_state_record['wheel_rotation_rate'] == 'NORMAL':
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['DECREASE']
        elif state_record['wheel_rotation_rate'] == successor_state_record['wheel_rotation_rate']:
            wheel_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['wheel_rotation_parameter']]['REMAIN']

        arm_rotation_rate_probability = 0
        if state_record['arm_rotation_rate'] == 'NONE' and successor_state_record['arm_rotation_rate'] == 'NONE':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['REMAIN'] + ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['DECREASE']
        elif state_record['arm_rotation_rate'] == 'HIGH' and successor_state_record['arm_rotation_rate'] == 'HIGH':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['REMAIN'] + ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['INCREASE']
        elif state_record['arm_rotation_rate'] == 'NONE' and successor_state_record['arm_rotation_rate'] == 'LOW':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['INCREASE']
        elif state_record['arm_rotation_rate'] == 'LOW' and successor_state_record['arm_rotation_rate'] == 'NORMAL':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['INCREASE']
        elif state_record['arm_rotation_rate'] == 'NORMAL' and successor_state_record['arm_rotation_rate'] == 'HIGH':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['INCREASE']
        elif state_record['arm_rotation_rate'] == 'LOW' and successor_state_record['arm_rotation_rate'] == 'NONE':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['DECREASE']
        elif state_record['arm_rotation_rate'] == 'NORMAL' and successor_state_record['arm_rotation_rate'] == 'LOW':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['DECREASE']
        elif state_record['arm_rotation_rate'] == 'HIGH' and successor_state_record['arm_rotation_rate'] == 'NORMAL':
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['DECREASE']
        elif state_record['arm_rotation_rate'] == successor_state_record['arm_rotation_rate']:
            arm_rotation_rate_probability = ROTATION_RATE_PROBABILITIES[parameter_record['arm_rotation_parameter']]['REMAIN']
        
        wheel_temperature_probability = 0
        if state_record['wheel_motor_temperature'] == MINIMUM_TEMPERATURE and state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature']:
            wheel_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] + TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE']
        elif state_record['wheel_motor_temperature'] == MAXIMUM_TEMPERATURE and state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature']:
            wheel_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] + TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE']
        elif state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] + 1:
            wheel_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE']
        elif state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature']:
            wheel_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN']
        elif state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] - 1:
            wheel_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE']

        arm_temperature_probability = 0
        if state_record['arm_motor_temperature'] == MINIMUM_TEMPERATURE and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            arm_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] + TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE']
        elif state_record['arm_motor_temperature'] == MAXIMUM_TEMPERATURE and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            arm_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] + TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE']
        elif state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] + 1:
            arm_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE']
        elif state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            arm_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN']
        elif state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] - 1:
            arm_temperature_probability = TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE']

        return wheel_rotation_rate_probability * arm_rotation_rate_probability * wheel_temperature_probability * arm_temperature_probability

    def severity_function(self, state, _):
        state_record = self.state_registry[state]
        absolute_wheel_motor_temperature_offset = abs(NOMINAL_TEMPERATURE - state_record['wheel_motor_temperature'])
        absolute_arm_motor_temperature_offset = abs(NOMINAL_TEMPERATURE - state_record['arm_motor_temperature'])
        return max(absolute_wheel_motor_temperature_offset, absolute_arm_motor_temperature_offset)

    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        wheel_rotation_parameter = parameter_record['wheel_rotation_parameter']
        arm_rotation_parameter = parameter_record['arm_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[wheel_rotation_parameter] + INTERFERENCE_MAP[arm_rotation_parameter] + INTERFERENCE_MAP[steering_parameter]

    def start_states(self):
        start_states = []

        for wheel_rotation_rate in WHEEL_ROTATION_RATE:
            for arm_rotation_rate in ARM_ROTATION_RATE:
                start_state = f'{NOMINAL_TEMPERATURE}:{NOMINAL_TEMPERATURE}:{wheel_rotation_rate}:{arm_rotation_rate}'
                start_states.append(start_state)

        return start_states
