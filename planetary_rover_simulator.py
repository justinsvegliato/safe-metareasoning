import logging
import random
import time

import utils
from printers import visualizer
from safety_processes.crevice_safety_process import CreviceSafetyProcess
from safety_processes.dust_storm_safety_process import DustStormSafetyProcess
from selector import Selector
from task_processes.planetary_rover_task_process import (GOAL_STATE, MOVEMENT_ACTION_DETAILS, PlanetaryRoverTaskProcess)

# GRID_WORLD = [
#     ['O', 'W', 'O', 'O'],
#     ['O', 'O', 'O', 'W'],
#     ['O', 'W', 'O', 'W'],
#     ['O', 'W', 'O', 'O']
# ]
# POINTS_OF_INTERESTS = [(3, 3), (0, 3)]
# SHADY_LOCATIONS = [(1, 1), (1, 2)]
# INITIAL_STATE = '1:0:5:NOMINAL:NOMINAL:NOT_ANALYZED:NOT_ANALYZED'

GRID_WORLD = [
    ['O', 'W'],
    ['O', 'O'],
]
POINTS_OF_INTERESTS = [(1, 1)]
SHADY_LOCATIONS = [(1, 0)]
INITIAL_STATE = '0:0:5:NOMINAL:NOMINAL:NOT_ANALYZED'

TASK_PROCESS_SLEEP_DURATION = 0 # 1.0
SAFETY_PROCESS_SLEEP_DURATION = 0 # 0.1
MINIMUM_ACTION_DURATION = 25
MAXIMUM_ACTION_DURATION = 30

VERBOSE = False

EXPERIMENT_BUILDERS = {
    'ACTIVE:ACTIVE': [
        {'constructor': CreviceSafetyProcess, 'arguments': [], 'is_active': True},
        {'constructor': DustStormSafetyProcess, 'arguments': [], 'is_active': True}
    ],
    'ACTIVE:INACTIVE': [
        {'constructor': CreviceSafetyProcess, 'arguments': [], 'is_active': True},
        {'constructor': DustStormSafetyProcess, 'arguments': [], 'is_active': False}
    ],
    'INACTIVE:ACTIVE': [
        {'constructor': CreviceSafetyProcess, 'arguments': [], 'is_active': False},
        {'constructor': DustStormSafetyProcess, 'arguments': [], 'is_active': True}
    ],
    'INACTIVE:INACTIVE': [
        {'constructor': CreviceSafetyProcess, 'arguments': [], 'is_active': False},
        {'constructor': DustStormSafetyProcess, 'arguments': [], 'is_active': False}
    ]
}
EXPERIMENT_SIMULATIONS = 100

