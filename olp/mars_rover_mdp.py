import itertools

TERRAIN_TYPES = {
    'W': 'IMPASSABLE',
    'O': 'NORMAL'
}
TERRAIN_STATUS = ['NOT_ANALYZED', 'ANALYZED']

# TODO: Fix the bug when you change this to 10
MAXIMUM_BATTERY_LEVEL = 10
BATTERY_LEVELS = range(0, MAXIMUM_BATTERY_LEVEL + 1)

WATER_ANALYZER_HEALTH = ['NOMINAL', 'ERROR']
SOIL_ANALYZER_HEALTH = ['NOMINAL', 'ERROR']

WEATHER = ['SUNNY', 'SHADY']

BREAK_PROBABILITIES = {
    'NOMINAL': {
        'NOMINAL': 0.95,
        'ERROR': 0.05
    },
    'ERROR': {
        'NOMINAL': 0.0,
        'ERROR': 1.0
    },
}

MOVE_DETAILS = {
    'NORTH': {
        'is_at_boundary': lambda row, column, grid_world: row == 0 or grid_world[row - 1][column] == 'W',
        'is_valid_move': lambda row, successor_row, column, successor_column: row == successor_row + 1 and column == successor_column
    },
    'EAST': {
        'is_at_boundary': lambda row, column, grid_world: column == len(grid_world[row]) - 1 or grid_world[row][column + 1] == 'W',
        'is_valid_move': lambda row, successor_row, column, successor_column: row == successor_row and column == successor_column - 1
    },
    'SOUTH': {
        'is_at_boundary': lambda row, column, grid_world: row == len(grid_world) - 1 or grid_world[row + 1][column] == 'W',
        'is_valid_move': lambda row, successor_row, column, successor_column: row == successor_row - 1 and column == successor_column
    },
    'WEST': {
        'is_at_boundary': lambda row, column, grid_world: column == 0 or grid_world[row][column - 1] == 'W',
        'is_valid_move': lambda row, successor_row, column, successor_column: row == successor_row and column == successor_column + 1
    }
}


