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
    # mdp = MarsRoverMdp(grid_world, [(1, 1)], [(1, 0)])

    grid_world = [
        ['O', 'W', 'O'],
        ['O', 'O', 'O'],
        ['O', 'W', 'O']
    ]
    mdp = MarsRoverMdp(grid_world, [(2, 2)], [(1, 1)])

    # grid_world = [
    #     ['O', 'W'],
    #     ['O', 'O']
    # ]
    # mdp = MarsRoverMdp(grid_world, [(1, 1)], [(1, 0)])

    import json
    solutions = mdp_solver.solve(mdp, 0.99)
    print(json.dumps(solutions['policy'], indent=4))

if __name__ == '__main__':
    main()
