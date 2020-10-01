import itertools

MINIMUM_TEMPERATURE = 1
MAXIMUM_TEMPERATURE = 5

WHEEL_MOTOR_TEMPERATURE = range(MINIMUM_TEMPERATURE, MAXIMUM_TEMPERATURE + 1)
ARM_MOTOR_TEMPERATURE = range(MINIMUM_TEMPERATURE, MAXIMUM_TEMPERATURE + 1)

WHEEL_ROTATION_RATE = ['NONE', 'LOW', 'NORMAL', 'HIGH']
ARM_ROTATION_RATE = ['NONE', 'LOW', 'NORMAL', 'HIGH']

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SLOW_DOWN', 'STOP']
ARM_ROTATION_PARAMETERS = ['NONE', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

TEMPERATURE_PROBABILITIES = {
    'NONE': {'DECREASE': 0.8, 'REMAIN': 0.2, 'INCREASE': 0.0},
    'LOW': {'DECREASE': 0.15, 'REMAIN': 0.8, 'INCREASE': 0.05},
    'NORMAL': {'DECREASE': 0.1, 'REMAIN': 0.8, 'INCREASE': 0.1},
    'HIGH': {'DECREASE': 0.05, 'REMAIN': 0.8, 'INCREASE': 0.15}
}

ROTATION_RATE_PROBABILITIES = {
    'NONE': 0.1,
    'LOW': 0.3,
    'NORMAL': 0.5,
    'HIGH': 0.1
}

INTERFERENCE_MAP = {
    'NONE': 0,
    'SLOW_DOWN': 5,
    'STOP': 10,
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

        OverheatingMlc.identifier += 1

    def states(self):
        return list(self.state_registry.keys())

    def parameters(self):
        return list(self.parameter_registry.keys())

    # TODO: Implement the transition function
    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        rotation_rate_probability = ROTATION_RATE_PROBABILITIES[successor_state_record['wheel_rotation_rate']] * ROTATION_RATE_PROBABILITIES[successor_state_record['arm_rotation_rate']]

        temperature_probability = 0
        # Checks if the wheel motor temperature stays the same and the arm motor temperature stays the same
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] * rotation_rate_probability

        # Checks if the wheel motor temperature stays the same and the arm motor temperature increases
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] - 1:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE'] * rotation_rate_probability

        # Checks if the wheel motor temperature increases and the arm motor temperature stays the same
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] - 1 and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] * rotation_rate_probability

        # Checks if the wheel motor temperature increases and the arm motor temperature increases
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] - 1 and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] - 1:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE'] * rotation_rate_probability

        # *** Checks if the wheel motor temperature stays the same and the arm motor temperature decreases
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] + 1:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['REMAIN'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE'] * rotation_rate_probability

        # *** Checks if the wheel motor temperature decreases and the arm motor temperature stays the same
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] + 1 and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature']:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['REMAIN'] * rotation_rate_probability

        # *** Checks if the wheel motor temperature decreases and the arm motor temperature decreases
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] + 1 and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] + 1:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE'] * rotation_rate_probability

        # Checks if the wheel motor temperature increases and the arm motor temperature decreases
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] - 1 and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] + 1:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['INCREASE'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['DECREASE'] * rotation_rate_probability

        # Checks if the wheel motor temperature decreases and the arm motor temperature increases
        if state_record['wheel_motor_temperature'] == successor_state_record['wheel_motor_temperature'] + 1 and state_record['arm_motor_temperature'] == successor_state_record['arm_motor_temperature'] - 1:
            return TEMPERATURE_PROBABILITIES[state_record['wheel_rotation_rate']]['DECREASE'] * TEMPERATURE_PROBABILITIES[state_record['arm_rotation_rate']]['INCREASE'] * rotation_rate_probability

        return 0

    def severity_function(self, state, _):
        state_record = self.state_registry[state]
        maximum_temperature = max(state_record['wheel_motor_temperature'], state_record['arm_motor_temperature'])
        return maximum_temperature

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
                start_state = f'{MINIMUM_TEMPERATURE}:{MINIMUM_TEMPERATURE}:{wheel_rotation_rate}:{arm_rotation_rate}'
                start_states.append(start_state)

        return start_states
