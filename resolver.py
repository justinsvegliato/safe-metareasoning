import json
import logging
import os
import random

from solvers import mlc_solver

POLICY_CACHE_DIRECTORY = 'policies'

EPSILON = 0.001
GAMMA = 0.99

logging.basicConfig(format='[%(asctime)s|%(module)-20s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Resolver:
    def __init__(self, meta_level_controllers):
        self.meta_level_controllers = meta_level_controllers

        self.severity_parameter_value_map = {}
        self.interference_parameter_value_map = {}

        for meta_level_controller in self.meta_level_controllers:
            solution = self.get_solution(meta_level_controller)
            self.severity_parameter_value_map[meta_level_controller.name] = solution['severity_parameter_values']
            self.interference_parameter_value_map[meta_level_controller.name] = solution['interference_parameter_values']

    def get_solution(self, meta_level_controller):
        file_path = os.path.join(POLICY_CACHE_DIRECTORY, meta_level_controller.kind + ".json")

        if os.path.exists(file_path):
            logging.info("Loading the policy: [mlc=%s, file=%s]", meta_level_controller.kind, file_path)
            with open(file_path) as file:
                return json.load(file)

        logging.info("Solving the policy: [mlc=%s, file=%s]", meta_level_controller.kind, file_path)
        solution = mlc_solver.solve(meta_level_controller, GAMMA, EPSILON)
        with open(file_path, 'w') as file:
            json.dump(solution, file, indent=4)
            return solution

    def filter(self, parameters, preferences, objective):
        value_matrix = {}

        for parameter in parameters:
            values = [preference[parameter][objective] for preference in preferences]
            descending_values = sorted(values, reverse=True)
            value_matrix[parameter] = descending_values

        for index in range(len(preferences)):
            highest_severity_column = [value_matrix[parameter][index] for parameter in value_matrix]

            minimum_value = min(highest_severity_column)

            new_value_matrix = {}
            for parameter, values in value_matrix.items():
                if values[index] == minimum_value:
                    new_value_matrix[parameter] = values

            value_matrix = new_value_matrix

        return list(value_matrix.keys())

    def resolve(self, preferences):
        parameters = self.meta_level_controllers[0].parameters()
        best_severity_parameters = self.filter(parameters, preferences, 'severity')
        best_severity_interference_parameters = self.filter(best_severity_parameters, preferences, 'interference')
        return random.choice(best_severity_interference_parameters)

    def recommend(self, meta_level_controller, state, is_nonmyopic=True):
        preference = {}

        if is_nonmyopic:
            for parameter in meta_level_controller.parameters():
                preference[parameter] = {
                    'severity': self.severity_parameter_value_map[meta_level_controller.name][state][parameter],
                    'interference': self.interference_parameter_value_map[meta_level_controller.name][state][parameter]
                }
        else:
            for parameter in meta_level_controller.parameters():
                preference[parameter] = {
                    'severity': meta_level_controller.severity_function(state, parameter),
                    'interference': meta_level_controller.interference_function(state, parameter)
                }

        return preference