import itertools

HORIZONTAL_ROUGH_TERRAIN_POSITION = ['NONE', 'APPROACHING', 'AT']
ROVER_SPEED = ['NONE', 'LOW', 'NORMAL', 'HIGH']

NOMINAL_TERRAIN_LEVEL = 8
MINIMUM_TERRAIN_LEVEL = 1
MAXIMUM_TERRAIN_LEVEL = 10
ROUGH_TERRAIN_LEVEL = range(MINIMUM_TERRAIN_LEVEL, MAXIMUM_TERRAIN_LEVEL + 1)

ROUGH_TERRAIN_LEVEL_PROBABILITY = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0.15,
    8: 0.7,
    9: 0.1,
    10: 0.05
}

WHEEL_ROTATION_PARAMETERS = ['NONE', 'SPEED_UP', 'SLOW_DOWN', 'STOP']
STEERING_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

APPROACHING_PROBABILITY = 0.5
AT_PROBABILITY = 0.5
PASS_PROBABILITY = 0.2

SPEED_PROBABILITIES = {
    'NONE': {'NONE': 0.1, 'LOW': 0.1, 'NORMAL': 0.7, 'HIGH': 0.1},
    'SPEED_UP': {'NONE': 0.0, 'LOW': 0.0, 'NORMAL': 0.0, 'HIGH': 1.0},
    'SLOW_DOWN': {'NONE': 0.0, 'LOW': 0.6, 'NORMAL': 0.4, 'HIGH': 0.0},
    'STOP': {'NONE': 0.0, 'LOW': 0.0, 'NORMAL': 0.0, 'HIGH': 1.0}
}

ROUGH_TERRAIN_INCREASE_PROBABILITY = 0.2
ROUGH_TERRAIN_REMAIN_PROBABILITY = 0.6
ROUGH_TERRAIN_DECREASE_PROBABILITY = 0.2

ROVER_SPEED_SEVERITY_MAP = {
    'NONE': {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1
    },
    'LOW': {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1
    },
    'NORMAL': {
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
    },
    'HIGH': {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 2,
        7: 3,
        8: 4,
        9: 5,
        10: 5
    }
}

INTERFERENCE_MAP = {
    'NONE': 0,
    'SPEED_UP': 0.05,
    'SLOW_DOWN': 0.15,
    'STOP': 0.25,
    'SHIFT_LEFT': 0.1,
    'SHIFT_RIGHT': 0.1
}

class RoughTerrainSafetyProcess:
    identifier = 1

    def __init__(self):
        self.safety_problem = 'rough-terrain'
        self.kind = 'rough-terrain-safety-process'
        self.name = f'rough-terrain-safety-process-{RoughTerrainSafetyProcess.identifier}'

        self.state_registry = {}
        for state_tuple in itertools.product(HORIZONTAL_ROUGH_TERRAIN_POSITION, ROVER_SPEED, ROUGH_TERRAIN_LEVEL):
            state = ':'.join((str(state_factor) for state_factor in state_tuple))
            self.state_registry[state] = {
                'horizontal_rough_terrain_position': state_tuple[0],
                'rover_speed': state_tuple[1],
                'rough_terrain_level': state_tuple[2]
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
 
        if state_record['horizontal_rough_terrain_position'] == 'NONE' and state_record['rough_terrain_level'] != NOMINAL_TERRAIN_LEVEL:
            return 1 if state == successor_state else 0

        # if state_record['horizontal_rough_terrain_position'] != 'NONE' and state_record['rough_terrain_level'] == NOMINAL_TERRAIN_LEVEL:
        #     return 1 if state == successor_state else 0

        if state_record['horizontal_rough_terrain_position'] == 'NONE':
            if successor_state_record['horizontal_rough_terrain_position'] == 'NONE' and successor_state_record['rough_terrain_level'] == NOMINAL_TERRAIN_LEVEL:
                return (1 - APPROACHING_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']]

            if successor_state_record['horizontal_rough_terrain_position'] == 'APPROACHING':
                return APPROACHING_PROBABILITY * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * ROUGH_TERRAIN_LEVEL_PROBABILITY[successor_state_record['rough_terrain_level']]

            return 0

        rough_terrain_level_probability = 0
        if state_record['rough_terrain_level'] == MINIMUM_TERRAIN_LEVEL and state_record['rough_terrain_level'] == successor_state_record['rough_terrain_level']:
            rough_terrain_level_probability = ROUGH_TERRAIN_REMAIN_PROBABILITY + ROUGH_TERRAIN_DECREASE_PROBABILITY
        elif state_record['rough_terrain_level'] == MAXIMUM_TERRAIN_LEVEL and state_record['rough_terrain_level'] == successor_state_record['rough_terrain_level']:
            rough_terrain_level_probability = ROUGH_TERRAIN_REMAIN_PROBABILITY + ROUGH_TERRAIN_INCREASE_PROBABILITY
        elif state_record['rough_terrain_level'] == successor_state_record['rough_terrain_level'] + 1:
            rough_terrain_level_probability = ROUGH_TERRAIN_DECREASE_PROBABILITY
        elif state_record['rough_terrain_level'] == successor_state_record['rough_terrain_level']:
            rough_terrain_level_probability = ROUGH_TERRAIN_REMAIN_PROBABILITY
        elif state_record['rough_terrain_level'] == successor_state_record['rough_terrain_level'] - 1:
            rough_terrain_level_probability = ROUGH_TERRAIN_INCREASE_PROBABILITY

        if state_record['horizontal_rough_terrain_position'] == 'APPROACHING':
            if successor_state_record['horizontal_rough_terrain_position'] == 'APPROACHING':
                return (1 - AT_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * rough_terrain_level_probability

            if successor_state_record['horizontal_rough_terrain_position'] == 'AT':
                return AT_PROBABILITY * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * rough_terrain_level_probability

            return 0

        if state_record['horizontal_rough_terrain_position'] == 'AT':
            if successor_state_record['horizontal_rough_terrain_position'] == 'AT':
                return (1 - PASS_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * rough_terrain_level_probability

            if successor_state_record['horizontal_rough_terrain_position'] == 'NONE':
                return PASS_PROBABILITY * SPEED_PROBABILITIES[parameter_record['wheel_rotation_parameter']][successor_state_record['rover_speed']] * rough_terrain_level_probability

            return 0

        return 1

    def severity_function(self, state, _):
        horizontal_rough_terrain_position = self.state_registry[state]['horizontal_rough_terrain_position']
        rough_terrain_level = self.state_registry[state]['rough_terrain_level']
        rover_speed = self.state_registry[state]['rover_speed']

        if horizontal_rough_terrain_position == 'AT':
            return ROVER_SPEED_SEVERITY_MAP[rover_speed][rough_terrain_level]

        return 1

    def interference_function(self, _, parameter):
        parameter_record = self.parameter_registry[parameter]
        wheel_rotation_parameter = parameter_record['wheel_rotation_parameter']
        steering_parameter = parameter_record['steering_parameter']
        return INTERFERENCE_MAP[wheel_rotation_parameter] + INTERFERENCE_MAP[steering_parameter]

    def start_states(self):
        start_states = []

        for vehicle_speed in ROVER_SPEED:
            start_state = f'NONE:{vehicle_speed}:{NOMINAL_TERRAIN_LEVEL}'
            start_states.append(start_state)

        return start_states
