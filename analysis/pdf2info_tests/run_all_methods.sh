#/bin/bash

python3 execute_method_on_DATASET.py --method camelot
python3 show_results_of_method.py --hide --method camelot

python3 execute_method_on_DATASET.py --method tabula
python3 show_results_of_method.py --hide --method tabula

python3 execute_method_on_DATASET.py --method linesearch
python3 show_results_of_method.py --hide --method linesearch

python3 execute_method_on_DATASET.py --method camelot_and_linesearch
python3 show_results_of_method.py --hide --method camelot_and_linesearch

python3 execute_method_on_DATASET.py --method tabula_and_linesearch
python3 show_results_of_method.py --hide --method tabula_and_linesearch