class MarsRoverMdp:
    def __init__(self, grid_world, target_locations, weather_status):
        self.grid_world = grid_world
        self.width = len(grid_world[0])
        self.height = len(grid_world)
        self.rows = range(self.height)
        self.cols = range(self.width)

        self.target_locations = target_locations

        terrain_statuses = [TERRAIN_STATUS for target_location in target_locations]

        self.state_registry = {}
        for state_tuple in itertools.product(self.rows, self.cols, BATTERY_LEVELS, WATER_ANALYZER_HEALTH, SOIL_ANALYZER_HEALTH, *terrain_statuses):
            state = ':'.join(str(entry) for entry in state_tuple)
            self.state_registry[state] = {
                'row': state_tuple[0],
                'column': state_tuple[1],
                'terrain_type': TERRAIN_TYPES[grid_world[state_tuple[0]][state_tuple[1]]],
                'weather_status': 'SHADY' if (state_tuple[0], state_tuple[1]) in weather_status else 'SUNNY',
                'battery_level': state_tuple[2],
                'water_analyzer_health': state_tuple[3],
                'soil_analyzer_health': state_tuple[4],
                'terrain_statuses': {self.target_locations[i]: state_tuple[5 + i] for i in range(len(terrain_statuses))}
            }
        self.state_registry['SLEEP_MODE'] = {
            'row': float('inf'),
            'column': float('inf'),
            'terrain_type': None,
            'weather_status': None,
            'battery_level': float('inf'),
            'water_analyzer_health': None,
            'soil_analyzer_health': None,
            'terrain_statuses': None
        }

    def states(self):
        return list(self.state_registry)

    def actions(self):
        return list(MOVE_DETAILS) + ['REBOOT', 'TRANSMIT', 'CHARGE', 'ANALYZE']

    def transition_function(self, state, action, successor_state):
        if state == 'SLEEP_MODE' and successor_state == 'SLEEP_MODE':
            return 1
        if state != 'SLEEP_MODE' and successor_state == 'SLEEP_MODE' and action != 'TRANSMIT':
            return 0
        if state == 'SLEEP_MODE' and successor_state != 'SLEEP_MODE':
            return 0

        record = self.state_registry[state]
        successor_record = self.state_registry[successor_state]

        # TODO: Delete all of these later
        row = record['row']
        column = record['column']
        successor_row = successor_record['row']
        successor_column = successor_record['column']
        battery_level = record['battery_level']
        successor_battery_level = successor_record['battery_level']
        water_analyzer_health = record['water_analyzer_health']
        successor_water_analyzer_health = successor_record['water_analyzer_health']
        soil_analyzer_health = record['soil_analyzer_health']
        successor_soil_analyzer_health = successor_record['soil_analyzer_health']
        terrain_statuses = record['terrain_statuses']
        successor_terrain_statuses = successor_record['terrain_statuses']
        weather_status = record['weather_status']

        # Loop for every action other than the CHARGE action if the rover ran out of battery
        if battery_level == 0 and record == successor_record and successor_state != 'SLEEP_MODE':
            return 1

        # Ensure that every action other than the CHARGE action decrements the battery level
        if action != 'CHARGE' and battery_level != successor_battery_level + 1 and successor_state != 'SLEEP_MODE':
            return 0

        # Ensure that every action other than the ANALYZE action does not alter any terrain status
        if action != 'ANALYZE' and terrain_statuses != successor_terrain_statuses and successor_state != 'SLEEP_MODE':
            return 0

        if battery_level > 0:
            if action in MOVE_DETAILS:
                is_at_boundary = MOVE_DETAILS[action]['is_at_boundary'](row, column, self.grid_world)
                if is_at_boundary and row == successor_row and column == successor_column:
                    return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

                # TODO: Confirm that this legacy code does anything
                if self.grid_world[successor_row][successor_column] == 'W':
                    return 0

                is_valid_move = MOVE_DETAILS[action]['is_valid_move'](row, successor_row, column, successor_column)
                if is_valid_move:
                    return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

            if action == 'REBOOT':
                if row == successor_row and column == successor_column and successor_water_analyzer_health == 'NOMINAL' and successor_soil_analyzer_health == 'NOMINAL':
                    return 1

            if action == 'TRANSMIT':
                # print('here')
                # if row == successor_row and column == successor_column:
                # print(successor_state)
                    # return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]
                if successor_state == 'SLEEP_MODE':
                    return 1

            if action == 'CHARGE':
                if row == successor_row and column == successor_column:
                    if (battery_level == successor_battery_level - 1 or battery_level == MAXIMUM_BATTERY_LEVEL and successor_battery_level == MAXIMUM_BATTERY_LEVEL) and weather_status == 'SUNNY':
                        return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]
                    if battery_level == successor_battery_level and weather_status == 'SHADY':
                        return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

            if action == 'ANALYZE':
                if row == successor_row and column == successor_column:
                    if (row, column) in successor_terrain_statuses and water_analyzer_health == 'NOMINAL' and soil_analyzer_health == 'NOMINAL':
                        terrain_statuses_copy = terrain_statuses.copy()
                        terrain_statuses_copy[(row, column)] = 'ANALYZED'
                        if terrain_statuses_copy == successor_terrain_statuses:
                            return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]
                    if terrain_statuses == successor_terrain_statuses and ((row, column) not in successor_terrain_statuses or water_analyzer_health != 'NOMINAL' or soil_analyzer_health != 'NOMINAL'):
                        return BREAK_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * BREAK_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

        return 0

    def reward_function(self, state, action):
        state_record = self.state_registry[state]

        terrain_statuses = state_record['terrain_statuses']
        battery_level = state_record['battery_level']
        target_terrain_statuses = {target_location: 'ANALYZED' for target_location in self.target_locations}

        if terrain_statuses == target_terrain_statuses and action == 'TRANSMIT' and battery_level > 0:
            return 100

        return 0

    def start_state_function(self, state):
        start_states = []

        for state_id in self.state_registry:
            state_record = self.state_registry[state_id]

            terrain_type = state_record['terrain_type']
            battery_level = state_record['battery_level']
            water_analyzer_health = state_record['water_analyzer_health']
            soil_analyzer_health = state_record['soil_analyzer_health']
            terrain_statuses = state_record['terrain_statuses']

            if terrain_type != 'IMPASSABLE' and battery_level == MAXIMUM_BATTERY_LEVEL \
                and water_analyzer_health == 'NOMINAL' and soil_analyzer_health == 'NOMINAL' \
                and terrain_statuses == {target_location: 'NOT_ANALYZED' for target_location in self.target_locations}:
                start_states.append(state_id)

        return 1.0 / len(start_states) if state in start_states else 0
