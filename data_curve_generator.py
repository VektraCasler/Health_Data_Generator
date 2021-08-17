import matplotlib.pyplot as plt
import numpy as np

mu, sigma = 100, 1
s = np.random.normal(mu, sigma, 1000)

print(abs(mu-np.mean(s)))

print(abs(sigma-np.std(s, ddof=1)))


count, bins, ignored = plt.hist(s, 30, density=True)

plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
plt.show()