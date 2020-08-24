class Ssas:
    def __init__(self, object_level_process, meta_level_controllers):
        self.object_level_process = object_level_process
        self.meta_level_controllers = meta_level_controllers

    def filter(self, meta_level_actions, recommendations, key):
        lowest_meta_level_actions = []
        lowest_value = float('inf')

        for meta_level_action in meta_level_actions:
            worst_case_value = float('-inf')
            for recommendation in recommendations:
                current_value = recommendation[meta_level_action][key]
                if current_value > worst_case_value:
                    worst_case_value = current_value

            if worst_case_value < lowest_value:
                lowest_value = worst_case_value
                lowest_meta_level_actions = [meta_level_action]
            elif worst_case_value is lowest_value:
                lowest_meta_level_actions.append(meta_level_action)

        return lowest_meta_level_actions

    def resolve(self, recommendations):
        lowest_severity_meta_level_actions = self.filter(self.meta_level_controllers[0].meta_level_actions(), recommendations, 'severity')
        return self.filter(lowest_severity_meta_level_actions, recommendations, 'interference')

    def recommend(self, mlc, state):
        return {action: {'severity': mlc.severity_function(state, action), 'interference': mlc.interference_function(state, action)} for action in mlc.meta_level_actions()}
