import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pylab as plb

from translate import translate


# generate data using: https://www.librec.net/datagen.html


def main():
    translate('path_data.csv', 'path_data.dat')  # convert data to ssv
    data = plb.loadtxt('path_data.dat')
    lon = data[:, 0]
    lat = data[:, 1]
    adj_lon, adj_lat = path(data)

    # Plot results.
    plt.plot(lon, lat, 'x', adj_lon, adj_lat, 'r-')
    plt.axis('equal')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()


parabolic_segment_time = 24

min_samples = 4


def path(data):
    lon = data[:, 0]
    lat = data[:, 1]
    t = np.array([i for i in range(len(data))])
    result_lon = []
    result_lat = []

    for i in range(len(data)):
        start = max(i - parabolic_segment_time, 0)
        sampled_lat = lat[start:i + 1]
        if len(sampled_lat) < min_samples:
            result_lon.append(lon[i])  # placeholder
            result_lat.append(lat[i])
            continue
        head_lon, head_lat = parabola_segment_head(
            lon[start:i + 1],
            lat[start:i + 1],
            t[start:i + 1],
        )
        result_lon[i-len(head_lon):] = head_lon
        result_lat[i-len(head_lon):] = head_lat
    return result_lon, result_lat


def parabola_segment_head(lon, lat, times):
    """
    Gets first half of parabolic segment determined from passed points.
    :param lat:
    :param lon:
    :param times: array of times at which samples take place.
    :return: lon points, lat points.
    """
    lat_coefficients, _ = curve_fit(func, times, lat)
    lon_coefficients, _ = curve_fit(func, times, lon)

    lat_adj = func(times, *lat_coefficients)
    lon_adj = func(times, *lon_coefficients)

    return_size = len(lat) // 2
    return lon_adj[-return_size:], lat_adj[-return_size:]


def func(x, a, b, c):
    return a*x + b*x**2 + c


if __name__ == '__main__':
    main()
