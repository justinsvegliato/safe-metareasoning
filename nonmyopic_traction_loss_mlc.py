import itertools

ROAD_POSITION = ['NONE', 'APPROACHING', 'AT']
LANE_POSITION = ['NONE', 'LEFT', 'CENTER', 'RIGHT']
VEHICLE_SPEED = ['LOW', 'NORMAL', 'HIGH']
VEHICLE_OFFSET = ['LEFT', 'CENTER', 'RIGHT']

SPEED_PARAMETERS = ['NONE', 'SLOW_DOWN']
LOCATION_PARAMETERS = ['NONE', 'SHIFT_LEFT', 'SHIFT_RIGHT']

APPROACHING_PROBABILITY = 0.2
AT_PROBABILITY = 0.5
PASS_PROBABILITY = 0.5

LANE_POSITION_PROBABILITIES = {
    'NONE': 0.0,
    'LEFT': 0.25,
    'CENTER': 0.5,
    'RIGHT': 0.25
}

SPEED_PROBABILITIES = {
    'NONE': {
        'LOW': 0.25,
        'NORMAL': 0.5,
        'HIGH': 0.25
    },
    'SLOW_DOWN': {
        'LOW': 1.0,
        'NORMAL': 0.0,
        'HIGH': 0.0
    }
}
VEHICLE_OFFSET_PROBABILITIES = {
    'NONE': {
        'LEFT': 0.25,
        'CENTER': 0.5,
        'RIGHT': 0.25
    },
    'SHIFT_LEFT': {
        'LEFT': 1.0,
        'CENTER': 0.0,
        'RIGHT': 0.0
    },
    'SHIFT_RIGHT': {
        'LEFT': 0.0,
        'CENTER': 0.0,
        'RIGHT': 1.0
    }
}


class TractionLossMlc:
    def __init__(self):
        self.name = 'TRACTION_LOSS'

        self.state_registry = {}
        for state_tuple in itertools.product(ROAD_POSITION, LANE_POSITION, VEHICLE_SPEED, VEHICLE_OFFSET):
            state = ':'.join(state_tuple)
            self.state_registry[state] = {
                'road_position': state_tuple[0],
                'lane_position': state_tuple[1],
                'vehicle_speed': state_tuple[2],
                'vehicle_offset': state_tuple[3]
            }

        self.parameter_registry = {}
        for parameter_tuple in itertools.product(SPEED_PARAMETERS, LOCATION_PARAMETERS):
            parameter = ':'.join(parameter_tuple)
            self.parameter_registry[parameter] = {
                'speed_parameter': parameter_tuple[0],
                'location_parameter': parameter_tuple[1]
            }

    def states(self):
        return list(self.state_registry.keys())

    def parameters(self):
        return list(self.parameter_registry.keys())

    def transition_function(self, state, parameter, successor_state):
        state_record = self.state_registry[state]
        parameter_record = self.parameter_registry[parameter]
        successor_state_record = self.state_registry[successor_state]

        if state_record['road_position'] == 'NONE' and state_record['lane_position'] != 'NONE':
            return 1 if state == successor_state else 0

        if state_record['road_position'] != 'NONE' and state_record['lane_position'] == 'NONE':
            return 1 if state == successor_state else 0

        if state_record['road_position'] == 'NONE':
            if successor_state_record['road_position'] == 'NONE' and successor_state_record['lane_position'] == 'NONE':
                return (1 - APPROACHING_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['speed_parameter']][successor_state_record['vehicle_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['location_parameter']][successor_state_record['vehicle_offset']]

            if successor_state_record['road_position'] == 'APPROACHING':
                return APPROACHING_PROBABILITY * LANE_POSITION_PROBABILITIES[successor_state_record['lane_position']] * SPEED_PROBABILITIES[parameter_record['speed_parameter']][successor_state_record['vehicle_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['location_parameter']][successor_state_record['vehicle_offset']]

            return 0

        if state_record['road_position'] == 'APPROACHING':
            if successor_state_record['road_position'] == 'APPROACHING' and state_record['lane_position'] == successor_state_record['lane_position']:
                return (1 - AT_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['speed_parameter']][successor_state_record['vehicle_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['location_parameter']][successor_state_record['vehicle_offset']]

            if successor_state_record['road_position'] == 'AT' and state_record['lane_position'] == successor_state_record['lane_position']:
                return AT_PROBABILITY * SPEED_PROBABILITIES[parameter_record['speed_parameter']][successor_state_record['vehicle_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['location_parameter']][successor_state_record['vehicle_offset']]

            return 0

        if state_record['road_position'] == 'AT':
            if successor_state_record['road_position'] == 'AT' and state_record['lane_position'] == successor_state_record['lane_position']:
                return (1 - PASS_PROBABILITY) * SPEED_PROBABILITIES[parameter_record['speed_parameter']][successor_state_record['vehicle_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['location_parameter']][successor_state_record['vehicle_offset']]

            if successor_state_record['road_position'] == 'NONE' and successor_state_record['lane_position'] == 'NONE':
                return PASS_PROBABILITY * SPEED_PROBABILITIES[parameter_record['speed_parameter']][successor_state_record['vehicle_speed']] * VEHICLE_OFFSET_PROBABILITIES[parameter_record['location_parameter']][successor_state_record['vehicle_offset']]

            return 0

        return 1

    def severity_function(self, state, _):
        state_record = self.state_registry[state]

        if state_record['road_position'] == 'APPROACHING':
            if state_record['lane_position'] == state_record['vehicle_offset']:
                if state_record['vehicle_speed'] == 'LOW':
                    return 1
                if state_record['vehicle_speed'] == 'NORMAL':
                    return 2
                if state_record['vehicle_speed'] == 'HIGH':
                    return 3

        if state_record['road_position'] == 'AT':
            if state_record['lane_position'] == state_record['vehicle_offset']:
                if state_record['vehicle_speed'] == 'LOW':
                    return 2
                if state_record['vehicle_speed'] == 'NORMAL':
                    return 3
                if state_record['vehicle_speed'] == 'HIGH':
                    return 4

        return 1

    def interference_function(self, state, _):
        state_record = self.state_registry[state]

        if state_record['vehicle_speed'] == 'LOW':
            return 10

        if state_record['vehicle_speed'] == 'NORMAL':
            return 0

        if state_record['vehicle_speed'] == 'HIGH':
            return 10

        return 0
