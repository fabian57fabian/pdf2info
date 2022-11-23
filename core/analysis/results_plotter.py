import matplotlib.pyplot as plt
import numpy as np
from  matplotlib.colors import LinearSegmentedColormap


def plot_results(res, color_min=None, color_max=None, cmap=None):
    if cmap is None:
        cmap = LinearSegmentedColormap.from_list('rg',["w", "g"], N=256)
    plt.figure(figsize=(9,9))
    a = np.array(res)
    ns = np.ceil(np.sqrt(len(res))).astype(int)
    s = np.zeros(ns ** 2)
    s[:a.size] = a
    y = s.reshape(ns, ns)
    plt.title("{:.2f}%".format(np.mean(y)))
    plt.imshow(y, cmap=cmap, vmin=color_min, vmax=color_max)
    plt.show()


if __name__ == '__main__':
    test_data = [1,3,4,5,1,24,25,245,45,2,11,31,214,3,24,124,1,1,2]
    plot_results(test_data)
