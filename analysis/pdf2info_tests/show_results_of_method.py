import logging
import sys
sys.path.insert(0, "../../")
from core.analysis.results_plotter import plot_save_results
from core.analysis.check_results_over_groundtruth import load_groundtruth, check_results


def create_plots_results(method_used:str, show_fig:bool=True):
    csv_folder = "csv_extracted"
    gth = load_groundtruth("../DATASET/GROUNDTRUTH_DATASET.csv")
    TP, TN, FP, FN, files_percentage_ok = check_results(csv_folder, gth, split_char='_')
    plot_save_results(TP, TN, FP, FN, files_percentage_ok, method_used=method_used,  color_min=0, color_max=100, save_to="../results", show_fig=show_fig)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    method_used = 'linesearch'
    create_plots_results(method_used, show_fig=True)

