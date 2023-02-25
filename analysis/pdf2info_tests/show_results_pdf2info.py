import sys
sys.path.insert(0, "../../")
from core.analysis.results_plotter import plot_results
from core.analysis.check_results_over_groundtruth import load_groundtruth, check_results


if __name__ == '__main__':
    csv_folder="csv_extracted"
    gth = load_groundtruth("../DATASET/GROUNDTRUTH_DATASET.csv")
    res, res_percentage = check_results(csv_folder, gth, split_char='_')
    plot_results(res_percentage, color_min=0, color_max=100, save_to="../results/pdf2info_on_DATASET.png")
