import itertools

STATE_CONNECTOR = ':'

TERRAIN_TYPES = {'W': 'IMPASSABLE', 'O': 'NORMAL'}
WEATHER = ['SUNNY', 'SHADY']

MAXIMUM_BATTERY_LEVEL = 5
BATTERY_LEVELS = range(0, MAXIMUM_BATTERY_LEVEL + 1)

WATER_ANALYZER_HEALTH = ['NOMINAL', 'ERROR']
SOIL_ANALYZER_HEALTH = ['NOMINAL', 'ERROR']
ANALYZER_HEALTH_PROBABILITIES = {
    'NOMINAL': {'NOMINAL': 0.95, 'ERROR': 0.05},
    'ERROR': {'NOMINAL': 0.0, 'ERROR': 1.0},
}
ANALYSIS_CONDITIONS = ['NOT_ANALYZED', 'ANALYZED']

GOAL_STATE = 'SLEEP_MODE'

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
    def __init__(self, grid_world, points_of_interest, shady_locations):
        self.grid_world = grid_world
        self.points_of_interests = points_of_interest

        self.width = len(grid_world[0])
        self.height = len(grid_world)
        self.points_of_interest_size = len(self.points_of_interests)

        rows = range(self.height)
        cols = range(self.width)
        analysis_status = [ANALYSIS_CONDITIONS for _ in points_of_interest]
        state_tuples = itertools.product(rows, cols, BATTERY_LEVELS, WATER_ANALYZER_HEALTH, SOIL_ANALYZER_HEALTH, *analysis_status)

        self.state_registry = {}
        for state_tuple in state_tuples:
            state = STATE_CONNECTOR.join(str(state_factor) for state_factor in state_tuple)
            self.state_registry[state] = {
                'row': state_tuple[0],
                'column': state_tuple[1],
                'terrain_type': TERRAIN_TYPES[grid_world[state_tuple[0]][state_tuple[1]]],
                'weather': 'SHADY' if (state_tuple[0], state_tuple[1]) in shady_locations else 'SUNNY',
                'battery_level': state_tuple[2],
                'water_analyzer_health': state_tuple[3],
                'soil_analyzer_health': state_tuple[4],
                'analysis_status': {self.points_of_interests[i]: state_tuple[5 + i] for i in range(self.points_of_interest_size)},
                'is_point_of_interest': (state_tuple[0], state_tuple[1]) in self.points_of_interests
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

    # TODO: Clean up this transition function
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
        successor_terrain_type = state_successor_record['terrain_type']
        successor_battery_level = state_successor_record['battery_level']
        successor_water_analyzer_health = state_successor_record['water_analyzer_health']
        successor_soil_analyzer_health = state_successor_record['soil_analyzer_health']
        successor_analysis_status = state_successor_record['analysis_status']
        successor_is_point_of_interest = state_successor_record['is_point_of_interest']

        # Loop for every action other than the CHARGE action if the rover ran out of battery
        is_battery_dead = battery_level == 0
        is_same_state = state_record == state_successor_record
        if is_battery_dead and is_same_state:
            return 1

        if successor_state != GOAL_STATE:
            # Ensure that every action other than the CHARGE action decrements the battery level
            is_charging = action == 'CHARGE'
            is_battery_decremented = battery_level == successor_battery_level + 1
            if not is_charging and not is_battery_decremented:
                return 0

            # Ensure that every action other than the ANALYZE action does not alter any analysis status
            is_analyzing = action == 'ANALYZE'
            is_analysis_status_unchanged = analysis_status == successor_analysis_status
            if not is_analyzing and not is_analysis_status_unchanged:
                return 0

        if battery_level > 0:
            if action in MOVEMENT_ACTION_DETAILS:
                is_at_boundary = MOVEMENT_ACTION_DETAILS[action]['is_at_boundary'](row, column, self.grid_world)
                has_not_moved = row == successor_row and column == successor_column
                if is_at_boundary and has_not_moved:
                    return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

                if successor_terrain_type == 'IMPASSABLE':
                    return 0

                is_valid_move = MOVEMENT_ACTION_DETAILS[action]['is_valid_move'](row, successor_row, column, successor_column)
                if is_valid_move:
                    return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

            if action == 'REBOOT':
                has_not_moved = row == successor_row and column == successor_column
                is_nominal = successor_water_analyzer_health == 'NOMINAL' and successor_soil_analyzer_health == 'NOMINAL'
                if has_not_moved and is_nominal:
                    return 1

            if action == 'TRANSMIT':
                if successor_state == GOAL_STATE:
                    return 1

            if action == 'CHARGE':
                has_not_moved = row == successor_row and column == successor_column
                if has_not_moved:
                    has_battery_incremented = battery_level == successor_battery_level - 1
                    is_fully_charged = battery_level == MAXIMUM_BATTERY_LEVEL and successor_battery_level == MAXIMUM_BATTERY_LEVEL
                    is_sunny = weather == 'SUNNY'
                    if is_sunny and (has_battery_incremented or is_fully_charged):
                        return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

                    has_battery_decremented = battery_level == successor_battery_level + 1
                    if not is_sunny and has_battery_decremented:
                        return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

            if action == 'ANALYZE':
                has_not_moved = row == successor_row and column == successor_column
                if has_not_moved:
                    is_nominal = water_analyzer_health == 'NOMINAL' and soil_analyzer_health == 'NOMINAL'
                    if successor_is_point_of_interest and is_nominal:
                        coordinate = (row, column)
                        target_analysis_status = analysis_status.copy()
                        target_analysis_status[coordinate] = 'ANALYZED'

                        is_analysis_status_updated = target_analysis_status == successor_analysis_status
                        if is_analysis_status_updated:
                            return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

                    is_analysis_status_unchanged = analysis_status == successor_analysis_status
                    is_something_broken = water_analyzer_health != 'NOMINAL' or soil_analyzer_health != 'NOMINAL'
                    if is_analysis_status_unchanged and (not successor_is_point_of_interest or is_something_broken):
                        return ANALYZER_HEALTH_PROBABILITIES[water_analyzer_health][successor_water_analyzer_health] * ANALYZER_HEALTH_PROBABILITIES[soil_analyzer_health][successor_soil_analyzer_health]

        return 0

    def reward_function(self, state, action):
        state_record = self.state_registry[state]
        battery_level = state_record['battery_level']
        analysis_status = state_record['analysis_status']

        complete_analysis_status = {point_of_interest: 'ANALYZED' for point_of_interest in self.points_of_interests}

        is_transmitting = action == 'TRANSMIT'
        is_alive = battery_level > 1
        is_analyzed = analysis_status == complete_analysis_status
        if is_transmitting and is_alive and is_analyzed:
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
            is_charged = battery_level == MAXIMUM_BATTERY_LEVEL
            is_nominal = water_analyzer_health == 'NOMINAL' and soil_analyzer_health == 'NOMINAL'

            incomplete_analysis_status = {point_of_interest: 'ANALYZED' for point_of_interest in self.points_of_interests}
            is_analyzed = analysis_status == incomplete_analysis_status

            if is_passable and is_charged and is_nominal and not is_analyzed:
                start_states.append(start_state)

        return 1.0 / len(start_states) if state in start_states else 0

    def get_state_record_from_state(self, state):
        return self.state_registry[state]

    def get_state_from_state_record(self, state_record):
        base_state_factors = [
            str(state_record['row']),
            str(state_record['column']),
            str(state_record['battery_level']),
            state_record['water_analyzer_health'],
            state_record['soil_analyzer_health']
        ]
        analysis_status_state_factors = [state_factor for state_factor in state_record['analysis_status'].values()]
        state_factors = base_state_factors + analysis_status_state_factors
        return STATE_CONNECTOR.join(state_factors)
