import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import utils

PLOT_DIRECTORY = "plots"

SEVERITY_LEVEL_COUNT = 5
SEVERITY_LEVELS = list(range(SEVERITY_LEVEL_COUNT))


def plot(nothing_results, baseline_results, proposed_results):
    for safety_concern_event in ['single-safety-concern', 'crevice,dust-storm', 'crevice,rough-terrain', 'dust-storm,rough-terrain', 'crevice,dust-storm,rough-terrain']:
        figure = plt.figure(figsize=(7, 1.6))

        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = ['Times'] + plt.rcParams['font.serif']
        plt.rcParams["font.size"] = 14
        plt.rcParams["text.usetex"] = True

        plt.margins(x=0.01, y=0.01)
        plt.xticks([0, 1, 2, 3, 4], ('$\ell = 5$', '$\ell = 4$', '$\ell = 3$', '$\ell = 2$', '$\ell = 1$'))
        plt.yticks([0, 20, 40, 60, 80, 100], ('0.0', '0.2', '0.4', '0.6', '0.8', '1.0'))

        plt.ylabel('$\Pr(\ell)$')

        axes = plt.gca()
        axes.set_ylim([-7, 107])

        if safety_concern_event == 'single-safety-concern':
            baseline_data = [0, 0, 0, 0, 0]
            proposed_data = [0, 0, 0, 0, 0]
            nothing_data = [0, 0, 0, 0, 0]

            for single_safety_concern in ['crevice', 'dust-storm', 'rough-terrain']:
                for index, severity_level in enumerate(['severity_level_5', 'severity_level_4', 'severity_level_3', 'severity_level_2', 'severity_level_1']):
                    nothing_data[index] += nothing_results[single_safety_concern][severity_level]
                    proposed_data[index] += proposed_results[single_safety_concern][severity_level]
                    baseline_data[index] += baseline_results[single_safety_concern][severity_level]

            total = sum(proposed_data)
            proposed_data = [x / total for x in proposed_data]
            proposed_data = [x * 100 for x in proposed_data]

            total = sum(baseline_data)
            baseline_data = [x / total for x in baseline_data]
            baseline_data = [x * 100 for x in baseline_data]

            total = sum(nothing_data)
            nothing_data = [x / total for x in nothing_data]
            nothing_data = [x * 100 for x in nothing_data]
        else:
            baseline_data = [x * 100 for x in baseline_results[safety_concern_event].values()][0:5]
            proposed_data = [x * 100 for x in proposed_results[safety_concern_event].values()][0:5]
            nothing_data = [x * 100 for x in nothing_results[safety_concern_event].values()][0:5]

        plt.plot(SEVERITY_LEVELS, nothing_data, label="No Metareasoning", color='indianred', zorder=15, marker='s')
        plt.fill_between(SEVERITY_LEVELS, nothing_data, [-7, -7, -7, -7, -7], color='indianred', alpha=0.25, zorder=10)

        plt.plot(SEVERITY_LEVELS, baseline_data, label="Objective[Simple]", color='steelblue', zorder=20, marker='.', markersize=12)
        plt.fill_between(SEVERITY_LEVELS, baseline_data, [-7, -7, -7, -7, -7], color='steelblue', alpha=0.25, zorder=11)

        plt.plot(SEVERITY_LEVELS, proposed_data, label="Objective[Lexicographic]", color='mediumseagreen', zorder=25, marker='^', markersize=5.5)
        plt.fill_between(SEVERITY_LEVELS, proposed_data, [-7, -7, -7, -7, -7], color='mediumseagreen', alpha=0.25, zorder=12)
        
        plt.legend(ncol=3, handletextpad=0.3, labelspacing=0.2, loc='upper center', prop={'size': 10, 'variant': 'small-caps'}).set_zorder(100)

        plt.tight_layout()
        
        figure.savefig(f'{PLOT_DIRECTORY}/analysis-{safety_concern_event}.pdf', bbox_inches='tight')


def main():
    none_results = utils.load_plot_data('none_approach')
    baseline_results = utils.load_plot_data('baseline_approach')
    proposed_results = utils.load_plot_data('proposed_approach')
    plot(none_results, baseline_results, proposed_results)


if __name__ == '__main__':
    main()
