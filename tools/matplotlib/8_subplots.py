import matplotlib.pyplot as plt
import numpy as np


figure,axes = plt.subplots(2,3, figsize=[40,20])
axes = axes.flatten()

x = np.arange(0,20) 
y1 = pow(x,2)
axes[0].plot(x, y1) 


plt.show()
