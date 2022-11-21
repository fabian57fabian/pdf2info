import sys
sys.path.insert(0, "../")
from core.analysis.results_plotter import plot_results
from core.analysis.check_results_over_groundtruth import load_groundtruth, check_results




if __name__ == '__main__':
    csv_folder="csv_extracted"
    gth = load_groundtruth("GROUNDTRUTH_TEST_200.csv")
    res = check_results(csv_folder, gth)
    # res into list
    results = [] # res
    plot_results(results)
