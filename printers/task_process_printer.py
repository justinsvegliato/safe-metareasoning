def print_states(task_process):
    print("States:")

    for index, state in enumerate(task_process.states()):
        print(f"  State {index}: {state}")


def print_actions(task_process):
    print("Actions:")

    for index, action in enumerate(task_process.actions()):
        print(f"  Action {index}: {action}")


def print_transition_function(task_process):
    print("Transition Function:")

    is_valid = True

    for state in task_process.states():
        for action in task_process.actions():
            print(f"  Transition: ({state}, {action})")

            total_probability = 0

            for successor_state in task_process.states():
                probability = task_process.transition_function(state, action, successor_state)

                total_probability += probability

                if probability > 0:
                    print(f"    Successor State: {successor_state} -> {probability}")

            is_valid = is_valid and 0.99 <= total_probability <= 1.01
            print(f"    Total Probability: {total_probability}")

            if not is_valid:
                return

    print(f"  Is Valid: {is_valid}")


def print_reward_function(task_process):
    print("Reward Function:")

    for state in task_process.states():
        print(f"  State: {state}")

        for action in task_process.actions():
            reward = task_process.reward_function(state, action)
            print(f"    Action: {action} -> {reward}")


def print_start_state_function(task_process):
    print("Start State Function:")

    total_probability = 0

    for state in task_process.states():
        probability = task_process.start_state_function(state)

        if probability > 0:
            print(f"  State {state}: {probability}")
        
        total_probability += probability

    print(f"  Total Probability: {total_probability}")

    is_valid = 0.99 <= total_probability <= 1.01
    print(f"  Is Valid: {is_valid}")


def print_task_process(task_process):
    print_states(task_process)
    print_actions(task_process)
    print_transition_function(task_process)
    print_reward_function(task_process)
    print_start_state_function(task_process)
