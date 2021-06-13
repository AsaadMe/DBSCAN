import functools

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, TextBox
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs, make_circles, make_moons


def load_data(file_name):
    with open(file_name, "r") as file:
        datas = []
        for line in file:
            x, y = line.strip().split(",")
            datas.append([float(x), float(y)])
    return np.array(datas)


def compute_dbscan(dataset, subplot, eps, min_samples):
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(dataset)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    
    for k, color in zip(unique_labels, colors):
        if k == -1:
            color = [0, 0, 0, 1]  # black

        class_member_mask = (labels == k)

        xy = dataset[class_member_mask & core_samples_mask]
        subplot.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(color),
            markeredgecolor='k', markersize=10)
        
        xy = dataset[class_member_mask & ~core_samples_mask]
        subplot.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(color),
            markeredgecolor='k', markersize=4)

    subplot.set_title(f'clusters: {n_clusters_}', size=10)


def ax5_on_click(event, ax, points):
    if event.inaxes == ax:
        points.append([event.xdata, event.ydata])
        ax.plot(event.xdata, event.ydata, 'o', markeredgecolor='k')
        event.canvas.draw()


def go_btn(event, ax, points, eps_txt, min_sam_txt):
    ax.cla()
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    compute_dbscan(np.array(points), ax, 
        float(eps_txt.text), float(min_sam_txt.text))
    event.canvas.draw()


def reset_btn(event, ax, points):
    points.clear()
    ax.cla()
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    event.canvas.draw()


def main():
    smiley_face = load_data("smiley-face.txt")
    density_bars = load_data("density-bars.txt")
    #noisy_circles, _ = make_circles(n_samples=1500, factor=.5, noise=.05)
    noisy_moons, _ = make_moons(n_samples=1500, noise=.05)
    gaussian_mixture, _ = make_blobs(n_samples=1500, random_state=8)
    rings = np.array([[0, 0], [1, 0], [-1, 0], [0, -1], [0, 1]])

    points = []

    f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(
        2, 3, figsize=(11, 7), dpi=95)

    ax5.set_xlim([0, 100])
    ax5.set_ylim([0, 100])

    datasets = [(density_bars, ax1, 5, 7),
                (smiley_face, ax2, 5, 7),
                (gaussian_mixture, ax3, 1, 4),
                (noisy_moons, ax4, 0.1, 4),
                (rings, ax6, 1, 4)]

    for (dataset, subplot, eps, min_samples) in datasets:
        compute_dbscan(dataset, subplot, eps, min_samples)

    f.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(bottom=0.18)
    f.canvas.mpl_disconnect(f.canvas.manager.key_press_handler_id)
    f.canvas.manager.set_window_title('DBSCAN')
    
    axbox1 = plt.axes([0.45, 0.08, 0.05, 0.03])
    eps_textbox = TextBox(axbox1, "Epsilon ")
    eps_textbox.set_val("3")
    
    axbox2 = plt.axes([0.45, 0.04, 0.05, 0.03])
    min_samples_textbox = TextBox(axbox2, "Min Samples ")
    min_samples_textbox.set_val("5")

    axgo = plt.axes([0.52, 0.08, 0.07, 0.03])
    bgo = Button(axgo, 'GO')
    bgo.on_clicked(functools.partial(go_btn, ax=ax5, points=points,
        eps_txt=eps_textbox, min_sam_txt=min_samples_textbox))

    axreset = plt.axes([0.52, 0.04, 0.07, 0.03])
    breset = Button(axreset, 'Reset')
    breset.on_clicked(functools.partial(reset_btn, ax=ax5, points=points))
    
    plt.connect('button_press_event', functools.partial(ax5_on_click, 
                                        ax=ax5, points=points))
    
    plt.show()


if __name__ == "__main__":
    main()
