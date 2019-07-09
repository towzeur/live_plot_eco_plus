import matplotlib.pyplot as plt
import time
import numpy as np
import collections


def live_plot(metrics, figure_dsc, progress=True, fps=10, obs_window=30):
    '''
    :param list metrics: [{'label':'F', 'color':'r', 'get_function':f1},
                                            ...
                          {'label':'H', 'color':'b', 'get_function':f2}]

    :param dict figure_dsc : {'title'  : '?', 'ylabel' : '?'}

    :param bool progress : expand the Xaxis while the elapsed time reach the obs window if true

    :param int fps : framerate

    :param int obs_window : final observation time in second

    :return: elapsed time in ticks (there is fps ticks in 1 second)
    '''

    dt = 1 / fps
    N = fps * obs_window
    n_metrics = len(metrics)

    plt.ion()
    plt.plot()

    deques = [collections.deque(maxlen=N) for _ in range(n_metrics)]

    X0 = np.linspace(0, obs_window, N)
    X = np.array([])
    n = 0
    while plt.get_fignums():
        t0 = time.time()

        # clear
        plt.clf()

        # (X axis)
        if n < N:
            X = X0[:n + 1]
            if not progress:
                plt.xlim(0, X0[-1])
        else:
            X += dt

        # (Y axis)
        for i in range(n_metrics):
            # query and add the new value
            deques[i].append(metrics[i]['get_function'](n / fps))
            # plot it
            plt.plot(X, deques[i], metrics[i]['color'], label=metrics[i]['label'])

        plt.title(figure_dsc.get('title', ''))
        plt.xlabel('Temps en s')
        plt.ylabel(figure_dsc.get('ylabel', ''))
        plt.legend(loc='lower right')
        plt.grid()
        plt.draw()

        # wait if necessary
        elapsed = time.time() - t0
        left = dt - elapsed
        if left > 0:
            plt.pause(left)
        else:
            print('dépassement en temps de ', -left)
        n += 1

    plt.show(block=True)
    return


def get_U(t):
    return np.cos(2 * np.pi * t)


def get_I(t):
    return 0.1 * np.cos(2 * np.pi * t + np.pi / 2)


m = [{'label': 'U : voltage',
      'color': 'r',
      'get_function': get_U},

     {'label': 'I : current',
      'color': 'b',
      'get_function': get_I}
     ]

f_d = {'title': '',
       'ylabel': 'Voltage(V) / Current(A)'}

live_plot(m, f_d, progress=True, fps=16, obs_window=4)
