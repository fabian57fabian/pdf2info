import sys
sys.path.insert(0, "../")
from core.analysis.results_plotter import plot_results
from core.analysis.check_results_over_groundtruth import load_groundtruth, check_results




if __name__ == '__main__':
    csv_folder="csv_extracted"
    gth = load_groundtruth("GROUNDTRUTH_DATASET_50.csv")
    res, res_percentage = check_results(csv_folder, gth)
    # res into list
    results = res_percentage
    plot_results(results)
