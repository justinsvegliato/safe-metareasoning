import random
import time

import numpy as np

import mdp_printer
import mdp_solver
from grid_world_mdp import GridWorldMdp
from obstacle_collision_mlc import ObstacleCollisionMlc
from ssas import Ssas
from traction_loss_mlc import TractionLossMlc


def get_successor_state(current_state, current_action, mdp):
    probability_threshold = random.random()

    total_probability = 0

    for successor_state in mdp.states():
        transition_probability = mdp.transition_function(current_state, current_action, successor_state)

        total_probability += transition_probability

        if total_probability >= probability_threshold:
            return successor_state


def main():
    grid_world = [
        ['O', 'O', 'W', 'W', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'W', 'W', 'O', 'W', 'O', 'W', 'O', 'W', 'O', 'O'],
        ['O', 'O', 'W', 'W', 'O', 'W', 'O', 'O', 'O', 'W', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'W', 'W', 'W', 'W', 'W', 'O', 'O'],
        ['O', 'O', 'W', 'W', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'W', 'W', 'W', 'W', 'W', 'G', 'O']
    ]

    print("Creating and solving the grid world MDP...")
    mdp = GridWorldMdp(grid_world)
    solution = mdp_solver.solve(mdp, 0.99)

    print("Creating the traction loss MLC...")
    traction_loss_mlc = TractionLossMlc()

    print("Creating the obstacle MLC...")
    obstacle_collision_mlc = ObstacleCollisionMlc()

    print("Creating the SSAS...")
    ssas = Ssas(mdp, [traction_loss_mlc, obstacle_collision_mlc])

    current_state = 0
    current_action = None

    while current_action != "STAY":
        print("===================================================================")

        mdp_printer.print_grid_world_domain(grid_world, current_state)

        current_action = solution['policy'][current_state]

        traction_loss_mlc_state = np.random.choice(traction_loss_mlc.meta_level_states(), p=[0.1, 0.2, 0.7])
        obstacle_mlc_state = np.random.choice(obstacle_collision_mlc.meta_level_states(), p=[0.2, 0.8])

        print("Traction Loss MLC State:", traction_loss_mlc_state)
        print("Obstacle Collision MLC State:", obstacle_mlc_state)

        traction_loss_recommendation = ssas.recommend(traction_loss_mlc, traction_loss_mlc_state)
        obstacle_loss_recommendation = ssas.recommend(obstacle_collision_mlc, obstacle_mlc_state)
        meta_level_actions = ssas.resolve([traction_loss_recommendation, obstacle_loss_recommendation])

        print("Hyperparameter Selection:", meta_level_actions)

        current_state = get_successor_state(current_state, current_action, mdp)

        time.sleep(0.25)


if __name__ == '__main__':
    main()
