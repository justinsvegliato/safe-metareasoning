import itertools

NOMINAL_TEMPERATURE = 5
MINIMUM_TEMPERATURE = 1
MAXIMUM_TEMPERATURE = 10
ARM_MOTOR_TEMPERATURE = range(MINIMUM_TEMPERATURE, MAXIMUM_TEMPERATURE + 1)

ARM_ROTATION_RATE = ['NONE', 'LOW', 'NORMAL', 'HIGH']

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
ARM_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

MOTOR_TEMPERATURE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.9, 'REMAIN': 0.1, 'INCREASE': 0.0},
    'LOW': {'DECREASE': 0.7, 'REMAIN': 0.3, 'INCREASE': 0.0},
    'NORMAL': {'DECREASE': 0.05, 'REMAIN': 0.9, 'INCREASE': 0.05},
    'HIGH': {'DECREASE': 0.0, 'REMAIN': 0.3, 'INCREASE': 0.7}
}

ROTATION_RATE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.0, 'REMAIN': 1.0, 'INCREASE': 0.0},
    'SPEED_UP': {'DECREASE': 0.0, 'REMAIN': 0.05, 'INCREASE': 0.95},
    'SLOW_DOWN': {'DECREASE': 0.95, 'REMAIN': 0.05, 'INCREASE': 0.0}
}

SEVERITY_MAP = {
    1: 5,
    2: 4,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
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


class ArmMotorTemperatureSafetyProcess:
    identifier = 1

    def __init__(self):
        self.kind = 'arm-motor-temperature-safety-process'
        self.name = f'arm-motor-temperature-safety-process-{ArmMotorTemperatureSafetyProcess.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product(ARM_MOTOR_TEMPERATURE, ARM_ROTATION_RATE):
            state = ':'.join((str(state_factor) for state_factor in state_tuple))
            self.state_registry[state] = {
                'arm_motor_temperature': state_tuple[0],
                'arm_rotation_rate': state_tuple[1]
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

        ArmMotorTemperatureSafetyProcess.identifier += 1

    def states(self):
        return self.state_space

    def parameters(self):
        return self.parameter_space

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        arm_rotation_rate_probability = 0
        if parameter_record['arm_rotation_parameter'] == 'STOP':
            arm_rotation_rate_probability = 1 if successor_state_record['arm_rotation_rate'] == 'NONE' else 0
        elif state_record['arm_rotation_rate'] == 'NONE' and successor_state_record['arm_rotation_rate'] == 'NONE':
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

        arm_temperature_probability = 0
        if state_record['arm_motor_temperature'] == MINIMUM_TEMPERATURE and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            arm_temperature_probability = MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] + MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE']
        elif state_record['arm_motor_temperature'] == MAXIMUM_TEMPERATURE and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            arm_temperature_probability = MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] + MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE']
        elif state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] + 1:
            arm_temperature_probability = MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE']
        elif state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            arm_temperature_probability = MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN']
        elif state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] - 1:
            arm_temperature_probability = MOTOR_TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE']

        return arm_rotation_rate_probability * arm_temperature_probability

    def severity_function(self, state, _):
        arm_motor_temperature = self.state_registry[state]['arm_motor_temperature']
        return SEVERITY_MAP[arm_motor_temperature]

    # TODO: Should wheel motor temperature be included in this?
    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        arm_rotation_parameter = parameter_record['arm_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[arm_rotation_parameter] + INTERFERENCE_MAP[steering_parameter]

    def start_states(self):
        return [f'{NOMINAL_TEMPERATURE}:NORMAL']