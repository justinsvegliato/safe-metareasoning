import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from numpy.core.numeric import ComplexWarning, base_repr

import utils

PLOT_DIRECTORY = "plots"

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(SEVERITY_LEVEL_COUNT))

SAFETY_CONCERNS = {'crevice': "Crevice", 'dust-storm': "Dust Storm", 'rough-terrain': "Rough Terrain"}
SAFETY_CONCERN_EVENTS = utils.get_safety_concern_events(SAFETY_CONCERNS)

HELPER = {
    "none": {'maximum': 100},
    "crevice": {'maximum': 100},
    "dust-storm": {'maximum': 100},
    "rough-terrain": {'maximum': 100},
    "crevice,dust-storm": {'maximum': 100},
    "crevice,rough-terrain": {'maximum': 100},
    "dust-storm,rough-terrain": {'maximum': 100},
    "crevice,dust-storm,rough-terrain": {'maximum': 100}
}


def plot(baseline_results, proposed_results):
    for safety_concern_event in SAFETY_CONCERN_EVENTS:
        figure = plt.figure(figsize=(7, 1.6))

        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = ['Times'] + plt.rcParams['font.serif']
        plt.rcParams["font.size"] = 14
        plt.rcParams["text.usetex"] = True

        plt.margins(x=0.01, y=0.01)
        plt.xticks([0, 1, 2, 3, 4], ('$\ell = 5$', '$\ell = 4$', '$\ell = 3$', '$\ell = 2$', '$\ell = 1$'))
        plt.yticks([0, 20, 40, 60, 80, 100], ('0.0', '0.2', '0.4', '0.6', '0.8', '1.0'))

        axes = plt.gca()
        # axes.set_ylim([0, HELPER[safety_concern_event]['maximum']])
        axes.set_ylim([-7, 107])

        baseline_data = [x * 100 for x in baseline_results[safety_concern_event].values()][0:5]
        # baseline_data = [15.05, 20.40, 6.02, 12.04, 46.49]
        # baseline_data = [0, 0, 0, 0, 100]
        plt.scatter(SEVERITY_LEVELS, baseline_data, label="Naive Conflict Resolution", color='indianred', zorder=15, marker='s')
        plt.plot(SEVERITY_LEVELS, baseline_data, color='indianred', zorder=15)
        plt.fill_between(SEVERITY_LEVELS, baseline_data, [-7, -7, -7, -7, -7], color='red', alpha=0.1, zorder=10)

        proposed_data = [x * 100 for x in proposed_results[safety_concern_event].values()][0:5]
        # proposed_data = [11.16, 16.71, 6.63, 31.56, 33.94]
        # proposed_data = [0, 0, 0, 0, 100]
        plt.scatter(SEVERITY_LEVELS, proposed_data, label="Proposed Conflict Resolution", color='seagreen', zorder=25, marker='x')
        plt.plot(SEVERITY_LEVELS, proposed_data, color='seagreen', zorder=25)
        plt.fill_between(SEVERITY_LEVELS, proposed_data, [-7, -7, -7, -7, -7], color='green', alpha=0.1, zorder=12)
        
        plt.legend(ncol=1, handletextpad=0.3, labelspacing=0.2, loc='upper left', prop={'size': 10})

        plt.tight_layout()
        
    figure.savefig(f'{PLOT_DIRECTORY}/results-{safety_concern_event}.pdf', bbox_inches='tight')
    # figure.savefig(f'{PLOT_DIRECTORY}/results-test.pdf', bbox_inches='tight')

# plot(1, 1)