import json

from mlc.overheating_mlc import OverheatingMlc
from solvers import mlc_solver


def main():
    mlc = OverheatingMlc()
    print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))


if __name__ == '__main__':
    main()
