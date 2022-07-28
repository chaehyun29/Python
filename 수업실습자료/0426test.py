import numpy as np
a = [1, 2, 3, 4, 5]
padded = np.pad(a, (2, 3), 'constant', constant_values=(4, 6))
print(padded)