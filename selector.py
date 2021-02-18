import json
import logging
import os

from solvers import safety_process_solver

POLICY_CACHE_DIRECTORY = 'policies'
POLICY_CACHE_EXTENSION = '.json'

EPSILON = 0.001
GAMMA = 0.99
MINIMUM_SEVERITY = 1
MAXIMUM_SEVERITY = 5

logging.basicConfig(format='[%(asctime)s|%(module)-25s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Selector:
    def __init__(self, safety_processes):
        self.safety_processes = safety_processes

        self.severity_parameter_value_map = {}
        self.interference_parameter_value_map = {}

        for safety_process in self.safety_processes:
            solution = self.get_solution(safety_process)
            self.severity_parameter_value_map[safety_process.name] = solution['severity_parameter_values']
            self.interference_parameter_value_map[safety_process.name] = solution['interference_parameter_values']

    def get_solution(self, safety_process):
        file_path = os.path.join(POLICY_CACHE_DIRECTORY, safety_process.kind + POLICY_CACHE_EXTENSION)

        if not os.path.exists(file_path):
            solution = safety_process_solver.solve(safety_process, GAMMA, EPSILON)

            logging.info("Saving the policy: [safety_process=%s, file=%s]", safety_process.kind, file_path)
            with open(file_path, 'w') as file:
                json.dump(solution, file, indent=4)

        logging.info("Loading the policy: [safety_process=%s, file=%s]", safety_process.kind, file_path)
        with open(file_path) as file:
            return json.load(file)

    # TODO: Fix severity being a string instead of an integer
    def filter_by_severity(self, parameters, ratings):
        severity_count_matrix = {}

        for parameter in parameters:
            severity_count_matrix[parameter] = {severity: 0 for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1))}
            for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1)):
                for rating in ratings:
                    severity_count_matrix[parameter][severity] += rating[parameter]['severity'][f'{severity}']

        available_parameters = set(parameters)
        eliminated_parameters = set()
        for severity in reversed(range(MINIMUM_SEVERITY, MAXIMUM_SEVERITY + 1)):
            minimum_severity = min([severity_count_matrix[parameter][severity] for parameter in available_parameters])
            for parameter in available_parameters:
                if severity_count_matrix[parameter][severity] > minimum_severity:
                    eliminated_parameters.add(parameter)

            available_parameters = available_parameters - eliminated_parameters

        return available_parameters

    def filter_by_interference(self, parameters, ratings):
        interference_matrix = {}

        for parameter in parameters:
            values = [rating[parameter]['interference'] for rating in ratings]
            descending_values = sorted(values, reverse=True)
            interference_matrix[parameter] = descending_values

        for index in range(len(ratings)):
            highest_severity_column = [interference_matrix[parameter][index] for parameter in interference_matrix]

            minimum_value = min(highest_severity_column)

            new_value_matrix = {}
            for parameter, values in interference_matrix.items():
                if values[index] == minimum_value:
                    new_value_matrix[parameter] = values

            interference_matrix = new_value_matrix

        return list(interference_matrix.keys())

    # TODO: Avoid relying on a specific safety process
    # TODO: Choose a parameter randomly once the code performs well
    def select(self, ratings):
        parameters = self.safety_processes[0].parameters()
        best_severity_parameters = self.filter_by_severity(parameters, ratings)
        best_severity_interference_parameters = self.filter_by_interference(best_severity_parameters, ratings)
        return best_severity_interference_parameters[0]

    def recommend(self, safety_process, state, is_nonmyopic=True):
        rating = {}

        if is_nonmyopic:
            for parameter in safety_process.parameters():
                rating[parameter] = {
                    'severity': self.severity_parameter_value_map[safety_process.name][state][parameter],
                    'interference': self.interference_parameter_value_map[safety_process.name][state][parameter]
                }
        else:
            for parameter in safety_process.parameters():
                rating[parameter] = {
                    'severity': safety_process.severity_function(state, parameter),
                    'interference': safety_process.interference_function(state, parameter)
                }

        return rating
