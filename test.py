import json

from mlc.obstacle_mlc import ObstacleMlc
from mlc.overheating_mlc import OverheatingMlc
from printers import mlc_printer
from solvers import mdp_container, mdp_solver, mlc_solver


def resolve(parameters, preferences):
    severity_matrix = {}

    for parameter in parameters:
        severities = [preference[parameter]['severity'] for preference in preferences]
        sorted_severities = sorted(severities, reverse=True)
        severity_matrix[parameter] = sorted_severities

    for mlc_index in range(len(preferences)):
        highest_severity_column = [severity_matrix[parameter][mlc_index] for parameter in severity_matrix]
        minimum_severity = min(highest_severity_column)

        new_severity_matrix = {}
        for parameter, severities in severity_matrix.items():
            if severities[mlc_index] <= minimum_severity:
                new_severity_matrix[parameter] = severities

        severity_matrix = new_severity_matrix

    return severity_matrix


# def main():
    # parameters = ['SAMER', 'JUSTIN', 'SULIN', 'YUME', 'CONNOR']
    # preferences = [
    #     {
    #         'SAMER': {'severity': 12},
    #         'JUSTIN': {'severity': 1},
    #         'SULIN': {'severity': 2},
    #         'YUME': {'severity': 11},
    #         'CONNOR': {'severity': 19}
    #     },
    #     {
    #         'SAMER': {'severity': 10},
    #         'JUSTIN': {'severity': 12},
    #         'SULIN': {'severity': 1},
    #         'YUME': {'severity': 11},
    #         'CONNOR': {'severity': 1}
    #     },
    #     {
    #         'SAMER': {'severity': 1},
    #         'JUSTIN': {'severity': 4},
    #         'SULIN': {'severity': 12},
    #         'YUME': {'severity': 11},
    #         'CONNOR': {'severity': 1}
    #     },
    #     {
    #         'SAMER': {'severity': 10},
    #         'JUSTIN': {'severity': 8},
    #         'SULIN': {'severity': 8},
    #         'YUME': {'severity': 12},
    #         'CONNOR': {'severity': 1}
    #     }
    # ]
    # severity_matrix = resolve(parameters, preferences)
    # print('Answer:', severity_matrix)


def main():
    mlc = OverheatingMlc()
    print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    # mlc = ObstacleMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))


if __name__ == '__main__':
    main()
