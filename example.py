import random
import time

import mdp_printer
import mdp_solver
from grid_world_mdp import GridWorldMdp
from nonmyopic_traction_loss_mlc import TractionLossMlc
from ssas import Ssas


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

    print("Creating the SSAS...")
    ssas = Ssas(mdp, [traction_loss_mlc])

    current_state = 0
    current_action = None

    while current_action != "STAY":
        print("===================================================================")

        mdp_printer.print_grid_world_domain(grid_world, current_state)

        current_action = solution['policy'][current_state]

        traction_loss_mlc_start_state = random.choice(traction_loss_mlc.start_states())
        print("Traction Loss MLC Start State:", traction_loss_mlc_start_state)

        traction_loss_mlc_state = get_successor_state(traction_loss_mlc_start_state, 'NONE:NONE', traction_loss_mlc)
        print("Traction Loss MLC State:", traction_loss_mlc_state)

        traction_loss_mlc_preference = ssas.recommend(traction_loss_mlc, traction_loss_mlc_state)
        parameters = ssas.resolve([traction_loss_mlc_preference])
        selected_parameter = parameters
        print("Parameter Selection:", selected_parameter)

        while selected_parameter != 'NONE:NONE':
            traction_loss_mlc_state = get_successor_state(traction_loss_mlc_state, selected_parameter, traction_loss_mlc)
            print("Traction Loss MLC State:", traction_loss_mlc_state)

            traction_loss_mlc_preference = ssas.recommend(traction_loss_mlc, traction_loss_mlc_state)
            parameters = ssas.resolve([traction_loss_mlc_preference])
            selected_parameter = parameters

            print("Parameter Selection:", parameters)

        current_state = get_successor_state(current_state, current_action, mdp)

        time.sleep(0.25)


if __name__ == '__main__':
    main()
