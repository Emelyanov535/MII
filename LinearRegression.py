import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def calc_coeff(x: list[float], y: list[float]) -> tuple:
    a = len(y)
    b = sum(x)
    c = sum(y)
    d = sum([i * i for i in x])
    e = sum([x[i] * y[i] for i in range(len(y))])

    b1 = (a * e - c * b) / (a * d - b * b)
    b0 = (c - b1 * b) / a
    return b0, b1


def do_predict(b0: float, b1: float, x: list[float]) -> list[float]:
    y = [b1 * i + b0 for i in x]
    return y


def buildRegression():
    data = pd.read_csv('data.csv', delimiter=',')
    data = data.groupby(['unemploymentrate'])['oil prices'].agg([np.average]).reset_index()

    all_prices = list(map(float, data['average']))
    all_unemploymentrate = list(map(float, data['unemploymentrate']))

    max_price, min_price = max(all_prices), min(all_prices)
    all_prices = [(i - min_price) / (max_price - min_price) for i in all_prices]

    price = all_prices[:len(all_prices) - int(len(all_prices) * 0.1)]
    unemploymentrate = all_unemploymentrate[:len(all_prices) - int(len(all_unemploymentrate) * 0.1)]

    check_price = all_prices[len(all_prices) - int(len(all_prices) * 0.1):]
    check_unemploymentrate = all_unemploymentrate[len(all_unemploymentrate) - int(len(all_unemploymentrate) * 0.1):]

    plt.title('99% data')
    plt.plot(unemploymentrate, price, 'ro')
    b0, b1 = calc_coeff(unemploymentrate, price)
    plt.plot(unemploymentrate, do_predict(b0, b1, unemploymentrate))
    plt.text(min(unemploymentrate), max(price), f'y={b1:.4f}*x + {b0:.4f}', fontsize=20, bbox={'facecolor': 'yellow', 'alpha': 0.2})
    plt.show()

    plt.title('1 % data')
    plt.plot(check_unemploymentrate, check_price, 'ro')
    b0, b1 = calc_coeff(check_unemploymentrate, check_price)
    plt.plot(check_unemploymentrate, do_predict(b0, b1, check_unemploymentrate))
    plt.text(min(check_unemploymentrate), max(check_price), f'y={b1:.4f}*x + {b0:.4f}', fontsize=20,
             bbox={'facecolor': 'yellow', 'alpha': 0.2})

    plt.show()
