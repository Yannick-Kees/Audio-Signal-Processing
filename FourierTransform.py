import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from math import floor

t = np.arange(0, 1, 0.01)

def fourier_coefficents_of_id(n):
    # Calculation of coefficients like in a) described
    ft = np.zeros(100)

    for k in range(1,n):
        ft += - ((1/(np.sqrt(2)*np.pi*k)) * (np.sqrt(2)*np.sin(2*np.pi*k*t)))
    ft += 0.5
    return ft

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

n = 10 # Start value

plt.plot(t, t, 'r') # plot identity
P, = plt.plot(t, fourier_coefficents_of_id(n))

axamp = plt.axes([0.25, 0.15, 0.65, 0.03])
samp = Slider(axamp, '$n$', 1, 50, valinit=n)

def update(val):
    amp = samp.val
    P.set_ydata(fourier_coefficents_of_id(floor(amp)))
    fig.canvas.draw_idle()

samp.on_changed(update)

print("Use the slider on the plot to adjust the approximation")
plt.show()

"""
If k gets higher, the approximation becomes better
"""
