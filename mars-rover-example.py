import logging
import time

import utils
from olp.mars_rover_mdp import MarsRoverMdp, GOAL_STATE
from printers import mdp_printer
from solvers import mdp_solver

GRID_WORLD = [
    ['O', 'W', 'O', 'O'],
    ['O', 'O', 'O', 'W'],
    ['O', 'W', 'O', 'W'],
    ['O', 'W', 'O', 'O']
]
POINTS_OF_INTERESTS = [(3, 3), (0, 3)]
SHADY_LOCATIONS = [(1, 1), (1, 2)]
INITIAL_STATE = '1:0:5:NOMINAL:NOMINAL:NOT_ANALYZED:NOT_ANALYZED'

OLP_SLEEP_DURATION = 1.0

logging.basicConfig(format='[%(asctime)s|%(module)-20s|%(funcName)-10s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def main():
    start = time.time()
    mdp = MarsRoverMdp(GRID_WORLD, POINTS_OF_INTERESTS, SHADY_LOCATIONS)
    logging.info("Built the earth observation MDP: [states=%d, actions=%d, time=%f]", len(mdp.states()), len(mdp.actions()), time.time() - start)

    logging.info("Solving the earth observation MDP...")
    start = time.time()
    solutions = mdp_solver.solve(mdp, 0.99)
    logging.info("Solved the earth observation MDP: [time=%f]", time.time() - start)

    policy = solutions['policy']

    current_state = INITIAL_STATE
    current_action = policy[current_state]

    logging.info("Activating the simulator...")
    while current_state != GOAL_STATE:
        logging.info("Executing the simulator: [state=%s, action=%s]", current_state, current_action)

        mdp_printer.print_mars_rover_policy(mdp, current_state, policy, GRID_WORLD)

        current_state = utils.get_successor_state(current_state, current_action, mdp)
        current_action = policy[current_state]

        time.sleep(OLP_SLEEP_DURATION)


if __name__ == '__main__':
    main()
