class Ssas:
    def __init__(self, object_level_process, meta_level_controllers):
        self.object_level_process = object_level_process
        self.meta_level_controllers = meta_level_controllers

    def resolve(self, recommendations):
        lowest_severity_meta_level_actions = []
        lowest_severity = float('inf')

        for meta_level_action in self.meta_level_controllers[0].meta_level_actions():
            worst_case_severity = float('-inf')
            for recommendation in recommendations:
                current_severity = recommendation[meta_level_action][0]
                if current_severity > worst_case_severity:
                    worst_case_severity = current_severity

            if worst_case_severity < lowest_severity:
                lowest_severity = worst_case_severity
                lowest_severity_meta_level_actions = [meta_level_action]
            elif worst_case_severity is lowest_severity:
                lowest_severity_meta_level_actions.append(meta_level_action)

        lowest_interference = float('inf')
        lowest_interference_meta_level_actions = []

        for meta_level_action in lowest_severity_meta_level_actions:
            worst_case_interference = float('-inf')
            for recommendation in recommendations:
                current_interference = recommendation[meta_level_action][1]
                if current_interference > worst_case_interference:
                    worst_case_interference = current_interference

            if worst_case_interference < lowest_interference:
                lowest_interference = worst_case_interference
                lowest_interference_meta_level_actions = [meta_level_action]
            elif worst_case_interference is lowest_interference:
                lowest_interference_meta_level_actions.append(meta_level_action)

        return lowest_interference_meta_level_actions
