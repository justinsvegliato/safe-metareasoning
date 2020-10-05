import json

from mlc.overheating_mlc import OverheatingMlc
from mlc.obstacle_mlc import ObstacleMlc
from solvers import mlc_solver
from printers import mlc_printer

def main():
    mlc = OverheatingMlc()
    print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    # mlc = ObstacleMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))


if __name__ == '__main__':
    main()
