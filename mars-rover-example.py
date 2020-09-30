import logging
import random
import time

import utils
from mlc.obstacle_mlc import ObstacleMlc
from olp.mars_rover_mdp import (GOAL_STATE, MOVEMENT_ACTION_DETAILS, MarsRoverMdp)
from printers import mdp_printer
from solvers import mdp_solver
from ssas import Ssas

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
MINIMUM_ACTION_DURATION = 1
MAXIMUM_ACTION_DURATION = 10

META_LEVEL_CONTROLLERS = {
    'Obstacle_MLC_1': {'constructor': ObstacleMlc, 'arguments': []},
    'Obstacle_MLC_2': {'constructor': ObstacleMlc, 'arguments': []}
}

logging.basicConfig(format='[%(asctime)s|%(module)-20s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def main():
    start = time.time()
    mdp = MarsRoverMdp(GRID_WORLD, POINTS_OF_INTERESTS, SHADY_LOCATIONS)
    logging.info("Built the mars rover MDP: [states=%d, actions=%d, time=%f]", len(mdp.states()), len(mdp.actions()), time.time() - start)

    mlc_execution_contexts = {}
    for name, details in META_LEVEL_CONTROLLERS.items():
        start = time.time()
        mlc = details['constructor'](*details['arguments'])
        mlc_execution_contexts[mlc.name] = {
            'instance': mlc,
            'current_state': None,
            'current_preference': None
        }
        logging.info("Built a meta-level controller: [name=%s, time=%f]", mlc.name, time.time() - start)

    start = time.time()
    mlc_instances = [mlc_execution_contexts[name]['instance'] for name in mlc_execution_contexts]
    ssas = Ssas(mdp, mlc_instances)
    logging.info("Built a safety-sensitive autonomous system: [time=%f]", time.time() - start)

    # TODO Implement file cache logic
    logging.info("Solving the mars rover MDP...")
    start = time.time()
    solutions = mdp_solver.solve(mdp, 0.99)
    logging.info("Solved the mars rover MDP: [time=%f]", time.time() - start)

    policy = solutions['policy']

    current_state = INITIAL_STATE
    current_action = policy[current_state]

    logging.info("Activating the simulator...")
    while current_state != GOAL_STATE:
        logging.info("Performing one step of the simulator: [state=%s, action=%s]", current_state, current_action)
        mdp_printer.print_mars_rover_policy(mdp, current_state, policy, GRID_WORLD)

        action_duration = random.randint(MINIMUM_ACTION_DURATION, MAXIMUM_ACTION_DURATION)

        if current_action in MOVEMENT_ACTION_DETAILS:
            print("===== Safety Monitors".ljust(150, '='))

            for name in mlc_execution_contexts:
                mlc_instance = mlc_execution_contexts[name]['instance']

                current_mlc_state = random.choice(mlc_instance.start_states())
                current_mlc_preference = ssas.recommend(mlc_instance, current_mlc_state)

                mlc_execution_contexts[name]['current_state'] = current_mlc_state
                mlc_execution_contexts[name]['current_preference'] = current_mlc_preference

            preferences = [mlc_execution_contexts[name]['current_preference'] for name in mlc_execution_contexts]
            parameter = ssas.resolve(preferences)

            mdp_printer.print_mlc_information(0, mlc_execution_contexts, parameter)

            step = 1
            while step <= action_duration or parameter != 'NONE:NONE':
                for name in mlc_execution_contexts:
                    mlc_instance = mlc_execution_contexts[name]['instance']

                    current_mlc_state = utils.get_successor_state(mlc_execution_contexts[name]['current_state'], parameter, mlc_instance)
                    current_mlc_preference = ssas.recommend(mlc_instance, current_mlc_state)

                    mlc_execution_contexts[name]['current_state'] = current_mlc_state
                    mlc_execution_contexts[name]['current_preference'] = current_mlc_preference

                preferences = [mlc_execution_contexts[name]['current_preference'] for name in mlc_execution_contexts]
                parameter = ssas.resolve(preferences)

                mdp_printer.print_mlc_information(step, mlc_execution_contexts, parameter)

                step += 1
                time.sleep(MLC_SLEEP_DURATION)

        print("=" * 150)

        current_state = utils.get_successor_state(current_state, current_action, mdp)
        current_action = policy[current_state]

        time.sleep(OLP_SLEEP_DURATION)


if __name__ == '__main__':
    main()
