import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Patch
import numpy as np

PLOT_DIRECTORY = "plots"

WIDTH = 1.0

PRIMARY_ALPHA = 1.0
SECONDARY_ALPHA = 0.66
TERTIARY_ALPHA = 0.33

SYSTEM_COUNT = 4
SYSTEMS = range(SYSTEM_COUNT)

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(SEVERITY_LEVEL_COUNT)) + [999]

HELPER = {
    4: {'maximum': 100, 'ylabel': 'Severity Level $\ell = 5$ Frequency', 'file_key': '5', 'labelpad': -20},
    3: {'maximum': 100, 'ylabel': 'Severity Level $\ell = 4$ Frequency', 'file_key': '4', 'labelpad': -20},
    2: {'maximum': 100, 'ylabel': 'Severity Level $\ell = 3$ Frequency', 'file_key': '3', 'labelpad': -20},
    1: {'maximum': 100, 'ylabel': 'Severity Level $\ell = 2$ Frequency', 'file_key': '2', 'labelpad': -20},
    0: {'maximum': 6000, 'ylabel': 'Severity Level $\ell = 1$ Frequency', 'file_key': '1', 'labelpad': -17},
    999: {'maximum': 2000, 'ylabel': 'Cumulative Interference [sec]', 'file_key': 'interference', 'labelpad': -17}
}


def y_fmt(y, pos):
    decades = [1e9, 1e6, 1e3, 1e0, 1e-3, 1e-6, 1e-9 ]
    suffix  = ["G", "M", "K", "" , "m" , "u", "n"  ]
    if y == 0:
        return str(0)
    for i, d in enumerate(decades):
        if np.abs(y) >=d:
            val = y/float(d)
            signf = len(str(val).split(".")[1])
            if signf == 0:
                return '{val:d} {suffix}'.format(val=int(val), suffix=suffix[i])
            else:
                if signf == 1:
                    if str(val).split(".")[1] == "0":
                       return '{val:d}{suffix}'.format(val=int(round(val)), suffix=suffix[i]) 
                tx = "{"+"val:.{signf}f".format(signf = signf) +"}{suffix}"
                return tx.format(val=val, suffix=suffix[i])

    return y


def plot(plot_specification, ticks, id):
    for severity_level in SEVERITY_LEVELS:
        figure = plt.figure(figsize=(4, 4))

        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = "Times"
        plt.rcParams["font.size"] = 15
        plt.rcParams["text.usetex"] = True

        plt.margins(x=0.01, y=0.01)
        plt.ylabel(HELPER[severity_level]['ylabel'], labelpad=HELPER[severity_level]['labelpad']) 
        plt.xticks(SYSTEMS, ticks)
        plt.yticks([1, HELPER[severity_level]['maximum']])

        ax = pl.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(y_fmt))

        axes = plt.gca()
        axes.set_ylim([0, HELPER[severity_level]['maximum']])

        plt.bar(SYSTEMS, plot_specification[severity_level][0], alpha=0.7, color='#f8b335')

        accumulator = plot_specification[severity_level][0]
        plt.bar(SYSTEMS, plot_specification[severity_level][1], bottom=accumulator, alpha=0.7, color='#83dd70')

        accumulator = [a + b for a, b in zip(accumulator, plot_specification[severity_level][1])]
        plt.bar(SYSTEMS, plot_specification[severity_level][2], bottom=accumulator, alpha=0.7, color='#b09cdb')

        patches = [
            Patch(facecolor='#f8b335'),
            Patch(facecolor='#83dd70'),
            Patch(facecolor='#b09cdb')
        ]
        plt.legend(patches, [r'Crevices', r'Dust Storms', r'Rough Terrain'], ncol=1, handletextpad=0.3, labelspacing=0.2, prop={'size': 12})

        plt.tight_layout()

        figure.savefig(f'{PLOT_DIRECTORY}/results-{HELPER[severity_level]["file_key"]}.pdf', bbox_inches='tight')
