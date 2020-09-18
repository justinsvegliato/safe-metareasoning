from solvers import mlc_solver
import random

EPSILON = 0.001
GAMMA = 0.99


class Ssas:
    def __init__(self, object_level_process, meta_level_controllers):
        self.object_level_process = object_level_process
        self.meta_level_controllers = meta_level_controllers

        self.severity_parameter_value_map = {}
        self.interference_parameter_value_map = {}

        for meta_level_controller in self.meta_level_controllers:
            in_severity_parameter_value_map = meta_level_controller.name in self.severity_parameter_value_map
            in_interference_parameter_value_map = meta_level_controller.name in self.interference_parameter_value_map
            is_ready = in_severity_parameter_value_map and in_interference_parameter_value_map

            if not is_ready:
                solution = mlc_solver.solve(meta_level_controller, GAMMA, EPSILON)
                self.severity_parameter_value_map[meta_level_controller.name] = solution['severity_parameter_values']
                self.interference_parameter_value_map[meta_level_controller.name] = solution['interference_parameter_values']

    def filter(self, parameters, preferences, objective):
        best_parameters = []
        best_parameter_value = float('inf')

        for parameter in parameters:
            minimum_parameter_value = float('-inf')
            for preference in preferences:
                current_parameter_value = preference[parameter][objective]
                if current_parameter_value > minimum_parameter_value:
                    minimum_parameter_value = current_parameter_value

            if minimum_parameter_value < best_parameter_value:
                best_parameter_value = minimum_parameter_value
                best_parameters = [parameter]
            elif minimum_parameter_value is best_parameter_value:
                best_parameters.append(parameter)

        return best_parameters

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
