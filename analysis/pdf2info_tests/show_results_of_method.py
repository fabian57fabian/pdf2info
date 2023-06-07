import sys
sys.path.insert(0, "../../")
from core.analysis.results_plotter import plot_results
from core.analysis.check_results_over_groundtruth import load_groundtruth, check_results


def create_plots_results(method_used:str, show_fig:bool=True):
    csv_folder = "csv_extracted"
    gth = load_groundtruth("../DATASET/GROUNDTRUTH_DATASET.csv")
    TP, TN, FP, FN, files_percentage_ok = check_results(csv_folder, gth, split_char='_')
    plot_results(TP, TN, FP, FN, files_percentage_ok, title=method_used,  color_min=0, color_max=100, save_to="../results/{}_on_DATASET.png".format(method_used))


if __name__ == '__main__':
    method_used = 'linesearch'
    create_plots_results(method_used, show_fig=True)

