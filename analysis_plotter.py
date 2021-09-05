import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


import utils

PLOT_DIRECTORY = "plots"

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(SEVERITY_LEVEL_COUNT))

SAFETY_CONCERNS = {'crevice': "Crevice", 'dust-storm': "Dust Storm", 'rough-terrain': "Rough Terrain"}
SAFETY_CONCERN_EVENTS = utils.get_safety_concern_events(SAFETY_CONCERNS)


def plot(baseline_results, proposed_results):
    for safety_concern_event in SAFETY_CONCERN_EVENTS:
        figure = plt.figure(figsize=(7, 1.6))

        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = ['Times'] + plt.rcParams['font.serif']
        plt.rcParams["font.size"] = 14
        plt.rcParams["text.usetex"] = True

        plt.margins(x=0.01, y=0.01)
        # if safety_concern_event == 'crevice,dust-storm,rough-terrain':
        plt.xticks([0, 1, 2, 3, 4], ('$\ell = 5$', '$\ell = 4$', '$\ell = 3$', '$\ell = 2$', '$\ell = 1$'))
        plt.yticks([0, 20, 40, 60, 80, 100], ('0.0', '0.2', '0.4', '0.6', '0.8', '1.0'))

        axes = plt.gca()
        axes.set_ylim([-7, 107])
        # if safety_concern_event != 'crevice,dust-storm,rough-terrain':
            # axes.xaxis.set_ticklabels([])

        proposed_data = [x * 100 for x in proposed_results[safety_concern_event].values()][0:5]
        plt.scatter(SEVERITY_LEVELS, proposed_data, label="Objective[Lexicographic]", color='seagreen', zorder=25, marker='x')
        plt.plot(SEVERITY_LEVELS, proposed_data, color='seagreen', zorder=25)
        plt.fill_between(SEVERITY_LEVELS, proposed_data, [-7, -7, -7, -7, -7], color='green', alpha=0.1, zorder=12)

        baseline_data = [x * 100 for x in baseline_results[safety_concern_event].values()][0:5]
        plt.scatter(SEVERITY_LEVELS, baseline_data, label="Objective[Simple]", color='indianred', zorder=15, marker='s')
        plt.plot(SEVERITY_LEVELS, baseline_data, color='indianred', zorder=15)
        plt.fill_between(SEVERITY_LEVELS, baseline_data, [-7, -7, -7, -7, -7], color='red', alpha=0.1, zorder=10)
        
        plt.legend(ncol=1, handletextpad=0.3, labelspacing=0.2, loc='upper center', prop={'size': 10, 'variant': 'small-caps'})

        plt.tight_layout()
        
        figure.savefig(f'{PLOT_DIRECTORY}/results-{safety_concern_event}.pdf', bbox_inches='tight')

def main():
    baseline_results = utils.load_plot_data('baseline_approach')
    proposed_results = utils.load_plot_data('proposed_approach')
    plot(baseline_results, proposed_results)


if __name__ == '__main__':
    main()
