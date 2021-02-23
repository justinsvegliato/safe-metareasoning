import logging
import random
import time

import small_plotter
import utils
from printers.visualizer import Visualizer
from safety_processes.crevice_safety_process import CreviceSafetyProcess
from safety_processes.dust_storm_safety_process import DustStormSafetyProcess
from safety_processes.rough_terrain_safety_process import RoughTerrainSafetyProcess
from selector import Selector
from task_processes.planetary_rover_task_process import (GOAL_STATE, MOVEMENT_ACTION_DETAILS, PlanetaryRoverTaskProcess)

GRID_WORLD = [
    ['O', 'W', 'O', 'O'],
    ['O', 'O', 'O', 'W'],
    ['O', 'W', 'O', 'W'],
    ['O', 'W', 'O', 'O']
]
POINTS_OF_INTERESTS = [(3, 3), (0, 3)]
SHADY_LOCATIONS = [(1, 1), (1, 2)]
INITIAL_STATE = '1:0:5:NOMINAL:NOMINAL:NOT_ANALYZED:NOT_ANALYZED'

SAFETY_PROCESS_COUNT = 3

TASK_PROCESS_SLEEP_DURATION = 0
SAFETY_PROCESS_SLEEP_DURATION = 0
MINIMUM_ACTION_DURATION = 15
MAXIMUM_ACTION_DURATION = 30

VISUALIZER = Visualizer(is_verbose=False)

