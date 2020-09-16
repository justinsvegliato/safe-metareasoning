import mlc_solver

EPSILON = 0.01
GAMMA = 0.99


class Ssas:
    def __init__(self, object_level_process, meta_level_controllers):
        self.object_level_process = object_level_process
        self.meta_level_controllers = meta_level_controllers

        self.severity_parameter_value_map = {}
        self.interference_parameter_value_map = {}

        for meta_level_controller in self.meta_level_controllers:
            if meta_level_controller.name not in self.severity_parameter_value_map or meta_level_controller.name not in self.interference_parameter_value_map:
                solution = mlc_solver.solve(meta_level_controller, GAMMA, EPSILON)
                self.severity_parameter_value_map[meta_level_controller.name] = solution['severity_parameter_values']
                self.interference_parameter_value_map[meta_level_controller.name] = solution['interference_parameter_values']

    def filter(self, parameters, preferences, key):
        lowest_parameters = []
        lowest_value = float('inf')

        for parameter in parameters:
            worst_case_value = float('-inf')
            for preference in preferences:
                current_value = preference[parameter][key]
                if current_value > worst_case_value:
                    worst_case_value = current_value

            if worst_case_value < lowest_value:
                lowest_value = worst_case_value
                lowest_parameters = [parameter]
            elif worst_case_value is lowest_value:
                lowest_parameters.append(parameter)

        return lowest_parameters

    def resolve(self, preferences):
        parameters = self.meta_level_controllers[0].parameters()
        filtered_severity_parameters = self.filter(parameters, preferences, 'severity')
        filtered_interference_parameters = self.filter(filtered_severity_parameters, preferences, 'interference')
        return filtered_interference_parameters

    def recommend(self, meta_level_controller, state, is_nonmyopic=True):
        preference = {}

        for parameter in meta_level_controller.parameters():
            if is_nonmyopic:
                preference[parameter] = {
                    'severity': self.severity_parameter_value_map[meta_level_controller.name][state][parameter],
                    'interference': self.interference_parameter_value_map[meta_level_controller.name][state][parameter]
                }
            else:
                preference[parameter] = {
                    'severity': meta_level_controller.severity_function(state, parameter),
                    'interference': meta_level_controller.interference_function(state, parameter)
                }

        return preference
