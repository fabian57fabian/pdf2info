import os.path

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


def plot_results(TP, TN, FP, FN, files_percentage_ok, color_min=None, color_max=None, cmap=None, figsize=(7,7), save_to=None):
    if cmap is None: cmap = DEFAULT_CMAP
    fig = plt.figure(figsize=figsize)
    a = np.array(files_percentage_ok)
    ns = np.ceil(np.sqrt(len(files_percentage_ok))).astype(int)
    s = np.zeros(ns ** 2)
    s[:a.size] = a
    y = s.reshape(ns, ns)
    tables_num = TP + FN
    precision = (TP) / (TP+FP)
    recall = (TP) / (TP+FN)
    P = TP + FN
    N = 0
    acc = (TP+TN)/(P+N)
    accuracy_over_pdfs = np.mean(y)
    plt.title("acc: {:.2f}% ({:.2f}% pdf), precision:{:.2f}%, recall:{:.2f}%, tables num:{}".format(acc*100, accuracy_over_pdfs, precision*100, recall*100, tables_num))
    plt.axis('off')
    plt.imshow(y, cmap=cmap, vmin=color_min, vmax=color_max)
    plt.show()
    plt.draw()
    if save_to is not None:
        fig.savefig(save_to)

