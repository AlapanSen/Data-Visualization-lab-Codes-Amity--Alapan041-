import numpy as np
import matplotlib.pyplot as plt
x = np.random.rand(50)
y = -x + np.random.normal(0, 0.1, 50)
x = np.append(x, 0.2)
y = np.append(y, 2)
plt.scatter(x, y)
plt.xlabel('X values')
plt.ylabel('Y values')
plt.title('Negative correlation with outlier')
plt.show()