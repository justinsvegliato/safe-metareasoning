def print_states(olp):
    print("States:")

    for index, state in enumerate(olp.states()):
        print(f"  State {index}: {state}")


def print_actions(olp):
    print("Actions:")

    for index, action in enumerate(olp.actions()):
        print(f"  Action {index}: {action}")


def print_transition_function(olp):
    print("Transition Function:")

    is_valid = True

    for state in olp.states():
        for action in olp.actions():
            print(f"  Transition: ({state}, {action})")

            total_probability = 0

            for successor_state in olp.states():
                probability = olp.transition_function(state, action, successor_state)

                total_probability += probability

                if probability > 0:
                    print(f"    Successor State: {successor_state} -> {probability}")

            is_valid = is_valid and 0.99 <= total_probability <= 1.01
            print(f"    Total Probability: {total_probability}")

            if not is_valid:
                return

    print(f"  Is Valid: {is_valid}")


def print_reward_function(olp):
    print("Reward Function:")

    for state in olp.states():
        print(f"  State: {state}")

        for action in olp.actions():
            reward = olp.reward_function(state, action)
            print(f"    Action: {action} -> {reward}")


def print_start_state_function(olp):
    print("Start State Function:")

    total_probability = 0

    for state in olp.states():
        probability = olp.start_state_function(state)

        if probability > 0:
            print(f"  State {state}: {probability}")
        
        total_probability += probability

    print(f"  Total Probability: {total_probability}")

    is_valid = 0.99 <= total_probability <= 1.01
    print(f"  Is Valid: {is_valid}")


def print_olp(olp):
    print_states(olp)
    print_actions(olp)
    print_transition_function(olp)
    print_reward_function(olp)
    print_start_state_function(olp)
