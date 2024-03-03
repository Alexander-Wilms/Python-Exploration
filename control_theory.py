import control
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("QtAgg")

# Free body diagram

#     ↑ F
# |--------|
# |   m    | - x=0
# |--------|
#    |   |
# d |▄|  < k
#   ---  >
#    |   |
# -----------
# //////////

# Parameters defining the system
m = 100.0  # mass
k = 50.0  # spring constant
d = 25.0  # dampening constant

# Equation of forces
# obtained from the free body diagram of the mass being displaced by a force F
# m*x'' = F(t) - F_d(t) - F_k(t)

# Express forces in terms of derivatives of x(t)
# m*x''(t) = F(t) - d*x'(t) - k*x(t)
# F(t) = m*x''(t) + d*x'(t) + k*x(t)

# Laplace transform from time domain to frequency domain
# F(s) = m*X(s)*s^2+d*X(s)*s+k*X(s)

# Solving for the transfer function
# the TF expresses the relation of displacement and applied force
# G(s) = X(s)/F(s)
# G(s) = X(s)/(m*X(s)*s^2+d*X(s)*s+k*X(s))

# X(s) cancels out
# G(s) = 1/(m*s^2+d*s+k)

# Numerator and denominator coefficients of the PT2 transfer function
num = [1]
den = [m, d, k]

sys = control.TransferFunction(num, den)

plt.figure(1)
x, T = control.step_response(sys)
plt.plot(x, T)
plt.show(block=False)

plt.figure(2)
control.bode_plot(sys, np.logspace(-2, 2))
plt.show(block=False)

plt.figure(3)
control.nyquist_plot(sys)
plt.show(block=False)

plt.figure(4)
control.root_locus(sys)

plt.show()
