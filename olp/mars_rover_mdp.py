import itertools

TERRAIN_TYPES = {'W': 'IMPASSABLE', 'O': 'NORMAL'}

WEATHER = ['SUNNY', 'SHADY']

# TODO: Fix the bug when you change this to 10
MAXIMUM_BATTERY_LEVEL = 10
BATTERY_LEVELS = range(0, MAXIMUM_BATTERY_LEVEL + 1)

WATER_ANALYZER_HEALTH = ['NOMINAL', 'ERROR']
SOIL_ANALYZER_HEALTH = ['NOMINAL', 'ERROR']
ANALYZER_HEALTH_PROBABILITIES = {
    'NOMINAL': {'NOMINAL': 0.95, 'ERROR': 0.05},
    'ERROR': {'NOMINAL': 0.0, 'ERROR': 1.0},
}
ANALYSIS_CONDITIONS = ['NOT_ANALYZED', 'ANALYZED']

GOAL_STATE = 'SLEEP_MODE'

# TODO: Remove references to the grid world
MOVEMENT_ACTION_DETAILS = {
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
STATIONARY_ACTIONS = ['REBOOT', 'TRANSMIT', 'CHARGE', 'ANALYZE']


class MarsRoverMdp:
    def __init__(self, grid_world, point_of_interests, shady_locations):
        self.grid_world = grid_world
        self.width = len(grid_world[0])
        self.height = len(grid_world)

        self.point_of_interests = point_of_interests

        rows = range(self.height)
        cols = range(self.width)
        analysis_status = [ANALYSIS_CONDITIONS for _ in point_of_interests]
        state_tuples = itertools.product(rows, cols, BATTERY_LEVELS, WATER_ANALYZER_HEALTH, SOIL_ANALYZER_HEALTH, *analysis_status)

        self.state_registry = {}
        for state_tuple in state_tuples:
            state = ':'.join(str(state_factor) for state_factor in state_tuple)
            self.state_registry[state] = {
                'row': state_tuple[0],
                'column': state_tuple[1],
                'terrain_type': TERRAIN_TYPES[grid_world[state_tuple[0]][state_tuple[1]]],
                'weather': 'SHADY' if (state_tuple[0], state_tuple[1]) in shady_locations else 'SUNNY',
                'battery_level': state_tuple[2],
                'water_analyzer_health': state_tuple[3],
                'soil_analyzer_health': state_tuple[4],
                'analysis_status': {self.point_of_interests[i]: state_tuple[5 + i] for i in range(len(self.point_of_interests))},
                'is_point_of_interest': (state_tuple[0], state_tuple[1]) in self.point_of_interests
            }

        self.state_registry[GOAL_STATE] = {
            'row': float('inf'),
            'column': float('inf'),
            'terrain_type': None,
            'weather': None,
            'battery_level': float('inf'),
            'water_analyzer_health': None,
            'soil_analyzer_health': None,
            'analysis_status': None,
            'is_point_of_interest': False
        }

        self.state_space = list(self.state_registry)
        self.action_space = list(MOVEMENT_ACTION_DETAILS) + STATIONARY_ACTIONS

    def states(self):
        return self.state_space

    def actions(self):
        return self.action_space

    def transition_function(self, state, action, successor_state):
        if state == GOAL_STATE and successor_state == GOAL_STATE:
            return 1

        if state != GOAL_STATE and successor_state == GOAL_STATE and action != 'TRANSMIT':
            return 0

        state_record = self.state_registry[state]
        row = state_record['row']
        column = state_record['column']
        battery_level = state_record['battery_level']
        water_analyzer_health = state_record['water_analyzer_health']
        soil_analyzer_health = state_record['soil_analyzer_health']
        analysis_status = state_record['analysis_status']
        weather = state_record['weather']

        state_successor_record = self.state_registry[successor_state]
        successor_row = state_successor_record['row']
        successor_column = state_successor_record['column']
        successor_battery_level = state_successor_record['battery_level']
        successor_water_analyzer_health = state_successor_record['water_analyzer_health']
        successor_soil_analyzer_health = state_successor_record['soil_analyzer_health']
        successor_analysis_status = state_successor_record['analysis_status']

        # Loop for every action other than the CHARGE action if the rover ran out of battery
        if battery_level == 0 and state_record == state_successor_record:
            return 1

        # Ensure that every action other than the CHARGE action decrements the battery level
        if action != 'CHARGE' and battery_level != successor_battery_level + 1 and successor_state != GOAL_STATE:
            return 0

        # Ensure that every action other than the ANALYZE action does not alter any analysis status
        if action != 'ANALYZE' and analysis_status != successor_analysis_status and successor_state != GOAL_STATE:
            return 0

        if battery_level > 0:
            if action in MOVEMENT_ACTION_DETAILS:
                is_at_boundary = MOVEMENT_ACTION_DETAILS[action]['is_at_boundary'](row, column, self.grid_world)
                if is_at_boundary and row == successor_row and column == successor_column:
                    return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

                # TODO: Confirm that this legacy code does anything
                if self.grid_world[successor_row][successor_column] == 'W':
                    return 0

                is_valid_move = MOVEMENT_ACTION_DETAILS[action]['is_valid_move'](row, successor_row, column, successor_column)
                if is_valid_move:
                    return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

            if action == 'REBOOT':
                if row == successor_row and column == successor_column and successor_water_analyzer_health == 'NOMINAL' and successor_soil_analyzer_health == 'NOMINAL':
                    return 1

            if action == 'TRANSMIT':
                if successor_state == GOAL_STATE:
                    return 1

            if action == 'CHARGE':
                if row == successor_row and column == successor_column:
                    if (battery_level == successor_battery_level - 1 or battery_level == MAXIMUM_BATTERY_LEVEL and successor_battery_level == MAXIMUM_BATTERY_LEVEL) and weather == 'SUNNY':
                        return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]
                    if battery_level == successor_battery_level and weather == 'SHADY':
                        return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

            # TODO: Look at analysis status here
            if action == 'ANALYZE':
                if row == successor_row and column == successor_column:
                    if (row, column) in successor_analysis_status and water_analyzer_health == 'NOMINAL' and soil_analyzer_health == 'NOMINAL':
                        analysis_status = analysis_status.copy()
                        analysis_status[(row, column)] = 'ANALYZED'
                        if analysis_status == successor_analysis_status:
                            return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]
                    if analysis_status == successor_analysis_status and ((row, column) not in successor_analysis_status or water_analyzer_health != 'NOMINAL' or soil_analyzer_health != 'NOMINAL'):
                        return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

        return 0

    def reward_function(self, state, action):
        state_record = self.state_registry[state]
        analysis_status = state_record['analysis_status']
        battery_level = state_record['battery_level']

        target_analysis_status = {point_of_interest: 'ANALYZED' for point_of_interest in self.point_of_interests}

        if battery_level > 0 and action == 'TRANSMIT' and analysis_status == target_analysis_status:
            return 100

        return 0

    def start_state_function(self, state):
        start_states = []

        for start_state in self.state_registry:
            state_record = self.state_registry[start_state]
            terrain_type = state_record['terrain_type']
            battery_level = state_record['battery_level']
            water_analyzer_health = state_record['water_analyzer_health']
            soil_analyzer_health = state_record['soil_analyzer_health']
            analysis_status = state_record['analysis_status']

            is_passable = terrain_type != 'IMPASSABLE'
            is_fully_charged = battery_level == MAXIMUM_BATTERY_LEVEL
            are_analyzers_nominal = water_analyzer_health == 'NOMINAL' and soil_analyzer_health == 'NOMINAL'

            initial_analysis_status = {point_of_interest: 'NOT_ANALYZED' for point_of_interest in self.point_of_interests}
            has_not_analyzed = analysis_status == initial_analysis_status

            if is_passable and is_fully_charged and are_analyzers_nominal and has_not_analyzed:
                start_states.append(start_state)

        # start_states = ['0:0:5:NOMINAL:NOMINAL:NOT_ANALYZED']

        return 1.0 / len(start_states) if state in start_states else 0
