import random

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

FILENAME = 'anticipated-experimental-results.pdf'

WIDTH = 0.15
PRIMARY_ALPHA = 1.0
SECONDARY_ALPHA = 0.85
TERTIARY_ALPHA = 0.70
QUADRARY_ALPHA = 0.55

SYSTEM_COUNT = 5
SYSTEMS = range(SYSTEM_COUNT)

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(SEVERITY_LEVEL_COUNT)) + [999]

TOTAL_SEVERITY_LEVEL_COUNT = 1000
SEVERITY_LEVEL_1_OFFSET = 0.4

PROBLEM_SPECIFICATION = {
    0: {
        False: {4: 0, 3: 0, 2: 0, 1: 0, 0: 0},
        True: {4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    },
    1: {
        False: {4: 200, 3: 150, 2: 100, 1: 50, 0: 300},
        True: {4: 5, 3: 10, 2: 100, 1: 200, 0: 500}
    },
    2: {
        False: {4: 200, 3: 150, 2: 100, 1: 50, 0: 300},
        True: {4: 5, 3: 10, 2: 100, 1: 200, 0: 500}
    },
    3: {
        False: {4: 200, 3: 150, 2: 100, 1: 50, 0: 300},
        True: {4: 5, 3: 10, 2: 100, 1: 200, 0: 500}
    },
    4: {
        False: {4: 200, 3: 150, 2: 100, 1: 50, 0: 300},
        True: {4: 5, 3: 10, 2: 100, 1: 200, 0: 500}
    }
}

ALTERNATE_PROBLEM_SPECIFICATION = {
    4: [
        [200, 5, 5, 5, 5],
        [200, 200, 5, 5, 5],
        [200, 200, 200, 5, 5],
        [200, 200, 200, 200, 5],
    ],
    3: [
        [150, 10, 10, 10, 10],
        [150, 150, 10, 10, 10],
        [150, 150, 150, 10, 10],
        [150, 150, 150, 150, 10],
    ],
    2: [
        [100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100],
    ],
    1: [
        [50, 200, 200, 200, 200],
        [50, 50, 200, 200, 200],
        [50, 50, 50, 200, 200],
        [50, 50, 50, 50, 200],
    ],
    0: [
        [300, 500, 500, 500, 500],
        [300, 300, 500, 500, 500],
        [300, 300, 300, 500, 500],
        [300, 300, 300, 300, 500],
    ],
    999: [
        [10, 212, 243, 217, 222],
        [10, 0, 241, 220, 219],
        [10, 0, 0, 223, 235],
        [10, 0, 0, 0, 223],
    ]
}

HELPER = {
    4: {
        'domain': [i - 3 * WIDTH for i in SYSTEMS],
        'color': '#ae1c3d'
    },
    3: {
        'domain': [i - 2 * WIDTH for i in SYSTEMS],
        'color': '#e67b55'
    },
    2: {
        'domain': [i - WIDTH for i in SYSTEMS],
        'color': '#b8aa95'
    },
    1: {
        'domain': [i for i in SYSTEMS],
        'color': '#9fd1f1'
    },
    0: {
        'domain': [i + WIDTH for i in SYSTEMS],
        'color': '#3a82c4'
    },
    999: {
        'domain': [i + 2 * WIDTH for i in SYSTEMS],
        'color': 'gray'
    },
}

def main():
    figure = plt.figure(figsize=(7, 3.5))
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.rcParams["font.size"] = 12
    plt.xlabel("Safe Metareasoning System")
    plt.ylabel("Cumulative Severity Level")

    plt.xticks(range(5), (r'$r_0$', r'$r_1$', r'$r_2$', r'$r_3$', r'$r_4$',))

    axis = plt.gca()
    axis.set_ylim(0, 2500)

    # severity_level_counts = {}
    # for severity_level in reversed(SEVERITY_LEVELS):
    #     severity_level_counts[severity_level] = [0 for _ in SYSTEMS]

    #     for system in SYSTEMS:
    #         for i in range(0, system + 1):
    #             severity_level_counts[severity_level][system] += random.randint(0, 10) + PROBLEM_SPECIFICATION[i][True][severity_level]
    #         for j in range(system + 1, len(SYSTEMS)):
    #             severity_level_counts[severity_level][system] += random.randint(0, 10) + PROBLEM_SPECIFICATION[j][False][severity_level]

    # plt.bar([i - 2 * WIDTH for i in SYSTEMS], severity_level_counts[4], width=WIDTH, alpha=PRIMARY_ALPHA, color='#ae1c3d', align='center')
    # plt.bar([i - WIDTH for i in SYSTEMS], severity_level_counts[3], width=WIDTH, alpha=PRIMARY_ALPHA, color='#e67b55', align='center')
    # plt.bar([i for i in SYSTEMS], severity_level_counts[2], width=WIDTH, alpha=PRIMARY_ALPHA, color='#eeddc5', align='center')
    # plt.bar([i + WIDTH for i in SYSTEMS], severity_level_counts[1], width=WIDTH, alpha=PRIMARY_ALPHA, color='#9fd1f1', align='center')
    # plt.bar([i + 2 * WIDTH for i in SYSTEMS], severity_level_counts[0], width=WIDTH, alpha=PRIMARY_ALPHA, color='#3a82c4', align='center')

    # severity_level_counts = {}
    # for system in SYSTEMS:
    #     severity_level_counts[system] = {}
    #     for severity_level in reversed(SEVERITY_LEVELS):
    #         severity_level_counts[system][severity_level] = []
    #         for i in range(0, system + 1):
    #             severity_level_counts[system][severity_level].append(PROBLEM_SPECIFICATION[i][True][severity_level])
    #         for j in range(system + 1, len(SYSTEMS)):
    #             severity_level_counts[system][severity_level].append(PROBLEM_SPECIFICATION[j][False][severity_level])

    # print(severity_level_counts)

    for severity_level in ALTERNATE_PROBLEM_SPECIFICATION:
        if severity_level == 999:
            continue

        for i in range(len(ALTERNATE_PROBLEM_SPECIFICATION[severity_level])):
            ALTERNATE_PROBLEM_SPECIFICATION[severity_level][i] = [random.randint(10, 30) + value for value in ALTERNATE_PROBLEM_SPECIFICATION[severity_level][i]]

    for severity_level in SEVERITY_LEVELS:
        plt.bar(HELPER[severity_level]['domain'], ALTERNATE_PROBLEM_SPECIFICATION[severity_level][0], width=WIDTH, alpha=PRIMARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

        cumulative_bottom = ALTERNATE_PROBLEM_SPECIFICATION[severity_level][0]
        plt.bar(HELPER[severity_level]['domain'], ALTERNATE_PROBLEM_SPECIFICATION[severity_level][1], bottom=cumulative_bottom, width=WIDTH, alpha=SECONDARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

        cumulative_bottom = [a + b for a, b in zip(cumulative_bottom, ALTERNATE_PROBLEM_SPECIFICATION[severity_level][1])]
        plt.bar(HELPER[severity_level]['domain'], ALTERNATE_PROBLEM_SPECIFICATION[severity_level][2], bottom=cumulative_bottom, width=WIDTH, alpha=TERTIARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

        cumulative_bottom = [a + b for a, b in zip(cumulative_bottom, ALTERNATE_PROBLEM_SPECIFICATION[severity_level][2])]
        plt.bar(HELPER[severity_level]['domain'], ALTERNATE_PROBLEM_SPECIFICATION[severity_level][3], bottom=cumulative_bottom, width=WIDTH, alpha=QUADRARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

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
    axis2.set_yticks(range(0, 300, 50), minor=True)

    plt.tight_layout()

    figure.savefig(FILENAME, bbox_inches="tight")


if __name__ == "__main__":
    main()
