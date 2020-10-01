import logging
import random
import time

import utils
from mlc.obstacle_mlc import ObstacleMlc
from mlc.overheating_mlc import OverheatingMlc
from mdp.mars_rover_mdp import (GOAL_STATE, MOVEMENT_ACTION_DETAILS, MarsRoverMdp)
from printers import visualizer
from resolver import Resolver
from solvers import mdp_solver

# GRID_WORLD = [
#     ['O', 'W', 'O', 'O'],
#     ['O', 'O', 'O', 'W'],
#     ['O', 'W', 'O', 'W'],
#     ['O', 'W', 'O', 'O']
# ]
# POINTS_OF_INTERESTS = [(3, 3), (0, 3)]
# SHADY_LOCATIONS = [(1, 1), (1, 2)]
# INITIAL_STATE = '1:0:5:NOMINAL:NOMINAL:NOT_ANALYZED:NOT_ANALYZED'

GRID_WORLD = [
    ['O', 'W'],
    ['O', 'O'],
]
POINTS_OF_INTERESTS = [(1, 1)]
SHADY_LOCATIONS = [(1, 0)]
INITIAL_STATE = '0:0:5:NOMINAL:NOMINAL:NOT_ANALYZED'

OLP_SLEEP_DURATION = 1.0
MLC_SLEEP_DURATION = 0.1
MINIMUM_ACTION_DURATION = 25
MAXIMUM_ACTION_DURATION = 30

BUILDERS = [
    {'constructor': ObstacleMlc, 'arguments': []},
    {'constructor': OverheatingMlc, 'arguments': []}
]

logging.basicConfig(format='[%(asctime)s|%(module)-20s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def main():
    start = time.time()
    olp = MarsRoverMdp(GRID_WORLD, POINTS_OF_INTERESTS, SHADY_LOCATIONS)
    logging.info("Built the mars rover OLP: [states=%d, actions=%d, time=%f]", len(olp.states()), len(olp.actions()), time.time() - start)

    execution_contexts = {}
    for builder in BUILDERS:
        start = time.time()
        mlc = builder['constructor'](*builder['arguments'])
        execution_contexts[mlc.name] = {'instance': mlc, 'current_state': None, 'current_preference': None}
        logging.info("Built a meta-level controller: [name=%s, time=%f]", mlc.name, time.time() - start)

    start = time.time()
    mlcs = [execution_contexts[name]['instance'] for name in execution_contexts]
    resolver = Resolver(mlcs)
    logging.info("Built a safety-sensitive autonomous system: [time=%f]", time.time() - start)

    # TODO: Implement file cache logic
    logging.info("Solving the mars rover OLP...")
    start = time.time()
    solution = mdp_solver.solve(olp, 0.99)
    policy = solution['policy']
    logging.info("Solved for the policy of the mars rover OLP: [time=%f]", time.time() - start)

    current_state = INITIAL_STATE
    current_action = policy[current_state]

    logging.info("Activating the simulator...")
    while current_state != GOAL_STATE:
        logging.info("Performing one step of the simulator: [state=%s, action=%s]", current_state, current_action)
        visualizer.print_mars_rover_information(olp, current_state, policy, GRID_WORLD)

        action_duration = random.randint(MINIMUM_ACTION_DURATION, MAXIMUM_ACTION_DURATION)

        if current_action in MOVEMENT_ACTION_DETAILS:
            visualizer.print_header("Safety Monitors")

            for name in execution_contexts:
                mlc = execution_contexts[name]['instance']
                current_mlc_state = random.choice(mlc.start_states())
                current_mlc_preference = resolver.recommend(mlc, current_mlc_state)
                execution_contexts[name]['current_state'] = current_mlc_state
                execution_contexts[name]['current_preference'] = current_mlc_preference

            preferences = [execution_contexts[name]['current_preference'] for name in execution_contexts]
            parameter = resolver.resolve(preferences)

            visualizer.print_mlc_information(0, execution_contexts, parameter)

            step = 1
            while step <= action_duration or parameter != 'NONE:NONE:NONE':
                for name in execution_contexts:
                    mlc = execution_contexts[name]['instance']
                    current_mlc_state = utils.get_successor_state(execution_contexts[name]['current_state'], parameter, mlc)
                    current_mlc_preference = resolver.recommend(mlc, current_mlc_state)
                    execution_contexts[name]['current_state'] = current_mlc_state
                    execution_contexts[name]['current_preference'] = current_mlc_preference

                preferences = [execution_contexts[name]['current_preference'] for name in execution_contexts]
                parameter = resolver.resolve(preferences)

                visualizer.print_mlc_information(step, execution_contexts, parameter)

                step += 1
                time.sleep(MLC_SLEEP_DURATION)

        current_state = utils.get_successor_state(current_state, current_action, olp)
        current_action = policy[current_state]

        visualizer.print_separator()
        time.sleep(OLP_SLEEP_DURATION)


if __name__ == '__main__':
    main()
