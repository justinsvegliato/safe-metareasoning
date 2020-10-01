import random
import time

import utils
from mlc.traction_loss_mlc import TractionLossMlc
from olp.grid_world_mdp import GridWorldMdp
from printers import olp_printer
from solvers import mdp_solver
from ssas import Resolver

OLP_SLEEP_DURATION = 0.25
MLC_SLEEP_DURATION = 0.1
MINIMUM_ACTION_DURATION = 1
MAXIMUM_ACTION_DURATION = 10

def main():
    grid_world = [
        ['O', 'O', 'W', 'W', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'W', 'W', 'O', 'W', 'O', 'W', 'O', 'W', 'O', 'O'],
        ['O', 'O', 'W', 'W', 'O', 'W', 'O', 'O', 'O', 'W', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'W', 'W', 'W', 'W', 'W', 'O', 'O'],
        ['O', 'O', 'W', 'W', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'W', 'W', 'W', 'W', 'W', 'G', 'O']
    ]

    print("Building and solving the grid world MDP...")
    mdp = GridWorldMdp(grid_world)
    solution = mdp_solver.solve(mdp, 0.99)

    print("Building the traction loss MLC...")
    traction_loss_mlc = TractionLossMlc()

    print("Building the SSAS...")
    ssas = Resolver(mdp, [traction_loss_mlc])

    current_state = 0
    current_action = None

    while current_action != "STAY":
        current_action = solution['policy'][current_state]

        print("========== Object Level Process ========================================")
        olp_printer.print_grid_world_domain(grid_world, current_state)
        print("Action In Progress:", current_action)

        print("========== Traction Loss Meta-Level Controller =========================")
        action_duration = random.randint(MINIMUM_ACTION_DURATION, MAXIMUM_ACTION_DURATION)

        traction_loss_state = random.choice(traction_loss_mlc.start_states())
        traction_loss_preference = ssas.recommend(traction_loss_mlc, traction_loss_state)
        traction_loss_parameter = ssas.resolve([traction_loss_preference])

        state_record = traction_loss_mlc.state_registry[traction_loss_state]
        parameter_record = traction_loss_mlc.parameter_registry[traction_loss_parameter]
        print(f"0 State:     [Road Position: {state_record['road_position']} - Lane Position: {state_record['lane_position']} - Vehicle Speed: {state_record['vehicle_speed']} - Vehicle Offset: {state_record['vehicle_offset']}]")
        print(f"| Parameter: [Speed Parameter: {parameter_record['speed_parameter']} - Location Parameter: {parameter_record['location_parameter']}]")

        step = 1
        while step <= action_duration or traction_loss_parameter != 'NONE:NONE':
            print()

            traction_loss_state = utils.get_successor_state(traction_loss_state, traction_loss_parameter, traction_loss_mlc)
            traction_loss_preference = ssas.recommend(traction_loss_mlc, traction_loss_state)
            traction_loss_parameter = ssas.resolve([traction_loss_preference])

            state_record = traction_loss_mlc.state_registry[traction_loss_state]
            parameter_record = traction_loss_mlc.parameter_registry[traction_loss_parameter]
            print(f"{step} State:     [Road Position: {state_record['road_position']} - Lane Position: {state_record['lane_position']} - Vehicle Speed: {state_record['vehicle_speed']} - Vehicle Offset: {state_record['vehicle_offset']}]")
            print(f"| Parameter: [Speed Parameter: {parameter_record['speed_parameter']} - Location Parameter: {parameter_record['location_parameter']}]")

            step += 1
            time.sleep(MLC_SLEEP_DURATION)

        current_state = utils.get_successor_state(current_state, current_action, mdp)
        time.sleep(OLP_SLEEP_DURATION)


if __name__ == '__main__':
    main()
