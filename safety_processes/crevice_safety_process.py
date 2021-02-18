import itertools

HORIZONTAL_CREVICE_POSITION = ['NONE', 'APPROACHING', 'AT']
VERTICAL_CREVICE_POSITION = ['NONE', 'LEFT', 'CENTER', 'RIGHT']
ROVER_SPEED = ['NONE', 'LOW', 'NORMAL', 'HIGH']
ROVER_OFFSET = ['LEFT', 'CENTER', 'RIGHT']

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

APPROACHING_PROBABILITY = 0.2
AT_PROBABILITY = 0.5
PASS_PROBABILITY = 0.5

VERTICAL_OBSTACLE_POSITION_PROBABILITIES = {
    'NONE': 0.0,
    'LEFT': 0.25,
    'CENTER': 0.5,
    'RIGHT': 0.25
}

SPEED_PROBABILITIES = {
    'NONE': {'NONE': 0.1, 'LOW': 0.1, 'NORMAL': 0.7, 'HIGH': 0.1},
    'SPEED_UP': {'NONE': 0.0, 'LOW': 0.0, 'NORMAL': 0.0, 'HIGH': 1.0},
    'SLOW_DOWN': {'NONE': 0.0, 'LOW': 1.0, 'NORMAL': 0.0, 'HIGH': 0.0},
    'STOP': {'NONE': 1.0, 'LOW': 0.0, 'NORMAL': 0.0, 'HIGH': 0.0}
}
VEHICLE_OFFSET_PROBABILITIES = {
    'NONE': {'LEFT': 0.05, 'CENTER': 0.9, 'RIGHT': 0.05},
    'SHIFT_LEFT': {'LEFT': 1.0, 'CENTER': 0.0, 'RIGHT': 0.0},
    'SHIFT_RIGHT': {'LEFT': 0.0, 'CENTER': 0.0, 'RIGHT': 1.0}
}

SEVERITY_MAP = {
    'LEFT': {
        'NONE': {'LEFT': 1, 'CENTER': 1, 'RIGHT': 1},
        'LOW': {'LEFT': 4, 'CENTER': 2, 'RIGHT': 1},
        'NORMAL': {'LEFT': 5, 'CENTER': 3, 'RIGHT': 1},
        'HIGH': {'LEFT': 5, 'CENTER': 3, 'RIGHT': 1}
    },
    'CENTER': {
        'NONE': {'LEFT': 1, 'CENTER': 1, 'RIGHT': 1},
        'LOW': {'LEFT': 1, 'CENTER': 4, 'RIGHT': 1},
        'NORMAL': {'LEFT': 3, 'CENTER': 5, 'RIGHT': 3},
        'HIGH': {'LEFT': 3, 'CENTER': 5, 'RIGHT': 3}
    },
    'RIGHT': {
        'NONE': {'LEFT': 1, 'CENTER': 1, 'RIGHT': 1},
        'LOW': {'LEFT': 1, 'CENTER': 2, 'RIGHT': 4},
        'NORMAL': {'LEFT': 1, 'CENTER': 3, 'RIGHT': 5},
        'HIGH': {'LEFT': 1, 'CENTER': 3, 'RIGHT': 5}
    }
}

INTERFERENCE_MAP = {
    'NONE': {'NONE': 0, 'SHIFT_LEFT': 10, 'SHIFT_RIGHT': 10},
    'SPEED_UP': {'NONE': 5, 'SHIFT_LEFT': 15, 'SHIFT_RIGHT': 15},
    'SLOW_DOWN': {'NONE': 5, 'SHIFT_LEFT': 15, 'SHIFT_RIGHT': 15},
    'STOP': {'NONE': 20, 'SHIFT_LEFT': 25, 'SHIFT_RIGHT': 30},
}


class CreviceSafetyProcess:
    identifier = 1

    def __init__(self):
        self.kind = 'crevice-safety-process'
        self.name = f'crevice-safety-process-{CreviceSafetyProcess.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product(HORIZONTAL_CREVICE_POSITION, VERTICAL_CREVICE_POSITION, ROVER_SPEED, ROVER_OFFSET):
            state = ':'.join(state_tuple)
            self.state_registry[state] = {
                'horizontal_crevice_position': state_tuple[0],
                'vertical_crevice_position': state_tuple[1],
                'rover_speed': state_tuple[2],
                'rover_offset': state_tuple[3]
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

        CreviceSafetyProcess.identifier += 1

    def states(self):
        return self.state_space

    def parameters(self):
        return self.parameter_space

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        if state_record['horizontal_crevice_position'] == 'NONE' and state_record['vertical_crevice_position'] != 'NONE':
            return 1 if state == successor_state else 0

        if state_record['horizontal_crevice_position'] != 'NONE' and state_record['vertical_crevice_position'] == 'NONE':
            return 1 if state == successor_state else 0

        if state_record['horizontal_crevice_position'] == 'NONE':
            if successor_state_record['horizontal_crevice_position'] == 'NONE' and successor_state_record['vertical_crevice_position'] == 'NONE':
                return (1 - APPROACHING_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['steering_parameter']][successor_state_record['rover_offset']]

            if successor_state_record['horizontal_crevice_position'] == 'APPROACHING':
                return APPROACHING_PROBABILITY * VERTICAL_OBSTACLE_POSITION_PROBABILITIES[successor_state_record['vertical_crevice_position']] * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['steering_parameter']][successor_state_record['rover_offset']]

            return 0

        if state_record['horizontal_crevice_position'] == 'APPROACHING':
            if successor_state_record['horizontal_crevice_position'] == 'APPROACHING' and state_record['vertical_crevice_position'] == successor_state_record['vertical_crevice_position']:
                return (1 - AT_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['steering_parameter']][successor_state_record['rover_offset']]

            if successor_state_record['horizontal_crevice_position'] == 'AT' and state_record['vertical_crevice_position'] == successor_state_record['vertical_crevice_position']:
                return AT_PROBABILITY * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['steering_parameter']][successor_state_record['rover_offset']]

            return 0

        if state_record['horizontal_crevice_position'] == 'AT':
            if successor_state_record['horizontal_crevice_position'] == 'AT' and state_record['vertical_crevice_position'] == successor_state_record['vertical_crevice_position']:
                return (1 - PASS_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['steering_parameter']][successor_state_record['rover_offset']]

            if successor_state_record['horizontal_crevice_position'] == 'NONE' and successor_state_record['vertical_crevice_position'] == 'NONE':
                return PASS_PROBABILITY * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['steering_parameter']][successor_state_record['rover_offset']]

            return 0

        return 1

    def severity_function(self, state, _):
        state_record = self.state_registry[state]

        if state_record['horizontal_crevice_position'] == 'AT' and state_record['vertical_crevice_position'] != 'NONE':
            vertical_crevice_position = state_record['vertical_crevice_position']
            rover_speed = state_record['rover_speed']
            rover_offset = state_record['rover_offset']
            return SEVERITY_MAP[vertical_crevice_position][rover_speed][rover_offset]

        return 1

    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        wheel_rotation_parameter = parameter_record['wheel_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[wheel_rotation_parameter][steering_parameter]

    def start_states(self):
        start_states = []

        for vehicle_speed in ROVER_SPEED:
            for vehicle_offset in ROVER_OFFSET:
                start_state = f'NONE:NONE:{vehicle_speed}:{vehicle_offset}'
                start_states.append(start_state)

        return start_states
