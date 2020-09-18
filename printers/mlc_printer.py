def print_states(mlc):
    print("States:")

    for index, state in enumerate(mlc.states()):
        print(f"  State {index}: {state}")


def print_parameters(mlc):
    print("Parameters:")

    for index, parameter in enumerate(mlc.parameters()):
        print(f"  Parameter {index}: {parameter}")


def print_transition_function(mlc):
    print("Transition Function:")

    is_valid = True

    for state in mlc.states():
        for parameter in mlc.parameters():
            print(f"  Transition: ({state}, {parameter})")

            total_probability = 0

            for successor_state in mlc.states():
                probability = mlc.transition_function(state, parameter, successor_state)

                total_probability += probability

                if probability > 0:
                    print(f"    Successor State: {successor_state} -> {probability}")

            is_valid = is_valid and 0.99 <= total_probability <= 1.01
            print(f"    Total Probability: {total_probability}")

            if not is_valid:
                return

    print(f"  Is Valid: {is_valid}")


def print_severity_function(mlc):
    print("Severity Function:")

    for state in mlc.states():
        print(f"  State: {state}")

        for parameter in mlc.parameters():
            severity = mlc.severity_function(state, parameter)
            print(f"    Parameter: {parameter} -> {severity}")


def print_interference_function(mlc):
    print("Interference Function:")

    for state in mlc.states():
        print(f"  State: {state}")

        for parameter in mlc.parameters():
            severity = mlc.interference_function(state, parameter)
            print(f"    Parameter: {parameter} -> {severity}")


def print_start_states(mlc):
    print("Start States:")

    for index, state in enumerate(mlc.start_states()):
        print(f"  Start State {index}: {state}")


def print_mlc(mlc):
    print_states(mlc)
    print_parameters(mlc)
    print_transition_function(mlc)
    print_severity_function(mlc)
    print_interference_function(mlc)
    print_start_states(mlc)