logging.basicConfig(format='[%(asctime)s|%(module)-25s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def run_simulation(builders):
    statistics = {
        'cumulative_severity_level_count_1': 0,
        'cumulative_severity_level_count_2': 0,
        'cumulative_severity_level_count_3': 0,
        'cumulative_severity_level_count_4': 0,
        'cumulative_severity_level_count_5': 0,
        'cumulative_interference': 0
    }

    start = time.time()
    task_process = PlanetaryRoverTaskProcess(GRID_WORLD, POINTS_OF_INTERESTS, SHADY_LOCATIONS)
    logging.info("Built the planetary rover task process: [states=%d, actions=%d, time=%f]", len(task_process.states()), len(task_process.actions()), time.time() - start)

    execution_contexts = {}
    for builder in builders:
        start = time.time()
        safety_process = builder['constructor'](*builder['arguments'])
        execution_contexts[safety_process.name] = {'instance': safety_process, 'current_state': None, 'current_rating': None, 'is_active': builder['is_active']}
        logging.info("Built a safety process: [name=%s, time=%f]", safety_process.name, time.time() - start)

    start = time.time()
    selector = Selector([execution_contexts[name]['instance'] for name in execution_contexts])
    logging.info("Built a safety-sensitive autonomous system: [time=%f]", time.time() - start)

    logging.info("Solving the planetary rover task process...")
    start = time.time()
    policy = utils.get_task_process_solution(task_process)['policy']
    logging.info("Solved for the policy of the planetary rover task process: [time=%f]", time.time() - start)

    current_state = INITIAL_STATE
    current_action = policy[current_state]

    logging.info("Activating the simulator...")
    while current_state != GOAL_STATE:
        logging.info("Performing one step of the simulator: [state=%s, action=%s]", current_state, current_action)
        visualizer.print_planetary_rover_information(task_process, current_state, policy, GRID_WORLD)

        action_duration = random.randint(MINIMUM_ACTION_DURATION, MAXIMUM_ACTION_DURATION)

        if current_action in MOVEMENT_ACTION_DETAILS:
            visualizer.print_header("Safety Monitors")

            for name in execution_contexts:
                safety_process = execution_contexts[name]['instance']
                current_safety_process_state = random.choice(safety_process.start_states())
                current_safety_process_rating = selector.recommend(safety_process, current_safety_process_state)
                execution_contexts[name]['current_state'] = current_safety_process_state
                execution_contexts[name]['current_rating'] = current_safety_process_rating

            active_execution_contexts = [name for name in execution_contexts if execution_contexts[name]['is_active']]
            ratings = [execution_contexts[name]['current_rating'] for name in active_execution_contexts]
            parameter = selector.select(ratings) if len(ratings) > 0 else "NONE:NONE"

            for name in execution_contexts:
                safety_process = execution_contexts[name]['instance']
                severity = safety_process.severity_function(execution_contexts[name]['current_state'], parameter)
                statistics[f'cumulative_severity_level_count_{severity}'] += 1
                interference = safety_process.interference_function(execution_contexts[name]['current_state'], parameter)
                statistics[f'cumulative_interference'] += interference

            visualizer.print_safety_process_information(0, execution_contexts, parameter)

            step = 1
            while step <= action_duration or parameter != 'NONE:NONE':
                for name in execution_contexts:
                    safety_process = execution_contexts[name]['instance']
                    current_safety_process_state = utils.get_successor_state(execution_contexts[name]['current_state'], parameter, safety_process)
                    current_safety_process_rating = selector.recommend(safety_process, current_safety_process_state)
                    execution_contexts[name]['current_state'] = current_safety_process_state
                    execution_contexts[name]['current_rating'] = current_safety_process_rating

                active_execution_contexts = [name for name in execution_contexts if execution_contexts[name]['is_active']]
                ratings = [execution_contexts[name]['current_rating'] for name in active_execution_contexts]
                parameter = selector.select(ratings) if len(ratings) > 0 else "NONE:NONE"

                for name in execution_contexts:
                    safety_process = execution_contexts[name]['instance']                
                    severity = safety_process.severity_function(execution_contexts[name]['current_state'], parameter)
                    statistics[f'cumulative_severity_level_count_{severity}'] += 1
                    interference = safety_process.interference_function(execution_contexts[name]['current_state'], parameter)
                    statistics[f'cumulative_interference'] += interference

                visualizer.print_safety_process_information(step, execution_contexts, parameter)

                step += 1
                time.sleep(SAFETY_PROCESS_SLEEP_DURATION)

        current_state = utils.get_successor_state(current_state, current_action, task_process)
        current_action = policy[current_state]

        visualizer.print_separator()
        time.sleep(TASK_PROCESS_SLEEP_DURATION)
    
    return statistics


def main():
    for experiment_builder_key in EXPERIMENT_BUILDERS:
        logging.info("Running the experiment [%s]", experiment_builder_key)

        results = {
            'cumulative_severity_level_count_1': 0,
            'cumulative_severity_level_count_2': 0,
            'cumulative_severity_level_count_3': 0,
            'cumulative_severity_level_count_4': 0,
            'cumulative_severity_level_count_5': 0,
            'cumulative_interference': 0
        }

        for _ in range(EXPERIMENT_SIMULATIONS):
            statistics = run_simulation(EXPERIMENT_BUILDERS[experiment_builder_key])
            for key in results:
                results[key] += statistics[key]
        
        for key in results:
            results[key] /= EXPERIMENT_SIMULATIONS

        visualizer.print_results(results)


if __name__ == '__main__':
    main()
