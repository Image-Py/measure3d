# -*- coding: utf-8 -*-
import numpy as np
from numpy.linalg import norm
import sys
sys.path.append('../')
from measure3d import Manager

manager = Manager()
manager.config(1, 1, 1, False)

manager.point('A', 0, 0, 0, True)
manager.point('B', 2, 0, 0, True)
manager.point('C', 1, 1, 1, False)

manager.start('A')
manager.ts('A', 'C', np.pi / 4, np.arctan(1 / np.sqrt(2)), np.sqrt(3))
manager.ts('A', 'B', 0, 0, 2)
manager.end();

manager.start('B')
manager.ts('B', 'C', np.pi / 4 * 3, np.arctan(1 / np.sqrt(2)), np.sqrt(3))
manager.ts('B', 'A', np.pi, 0, 2)
manager.end();

print(manager.solve(1E-1, 1))
print(manager.reporter.get_result())
print(manager.reporter.get_points())
