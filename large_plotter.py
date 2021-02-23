import matplotlib.pyplot as plt
from matplotlib.patches import Patch

PLOT_DIRECTORY = "plots"

WIDTH = 0.16

PRIMARY_ALPHA = 1.0
SECONDARY_ALPHA = 0.66
TERTIARY_ALPHA = 0.33

SYSTEM_COUNT = 4
SYSTEMS = range(SYSTEM_COUNT)

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(1, SEVERITY_LEVEL_COUNT))

HELPER = {
    4: {'domain': [i - 3 * WIDTH for i in SYSTEMS], 'color': '#ae1c3d'},
    3: {'domain': [i - 2 * WIDTH for i in SYSTEMS], 'color': '#e67b55'},
    2: {'domain': [i - WIDTH for i in SYSTEMS], 'color': '#b8aa95'},
    1: {'domain': [i for i in SYSTEMS], 'color': '#9fd1f1'},
    0: {'domain': [i + WIDTH for i in SYSTEMS], 'color': '#3a82c4'},
    999: {'domain': [i + 2 * WIDTH for i in SYSTEMS], 'color': 'gray'}
}


def plot(plot_specification, ticks, id):
    figure = plt.figure(figsize=(10, 3.5))

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.rcParams["font.size"] = 15

    plt.margins(x=0.01, y=0.05)
    plt.xlabel("Safe Metareasoning System")
    plt.ylabel("Cumulative Severity Level") 
    plt.xticks(SYSTEMS, ticks)

    for severity_level in SEVERITY_LEVELS:
        plt.bar(HELPER[severity_level]['domain'], plot_specification[severity_level][0], width=WIDTH, alpha=PRIMARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

        accumulator = plot_specification[severity_level][0]
        plt.bar(HELPER[severity_level]['domain'], plot_specification[severity_level][1], bottom=accumulator, width=WIDTH, alpha=SECONDARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

        accumulator = [a + b for a, b in zip(accumulator, plot_specification[severity_level][1])]
        plt.bar(HELPER[severity_level]['domain'], plot_specification[severity_level][2], bottom=accumulator, width=WIDTH, alpha=TERTIARY_ALPHA, color=HELPER[severity_level]['color'], align='edge')

    patches = [
        Patch(facecolor=HELPER[4]['color']),
        Patch(facecolor=HELPER[3]['color']),
        Patch(facecolor=HELPER[2]['color']),
        Patch(facecolor=HELPER[1]['color']),
        Patch(facecolor=HELPER[0]['color']),
        Patch(facecolor=HELPER[999]['color']),
    ]
    plt.legend(patches, ['Severity Level 5', 'Severity Level 4', 'Severity Level 3', 'Severity Level 2', 'Severity Level 1', 'Interference'], ncol=2, handletextpad=0.5, labelspacing=0.2, prop={'size': 12})

    plt.tight_layout()

    figure.savefig(f'{PLOT_DIRECTORY}/plot-{id}.pdf', bbox_inches='tight')
