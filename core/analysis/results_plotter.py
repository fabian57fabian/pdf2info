import os.path
import json

import matplotlib.pyplot as plt
import numpy as np
from  matplotlib.colors import LinearSegmentedColormap

DEFAULT_CMAP = LinearSegmentedColormap.from_list('rg',["w", "g"], N=256)


def show_cmap():
    cmap = DEFAULT_CMAP
    plt.figure(figsize=(3,3))
    v = np.array([np.arange(200) for i in range(200)])
    plt.imshow(v, cmap=cmap)
    plt.axis('off')
    plt.show()


def create_results_plot(json_data:dict, path_out:str):
    data = []
    methods = list(json_data.keys())
    for k, v in json_data.items():
        data.append(list(v.values()))
    fig = plt.subplots(figsize=(16,9))
    bar_width = 0.20
    first_key = list(json_data.keys())[0]
    X = np.arange(len(json_data[first_key]))
    for i, d in enumerate(data):
        plt.bar(X + i*bar_width, d, width=bar_width, label=methods[i])
    scores = list(json_data[first_key].keys())
    plt.xticks([r + bar_width for r in range(len(scores))], scores)
    plt.legend()
    plt.title("Methods rsults")
    plt.savefig(path_out)

def create_csv(path:str, path_out:str):
    with open(path, 'r') as file:
        json_data = json.load(file)
    header_Written = False
    keys_values = []
    with open(path_out, 'w') as file_out:
        for method_used in json_data.keys():
            if not header_Written:
                header_Written = True
                keys_values = list(json_data[method_used].keys())
                file_out.write("method,{}\n".format(",".join(keys_values)))
            file_out.write("{},{}\n".format(method_used, ",".join([str(json_data[method_used][k]) for k in keys_values])))


def update_results(save_to:str, method_used:str, new_data:dict):
    path = os.path.join(save_to, "results.json")
    if os.path.exists(path):
        with open(path, 'r') as file:
            json_data = json.load(file)
    else:
        json_data = {}
    json_data[method_used] = new_data
    with open(path, 'w') as file_out:
        json.dump(json_data, file_out, indent=2)
    create_csv(path, os.path.join(save_to, "results.csv"))
    create_results_plot(json_data, os.path.join(save_to, "results.png"))


def plot_save_results(TP, TN, FP, FN, acc_iou, files_percentage_ok, method_used="pdf2info", color_min=None, color_max=None, cmap=None, figsize=(7,7), save_to=None, show_fig:bool=True):
    if cmap is None: cmap = DEFAULT_CMAP
    fig = plt.figure(figsize=figsize)

    # Compute matrix to show results
    a = np.array(files_percentage_ok)
    ns = np.ceil(np.sqrt(len(files_percentage_ok))).astype(int)
    s = np.zeros(ns ** 2)
    s[:a.size] = a
    y = s.reshape(ns, ns)

    # Compute scores
    tables_num = TP + FN
    precision = (TP) / (TP+FP)
    recall = (TP) / (TP+FN)
    P = TP + FN
    N = 0
    acc = (TP+TN)/(P+N)
    accuracy_over_pdfs = np.mean(y)
    data = {
           "ACC": round(acc*100, 2),
           "P": round(precision*100, 2),
           "R": round(recall*100, 2),
           "TP": TP,
           "FP": FP,
           "FN": FN,
           "TABLES_TOTAL": tables_num,
       }
    interesting_metrics = "{}: ACC: {:.2f}%, P: {:.2f}%, R: {:.2f}%, ({} tables)".format(method_used,  acc*100, precision*100, recall*100, tables_num)
    all_metrics_row = "TP: {}, FP: {}, FN: {}, IoU: {}".format(TP,FP,FN, acc_iou)
    plt.title(interesting_metrics + "\n" + all_metrics_row)
    plt.axis('off')
    plt.imshow(y, cmap=cmap, vmin=color_min, vmax=color_max)
    if show_fig:
        plt.show()
    plt.draw()
    if save_to is not None:
        filename = "{}_on_DATASET.png".format(method_used)
        fig.savefig(os.path.join(save_to, filename))
        update_results(save_to, method_used, data)

