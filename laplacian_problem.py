import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import timeit
import sys
from numpy import linalg as LA

np.set_printoptions(threshold=sys.maxsize)

def Laplacian_Problem(n):

    #grid
    f = np.zeros((n, n))

    # Boundary conditions

    # Top
    f[0, :(n // 4)] = np.arange(13, 5, -(13 - 5) / (n // 4))
    f[1, :(n // 4)] = np.arange(13, 5, -(13 - 5) / (n // 4))

    f[:2, (n // 4):(3 * n // 4)] = 5

    f[0, (3 * n // 4):] = np.arange(5, 13, (13 - 5) / (n // 4))
    f[1, (3 * n // 4):] = np.arange(5, 13, (13 - 5) / (n // 4))

    # Bottom
    f[n-1:, :] = 21

    # Left
    f[:(3 * n // 8), 0] = np.arange(13, 40, ((40 - 13) / (3 * n // 8)))
    f[:(3 * n // 8), 1] = np.arange(13, 40, ((40 - 13) / (3 * n // 8)))

    f[(n // 2):, 0] = np.arange(40, 21, -((40 - 21) / (n // 2)))
    f[(n // 2):, 1] = np.arange(40, 21, -((40 - 21) / (n // 2)))

    # Right

    f[:(n // 2), -1] = np.arange(13, 40, ((40 - 13) / (n // 2)))
    f[:(n // 2), -2] = np.arange(13, 40, ((40 - 13) / (n // 2)))

    f[(5 * n // 8):, -1] = np.arange(40, 21, -((40 - 21) / (3 * n // 8)))
    f[(5 * n // 8):, -2] = np.arange(40, 21, -((40 - 21) / (3 * n // 8)))

    # Heater
    f[(3 * n // 8):(n // 2) + 1, :(n // 8 + 1)] = 40

    f[(n // 2):(5 * n // 8) + 1, -(n // 8 + 1):] = 40

    return f

def jacobi_step(T):

    m, n = T.shape

    _T = np.copy(T)

    # iterate over interior

    for i in range(2, m-1):
        for j in range(2, n-1):

            _T[i, j] = (T[i+1, j] + T[i-1, j] + T[i, j-1] + T[i, j+1]) / 4

    return _T

def simulation(T, epsilon=None, num_steps=None):

    global _T, residual
    m, n = T.shape

    iteration_list = []
    l2_list = []
    residual = 1

    for i in range(num_steps):

        i += 1
        # Heater should be there at its own place all the time
        T[(3 * n // 8):(n // 2) + 1, :(n // 8 + 1)] = 40
        T[(n // 2):(5 * n // 8) + 1, -(n // 8 + 1):] = 40

        _T = jacobi_step(T)
        error = _T - T
        T = _T

        l2_norm = LA.norm(error)
        l2_list.append(l2_norm)

        iteration_list.append(i)

        if residual < np.log10(epsilon):
            print("Convergence Criteria satisfied")
            print("Solution converged in {} iterations".format(i))
            break

        l2_array = np.asarray(l2_list)
        maximum_value = l2_array.max()
        resi_drop = l2_array / maximum_value

        residual_list = np.log(resi_drop).reshape(-1, 1)
        iteration = np.asarray(iteration_list).reshape(-1, 1)

        residual = residual_list[-1]

        if i == num_steps-1:
            print("Iteration criteria satisfied")
            print("Solution converged in {} iterations".format(i))

    plt.plot(iteration, residual_list)
    plt.xlabel("Iterations")
    plt.ylabel("Residual drop")
    plt.show()
    return _T

# Making the grid with BC
A = Laplacian_Problem(16)

# Visualizing the problem
sn.heatmap(A)
plt.show()

start = timeit.default_timer()
# Running the simulation
B = simulation(A, epsilon=1e-02, num_steps=200)
end = timeit.default_timer()

print("runtime: {} s".format(float(round(end - start, 3))))
# Approximate solution
sn.heatmap(B)
plt.show()