import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pylab as plb

from translate import translate


# generate data using: https://www.librec.net/datagen.html


def main():
    translate('path_data.csv', 'path_data.dat')  # Convert data to ssv.
    data = plb.loadtxt('path_data.dat')
    lon = data[:, 0]  # Get array of longitudes from array of positions
    lat = data[:, 1]  # Get array of latitudes from array of positions.
    path_lon, path_lat = path(data)  # Get path lon and lat positions.

    # Plot results.
    plt.plot(lon, lat, 'x', path_lon, path_lat, 'r-')  # plot points and line.
    plt.axis('equal')  # Set both axis in plot to scale equally.
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()


parabolic_segment_time = 24

min_samples = 4


def path(data):
    lon = data[:, 0]  # Get lon positions from first half of data elements.
    lat = data[:, 1]  # Get lat positions from second half of data elements.
    t = np.array([i for i in range(len(data))])  # Get(create) position times.
    result_lon = []
    result_lat = []

    for i in range(len(data)):
        start = max(i - parabolic_segment_time, 0)
        sampled_lat = lat[start:i + 1]
        if len(sampled_lat) < min_samples:
            result_lon.append(lon[i])
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
    :param lat: array of latitude positions.
    :param lon: array of longitude positions.
    :param times: array of times at which samples take place.
    :return: lon points, lat points.
    """
    lat_coefficients, _ = curve_fit(parabola_func, times, lat)
    lon_coefficients, _ = curve_fit(parabola_func, times, lon)

    lat_adj = parabola_func(times, *lat_coefficients)
    lon_adj = parabola_func(times, *lon_coefficients)

    return_size = len(lat) // 2
    return lon_adj[-return_size:], lat_adj[-return_size:]


def parabola_func(x, a, b, c):
    return a*x + b*x**2 + c


if __name__ == '__main__':
    main()
