def print_states(safety_process):
    print("States:")

    for index, state in enumerate(safety_process.states()):
        print(f"  State {index}: {state}")


def print_parameters(safety_process):
    print("Parameters:")

    for index, parameter in enumerate(safety_process.parameters()):
        print(f"  Parameter {index}: {parameter}")


def print_transition_function(safety_process):
    print("Transition Function:")

    is_valid = True

    for state in safety_process.states():
        for parameter in safety_process.parameters():
            print(f"  Transition: ({state}, {parameter})")

            total_probability = 0

            for successor_state in safety_process.states():
                probability = safety_process.transition_function(state, parameter, successor_state)

                total_probability += probability

                if probability > 0:
                    print(f"    Successor State: {successor_state} -> {probability}")

            is_valid = is_valid and 0.99 <= total_probability <= 1.025
            print(f"    Total Probability: {total_probability}")

            if not is_valid:
                return

    print(f"  Is Valid: {is_valid}")


def print_severity_function(safety_process):
    print("Severity Function:")

    for state in safety_process.states():
        print(f"  State: {state}")

        for parameter in safety_process.parameters():
            severity = safety_process.severity_function(state, parameter)
            print(f"    Parameter: {parameter} -> {severity}")


def print_interference_function(safety_process):
    print("Interference Function:")

    for state in safety_process.states():
        print(f"  State: {state}")

        for parameter in safety_process.parameters():
            severity = safety_process.interference_function(state, parameter)
            print(f"    Parameter: {parameter} -> {severity}")


def print_start_states(safety_process):
    print("Start States:")

    for index, state in enumerate(safety_process.start_states()):
        print(f"  Start State {index}: {state}")


def print_safety_process(safety_process):
    print_states(safety_process)
    print_parameters(safety_process)
    print_transition_function(safety_process)
    print_severity_function(safety_process)
    print_interference_function(safety_process)
    print_start_states(safety_process)
