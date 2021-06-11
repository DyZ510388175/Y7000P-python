import pandas as pd
import numpy as np

epsilon = 1
k = 3
matrix = np.full(shape=(k, k), fill_value=1 / (np.e ** epsilon + k - 1))
print("-----matrix------")
print(matrix)
for i in range(k):
    matrix[i][i] = np.e ** epsilon / (np.e ** epsilon + k - 1)
print("-----matrix------")
print(matrix)
probability_list = matrix[2]
print("-----probability_list------")
print(probability_list)
print("-----np.random.choice------")
print(np.random.choice(a=range(k),size=2, p=probability_list))
print("-----np.zeros------")
print(np.zeros(shape=k))
print("-----np.full------")
print(np.full(shape=5, fill_value=1.0 / 5))
print("-----gauss------")
u = 10 / 2
sigma = 10 / 6
x = np.arange(1, 10+1)
fx = 1 / (np.sqrt(2*np.pi) * sigma) * np.e**(- (x-u)**2 / (2 * sigma**2))
print(fx / sum(fx))