EXPERIMENTS = [
    {
        'id': 1,
        'ticks': (r'$[]$', r'$[C]$', r'$[C, D]$', r'$[C, D, R]$'),
        'INACTIVE:INACTIVE:INACTIVE': [
            {'constructor': CreviceSafetyProcess, 'is_active': False},
            {'constructor': DustStormSafetyProcess, 'is_active': False},
            {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
        ],
        'ACTIVE:INACTIVE:INACTIVE': [
            {'constructor': CreviceSafetyProcess, 'is_active': True},
            {'constructor': DustStormSafetyProcess, 'is_active': False},
            {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
        ],
        'INACTIVE:ACTIVE:INACTIVE': [
            {'constructor': CreviceSafetyProcess, 'is_active': True},
            {'constructor': DustStormSafetyProcess, 'is_active': True},
            {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
        ],
        'ACTIVE:ACTIVE:ACTIVE': [
            {'constructor': CreviceSafetyProcess, 'is_active': True},
            {'constructor': DustStormSafetyProcess, 'is_active': True},
            {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
        ]
    },
    # {
    #     'id': 2,
    #     'ticks': (r'$\{ \}$', r'$\{ C \}$', r'$\{ C, R \}$', r'$\{ C, R, D \}$'),
    #     'INACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'ACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'INACTIVE:ACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ],
    #     'ACTIVE:ACTIVE:ACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ]
    # },
    # {
    #     'id': 3,
    #     'ticks': (r'$\{ \}$', r'$\{ D \}$', r'$\{ D, C \}$', r'$\{ D, C, R \}$'),
    #     'INACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'ACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'INACTIVE:ACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'ACTIVE:ACTIVE:ACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ]
    # },
    # {
    #     'id': 4,
    #     'ticks': (r'$\{ \}$', r'$\{ D \}$', r'$\{ D, R \}$', r'$\{ D, R, C \}$'),
    #     'INACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'ACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'INACTIVE:ACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ],
    #     'ACTIVE:ACTIVE:ACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ]
    # },
    # {
    #     'id': 5,
    #     'ticks': (r'$\{ \}$', r'$\{ R \}$', r'$\{ R, C \}$', r'$\{ R, C, D \}$'),
    #     'INACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'ACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ],
    #     'INACTIVE:ACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ],
    #     'ACTIVE:ACTIVE:ACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ]
    # },
    # {
    #     'id': 6,
    #     'ticks': (r'$\{ \}$', r'$\{ R \}$', r'$\{ R, D \}$', r'$\{ R, D, C \}$'),
    #     'INACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': False}
    #     ],
    #     'ACTIVE:INACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': False},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ],
    #     'INACTIVE:ACTIVE:INACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': False},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ],
    #     'ACTIVE:ACTIVE:ACTIVE': [
    #         {'constructor': CreviceSafetyProcess, 'is_active': True},
    #         {'constructor': DustStormSafetyProcess, 'is_active': True},
    #         {'constructor': RoughTerrainSafetyProcess, 'is_active': True}
    #     ]
    # }
]
SIMULATIONS = 25

logging.basicConfig(format='[%(asctime)s|%(module)-25s|%(funcName)-15s|%(levelname)-5s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def run_simulation(builders):
    simulation_results = {
        'severity_level_5': [0] * SAFETY_PROCESS_COUNT,
        'severity_level_4': [0] * SAFETY_PROCESS_COUNT,
        'severity_level_3': [0] * SAFETY_PROCESS_COUNT,
        'severity_level_2': [0] * SAFETY_PROCESS_COUNT,
        'severity_level_1': [0] * SAFETY_PROCESS_COUNT,
        'interference': [0] * SAFETY_PROCESS_COUNT
    }

    task_process = PlanetaryRoverTaskProcess(GRID_WORLD, POINTS_OF_INTERESTS, SHADY_LOCATIONS)
    logging.debug("Built the planetary rover task process: [states=%d, actions=%d]", len(task_process.states()), len(task_process.actions()))

    execution_contexts = {}
    for builder in builders:
        safety_process = builder['constructor']()
        is_active = builder['is_active']
        execution_contexts[safety_process.name] = {'instance': safety_process, 'current_state': None, 'current_rating': None, 'is_active': is_active}
        logging.debug("Built a safety process: [name=%s]", safety_process.name)

    selector = Selector([execution_contexts[name]['instance'] for name in execution_contexts])
    logging.debug("Built a safety-sensitive autonomous system")

    logging.debug("Solving the planetary rover task process...")
    policy = utils.get_task_process_solution(task_process)['policy']
    logging.debug("Solved for the policy of the planetary rover task process")

    current_state = INITIAL_STATE
    current_action = policy[current_state]

    logging.debug("Activating the simulator...")
    while current_state != GOAL_STATE:
        logging.debug("Performing one step of the simulator: [state=%s, action=%s]", current_state, current_action)
        VISUALIZER.print_planetary_rover_information(task_process, current_state, policy, GRID_WORLD)

        action_duration = random.randint(MINIMUM_ACTION_DURATION, MAXIMUM_ACTION_DURATION)

        if current_action in MOVEMENT_ACTION_DETAILS:
            VISUALIZER.print_header("Safety Monitors")

            for name in execution_contexts:
                safety_process = execution_contexts[name]['instance']
                current_safety_process_state = random.choice(safety_process.start_states())
                current_safety_process_rating = selector.recommend(safety_process, current_safety_process_state)
                execution_contexts[name]['current_state'] = current_safety_process_state
                execution_contexts[name]['current_rating'] = current_safety_process_rating

            active_execution_contexts = [name for name in execution_contexts if execution_contexts[name]['is_active']]
            ratings = [execution_contexts[name]['current_rating'] for name in active_execution_contexts]
            parameter = selector.select(ratings) if len(ratings) > 0 else "NONE:NONE"

            for index, name in enumerate(execution_contexts):
                safety_process = execution_contexts[name]['instance']
                severity = safety_process.severity_function(execution_contexts[name]['current_state'], parameter)
                simulation_results[f'severity_level_{severity}'][index] += 1
                interference = safety_process.interference_function(execution_contexts[name]['current_state'], parameter)
                simulation_results[f'interference'][index] += interference

            VISUALIZER.print_safety_process_information(0, execution_contexts, parameter)

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

                for index, name in enumerate(execution_contexts):
                    safety_process = execution_contexts[name]['instance']                
                    severity = safety_process.severity_function(execution_contexts[name]['current_state'], parameter)
                    simulation_results[f'severity_level_{severity}'][index] += 1
                    interference = safety_process.interference_function(execution_contexts[name]['current_state'], parameter)
                    simulation_results[f'interference'][index] += interference

                VISUALIZER.print_safety_process_information(step, execution_contexts, parameter)

                step += 1
                time.sleep(SAFETY_PROCESS_SLEEP_DURATION)

        current_state = utils.get_successor_state(current_state, current_action, task_process)
        current_action = policy[current_state]

        VISUALIZER.print_separator()
        time.sleep(TASK_PROCESS_SLEEP_DURATION)
    
    return simulation_results


def main():
    for experiment in EXPERIMENTS:
        experiment_results_container = []

        for name in experiment:
            if name == 'id' or name == 'ticks':
                continue

            logging.info("Running the experiment [%s]", name)
            
            experiment_results = {
                'severity_level_5': [0] * SAFETY_PROCESS_COUNT,
                'severity_level_4': [0] * SAFETY_PROCESS_COUNT,
                'severity_level_3': [0] * SAFETY_PROCESS_COUNT,
                'severity_level_2': [0] * SAFETY_PROCESS_COUNT,
                'severity_level_1': [0] * SAFETY_PROCESS_COUNT,
                'interference': [0] * SAFETY_PROCESS_COUNT
            }

            for _ in range(SIMULATIONS):
                simulation_results = run_simulation(experiment[name])
                for key in experiment_results:
                    for index in range(SAFETY_PROCESS_COUNT):
                        experiment_results[key][index] += simulation_results[key][index]
            
            for key in experiment_results:
                for index in range(SAFETY_PROCESS_COUNT):
                    experiment_results[key][index] /= SIMULATIONS
            
            experiment_results_container.append(experiment_results)

        plot_specification = utils.get_plot_specification(experiment_results_container, SAFETY_PROCESS_COUNT)
        small_plotter.plot(plot_specification, experiment['ticks'], experiment['id'])


if __name__ == '__main__':
    main()
