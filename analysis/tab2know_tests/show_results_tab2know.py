import sys
sys.path.insert(0, "../../")
from core.analysis.results_plotter import plot_results
from core.analysis.check_results_over_groundtruth import load_groundtruth, check_results


if __name__ == '__main__':
    csv_folder="out_tab2know/csv"
    gth = load_groundtruth("../DATASET/GROUNDTRUTH_DATASET.csv")
    TP, TN, FP, FN, files_percentage_ok = check_results(csv_folder, gth, split_char='-')
    plot_results(TP, TN, FP, FN, files_percentage_ok, title="tab2know: ", color_min=0, color_max=100, save_to="../results/tab2know_on_DATASET.png")
