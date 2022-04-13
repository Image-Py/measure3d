# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 21:54:05 2015

@author: Administrator
"""
import sys
sys.path.append('../')

from measure3d import Manager

manager = Manager(0,1,0)

manager.point('A', 0, 0, 1, True)
manager.point('B', 0, 0, 0, False)
manager.point('C', 0, 0, 0, False)

manager.level('A', 'B', 1, 1)
manager.level('A', 'C', 2, 1)
manager.level('B', 'C', 1, 1)

print(manager.solve(1e-1, 5))
print(manager.reporter.get_result())
print(manager.reporter.get_points())
