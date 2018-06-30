import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
import numpy as np
import pylab as plb

from translate import translate


# generate data using: https://www.librec.net/datagen.html


def main():
    translate()  # convert data to ssv
    data = plb.loadtxt('data.dat')
    lon = data[:, 0]
    lat = data[:, 1]
    t = np.array([i for i in range(len(data))])

    lat_coefficients, _ = curve_fit(func, t, lat)
    lon_coefficients, _ = curve_fit(func, t, lon)

    lat_adj = func(t, *lat_coefficients)
    lon_adj = func(t, *lon_coefficients)

    # Plot results.
    gs = gridspec.GridSpec(2, 2)
    plt.figure(1)
    plt.subplots_adjust(hspace=0.5, wspace=0.35)
    plt.subplot(gs[0, 0])
    plt.title('Longitude')
    plt.plot(t, lon, 'x', t, lon_adj, 'r-')
    plt.xlabel('time')
    plt.ylabel('longitude')
    plt.subplot(gs[1, 0])
    plt.title('Latitude')
    plt.plot(t, lat, 'x', t, lat_adj, 'r-')
    plt.xlabel('time')
    plt.ylabel('latitude')
    plt.subplot(gs[:, 1])
    plt.title('Position')
    plt.plot(lon, lat, 'x')
    plt.plot(lon_adj, lat_adj, 'r-')
    plt.axis('equal')
    plt.margins(0.15, 0.15)
    v_lat = func(t[-1] + 2, *lat_coefficients) - lat_adj[-1]
    v_lon = func(t[-1] + 2, *lon_coefficients) - lon_adj[-1]
    plt.plot(lon_adj[-1], lat_adj[-1], 'ro')  # current pos
    plt.arrow(lon_adj[-1], lat_adj[-1], v_lon, v_lat, fc="k", ec="k",
              head_width=1, head_length=2)  # velocity arrow / prediction
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()


def func(x, a, b, c):
    return a*x + b*x**2 + c


if __name__ == '__main__':
    main()
