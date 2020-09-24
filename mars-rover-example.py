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
    grid_world = [
        ['O', 'W', 'O'],
        ['O', 'O', 'O'],
        ['O', 'W', 'O']
    ]

    mdp = MarsRoverMdp(grid_world, [(2, 2)], [(1, 1)])
    # mdp_printer.print_transition_function(mdp)

    solutions = mdp_solver.solve(mdp, 0.99)

    import json
    print(json.dumps(solutions['policy'], indent=4))

if __name__ == '__main__':
    main()
