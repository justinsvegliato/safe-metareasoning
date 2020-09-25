from printers import mdp_printer
from olp.mars_rover_mdp import MarsRoverMdp
from solvers import mdp_solver


def main():
    # grid_world = [
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    #     ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    # ]
    # grid_world = [
    #     ['O', 'W', 'O'],
    #     ['O', 'O', 'O'],
    #     ['O', 'W', 'O']
    # ]
    grid_world = [
        ['O', 'W'],
        ['O', 'O']
    ]

    mdp = MarsRoverMdp(grid_world, [(1, 1)], [(1, 0)])
    mdp_printer.print_reward_function(mdp)

    # solutions = mdp_solver.solve(mdp, 0.99)

    # import json
    # print(json.dumps(solutions['values'], indent=4))
    # print(json.dumps(solutions['policy'], indent=4))

if __name__ == '__main__':
    main()
