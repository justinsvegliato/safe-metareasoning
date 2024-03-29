import utils

EPSILON = 0.001

MINIMUM_SEVERITY = 1    
MAXIMUM_SEVERITY = 5


class Selector:
    def __init__(self, safety_processes):
        self.safety_processes = safety_processes

        self.severity_parameter_value_map = {}
        self.interference_parameter_value_map = {}

        for safety_process in self.safety_processes:
            solution = utils.get_safety_process_solution(safety_process, EPSILON)
            self.severity_parameter_value_map[safety_process.name] = solution['severity_parameter_values']
            self.interference_parameter_value_map[safety_process.name] = solution['interference_parameter_values']

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

    def select(self, ratings, is_baseline):
        if is_baseline:
            return self.baseline_select(ratings)
        
        parameters = self.safety_processes[0].parameters()
        best_severity_parameters = self.filter_by_severity(parameters, ratings)
        best_severity_interference_parameters = self.filter_by_interference(best_severity_parameters, ratings)
        return best_severity_interference_parameters[0]

    def baseline_select(self, ratings): 
        parameters = self.safety_processes[0].parameters()
        
        for rating in ratings:
            independent_ratings = [rating]
            best_severity_parameters = self.filter_by_severity(parameters, independent_ratings)
            best_severity_interference_parameters = self.filter_by_interference(best_severity_parameters, independent_ratings)
            parameter = best_severity_interference_parameters[0]

            if parameter != 'NONE:NONE':
                break

        return parameter

    def independent_select(self, rating):
        parameters = self.safety_processes[0].parameters()

        independent_ratings = [rating]

        best_severity_parameters = self.filter_by_severity(parameters, independent_ratings)
        best_severity_interference_parameters = self.filter_by_interference(best_severity_parameters, independent_ratings)
        return best_severity_interference_parameters[0]

    def recommend(self, safety_process, state):
        rating = {}

        for parameter in safety_process.parameters():
            rating[parameter] = {
                'severity': self.severity_parameter_value_map[safety_process.name][state][parameter],
                'interference': self.interference_parameter_value_map[safety_process.name][state][parameter]
            }

        return rating
