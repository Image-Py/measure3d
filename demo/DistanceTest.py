# -*- coding: utf-8 -*
import numpy as np
import math
from numpy.linalg import norm
import sys
sys.path.append('../')
from measure3d import Manager

manager = Manager(3, 1e-3, 1)
manager.enable3d = False
manager.point('A', 53743.136, 61003.826, 0, True)
manager.point('B', 47943.002, 66225.854, 0, True)
manager.point('C', 40049.229, 53782.790, 0, True)
manager.point('D', 36924.728, 61027.086, 0, True)
manager.point('P1', 48580.270, 60500.505, 0, False)
manager.point('P2', 48681.390, 55018.279, 0, False)
manager.point('P3', 43767.223, 57968.593, 0, False)
manager.point('P4', 40843.219, 64867.875, 0, False)

manager.distance('P1','B', 5760.706)
manager.distance('P1','A', 5187.342)
manager.distance('P2','A', 7838.880)
manager.distance('P2','P1', 5483.158)
manager.distance('P2','P3', 5731.788)
manager.distance('P2','C', 8720.162)
manager.distance('P3','C', 5598.570)
manager.distance('P3','D', 7494.881)
manager.distance('P3','P4', 7493.323)
manager.distance('P3','P1', 5438.382)
manager.distance('P4','D', 5487.073)
manager.distance('P4','P1', 8884.587)
manager.distance('P4','B', 7228.367)

print(manager.solve(1E-6, 5))

reporter = manager.reporter
print(reporter.get_points())
print(reporter.get_result())
print(reporter.get_dist())
print(reporter.get_sum())

'''
        P1    48580.26848    60500.50027        0.00000        22.9724        25.3206              -
        P2    48681.38205    55018.28889        0.00000        29.0441        30.3875              -
        P3    43767.18867    57968.60834        0.00000        23.4848        29.9399              -
        P4    40843.32101    64867.97990        0.00000        25.9008        33.6817              -
'''