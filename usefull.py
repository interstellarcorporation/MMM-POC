"""
Usefull functions

@date: 30/08/2019
@author: Quentin Lieumont
"""
from matplotlib import pyplot as plt
import numpy as np


def nmap(func: callable, l) -> np.array:
    """
    Map build-in function for numpy
    :param func: the function to map like f
    :param l: a list like [a, b, c] (or numpy array)
    :return: numpy.array(f(a), f(b), f(c))
    """
    return np.array(list(map(func, l)))


def plot_color(
    z: iter, x: iter = None, y: iter = None, nb_ticks: int = 5, plot_title: str = ""
) -> plt:
    """
    plot a 2D colored graph of a 2D array
    :param z: the 2D array
    :param x: x axis label
    :param y: y axis label
    :param nb_ticks: number of labels over 1 axis
    :param plot_title: the plot title
    :return: the pyplot (if you want to save it)
    """
    fig, ax = plt.subplots()
    im = ax.imshow(z)
    # ax.plot([len(z) - 0.5, -0.5], [-0.5, len(z) - 0.5], "-k")
    if plot_title is not "":
        ax.title._text = plot_title
    fig.tight_layout()
    fig.colorbar(im)
    if x is not None:
        if y is None:
            y = x
        ticks_pos_x = nmap(int, np.arange(nb_ticks) * (len(x) - 1) / (nb_ticks - 1))
        ticks_pos_y = nmap(int, np.arange(nb_ticks) * (len(y) - 1) / (nb_ticks - 1))
        ax.set_xticks(ticks_pos_x)
        ax.set_yticks(ticks_pos_y)
        ax.set_xticklabels([x[i] for i in ticks_pos_x])
        ax.set_yticklabels([y[i] for i in ticks_pos_y])
    return fig
