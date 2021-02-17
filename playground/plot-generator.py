import random

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

FILENAME = 'anticipated-experimental-results.pdf'

WIDTH = 0.16

PRIMARY_ALPHA = 1.0
SECONDARY_ALPHA = 0.85
TERTIARY_ALPHA = 0.70
QUADRARY_ALPHA = 0.55

SYSTEM_COUNT = 4
SYSTEMS = range(SYSTEM_COUNT)

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(SEVERITY_LEVEL_COUNT)) + [999]

FUDGE_MINIMUM = 10
FUDGE_MAXIMUM = 30

CUMULATIVE_INTERFERENCE_MINIMUM = 0
CUMULATIVE_INTERFERENCE_MAXIMUM = 300
CUMULATIVE_INTERFERENCE_INCREMENT = 50

CUMULATIVE_SEVERITY_LEVEL_MINIMUM = 0
CUMULATIVE_SEVERITY_LEVEL_MAXIMUM = 2500

# # PROBLEM_SPECIFICATION = {
#     4: [
#         [200, 5, 5, 5, 5],
#         [200, 200, 5, 5, 5],
#         [200, 200, 200, 5, 5],
#         [200, 200, 200, 200, 5],
#     ],
#     3: [
#         [150, 10, 10, 10, 10],
#         [150, 150, 10, 10, 10],
#         [150, 150, 150, 10, 10],
#         [150, 150, 150, 150, 10],
#     ],
#     2: [
#         [100, 100, 100, 100, 100],
#         [100, 100, 100, 100, 100],
#         [100, 100, 100, 100, 100],
#         [100, 100, 100, 100, 100],
#     ],
#     1: [
#         [50, 200, 200, 200, 200],
#         [50, 50, 200, 200, 200],
#         [50, 50, 50, 200, 200],
#         [50, 50, 50, 50, 200],
#     ],
#     0: [
#         [300, 500, 500, 500, 500],
#         [300, 300, 500, 500, 500],
#         [300, 300, 300, 500, 500],
#         [300, 300, 300, 300, 500],
#     ],
#     999: [
#         [10, 212, 243, 217, 222],
#         [10, 0, 241, 220, 219],
#         [10, 0, 0, 223, 235],
#         [10, 0, 0, 0, 223],
#     ]
# }

PROBLEM_SPECIFICATION = {
    4: [
        [200, 5, 5, 5],
        [200, 200, 5, 5],
        [200, 200, 200, 5],
        [200, 200, 200, 200],
    ],
    3: [
        [150, 10, 10, 10],
        [150, 150, 10, 10],
        [150, 150, 150, 10],
        [150, 150, 150, 150],
    ],
    2: [
        [100, 100, 100, 100],
        [100, 100, 100, 100],
        [100, 100, 100, 100],
        [100, 100, 100, 100],
    ],
    1: [
        [50, 200, 200, 200],
        [50, 50, 200, 200],
        [50, 50, 50, 200],
        [50, 50, 50, 50],
    ],
    0: [
        [300, 500, 500, 500],
        [300, 300, 500, 500],
        [300, 300, 300, 500],
        [300, 300, 300, 300],
    ],
    999: [
        [10, 212, 243, 217],
        [10, 0, 241, 220],
        [10, 0, 0, 223],
        [10, 0, 0, 0],
    ]
}

HELPER = {
    4: {'domain': [i - 3 * WIDTH for i in SYSTEMS], 'color': '#ae1c3d'},
    3: {'domain': [i - 2 * WIDTH for i in SYSTEMS], 'color': '#e67b55'},
    2: {'domain': [i - WIDTH for i in SYSTEMS], 'color': '#b8aa95'},
    1: {'domain': [i for i in SYSTEMS], 'color': '#9fd1f1'},
    0: {'domain': [i + WIDTH for i in SYSTEMS], 'color': '#3a82c4'},
    999: {'domain': [i + 2 * WIDTH for i in SYSTEMS], 'color': 'gray'},
}


def main():
    figure = plt.figure(figsize=(7, 3.5))
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.rcParams["font.size"] = 15
    plt.xlabel("Safe Metareasoning System")
    plt.ylabel("Cumulative Severity Level")
    plt.margins(x=0.01, y=0.05)

    # plt.xticks(range(5), (r'$r_0$', r'$r_1$', r'$r_2$', r'$r_3$', r'$r_4$',))
    plt.xticks(range(5), (r'$r_0$', r'$r_1$', r'$r_2$', r'$r_3$'))

    axis = plt.gca()
    axis.set_ylim(CUMULATIVE_SEVERITY_LEVEL_MINIMUM, CUMULATIVE_SEVERITY_LEVEL_MAXIMUM)

    for key in PROBLEM_SPECIFICATION:
        if key == 999:
            continue

        for i in range(len(PROBLEM_SPECIFICATION[key])):
            PROBLEM_SPECIFICATION[key][i] = [random.randint(FUDGE_MINIMUM, FUDGE_MAXIMUM) + value for value in PROBLEM_SPECIFICATION[key][i]]

    for key in SEVERITY_LEVELS:
        plt.bar(HELPER[key]['domain'], PROBLEM_SPECIFICATION[key][0], width=WIDTH, alpha=PRIMARY_ALPHA, color=HELPER[key]['color'], align='edge')

        accumulator = PROBLEM_SPECIFICATION[key][0]
        plt.bar(HELPER[key]['domain'], PROBLEM_SPECIFICATION[key][1], bottom=accumulator, width=WIDTH, alpha=SECONDARY_ALPHA, color=HELPER[key]['color'], align='edge')

        accumulator = [a + b for a, b in zip(accumulator, PROBLEM_SPECIFICATION[key][1])]
        plt.bar(HELPER[key]['domain'], PROBLEM_SPECIFICATION[key][2], bottom=accumulator, width=WIDTH, alpha=TERTIARY_ALPHA, color=HELPER[key]['color'], align='edge')

        # accumulator = [a + b for a, b in zip(accumulator, PROBLEM_SPECIFICATION[key][2])]
        # plt.bar(HELPER[key]['domain'], PROBLEM_SPECIFICATION[key][3], bottom=accumulator, width=WIDTH, alpha=QUADRARY_ALPHA, color=HELPER[key]['color'], align='edge')

    elements = [
        Patch(facecolor=HELPER[4]['color'], edgecolor=HELPER[4]['color']),
        Patch(facecolor=HELPER[3]['color'], edgecolor=HELPER[3]['color']),
        Patch(facecolor=HELPER[2]['color'], edgecolor=HELPER[2]['color']),
        Patch(facecolor=HELPER[1]['color'], edgecolor=HELPER[1]['color']),
        Patch(facecolor=HELPER[0]['color'], edgecolor=HELPER[0]['color']),
        Patch(facecolor=HELPER[999]['color'], edgecolor=HELPER[999]['color'])
    ]
    plt.legend(elements, ['Severity Level 5', 'Severity Level 4', 'Severity Level 3', 'Severity Level 2', 'Severity Level 1', 'Interference'], ncol=2, handletextpad=0.5, labelspacing=0.2, prop={'size': 12})

    axis2 = axis.twinx()
    axis2.set_ylabel('Cumulative Interference')
    axis2.set_yticks(range(CUMULATIVE_INTERFERENCE_MINIMUM, CUMULATIVE_INTERFERENCE_MAXIMUM, CUMULATIVE_INTERFERENCE_INCREMENT), minor=False)

    plt.tight_layout()

    figure.savefig(FILENAME, bbox_inches="tight")


if __name__ == "__main__":
    main()