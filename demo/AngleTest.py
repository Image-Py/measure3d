# ','*',' coding: utf','8 ','*
import sys
sys.path.append('../')
from measure3d import Manager

manager = Manager(3e-1, 1e-3, 1)

manager.point('A', 9684.28, 43836.82, 0, True)
manager.point('B', 10649.55, 31996.50, 0, True)
manager.point('C', 19063.66, 37818.86, 0, True)
manager.point('D', 17814.63, 49923.19, 0, True)
manager.point('P1', 13188.61, 37334.97, 0, False)
manager.point('P2', 15578.61, 44391.03, 0, False)

manager.angle('A','P1','B', 2.203304133)
manager.angle('P1','A','B', 0.412997746)
manager.angle('P1','B','A', 0.525279625)
manager.angle('A','P2','D', 2.048661173)
manager.angle('P2','A','D', 0.548857568)
manager.angle('P2','D','A',0.544070518)
manager.angle('P2','C','D', 0.384762682)
manager.angle('C','P2','D', 2.269869536)
manager.angle('P2','D','C', 0.486943468)
manager.angle('P1','P2','A', 1.150466744)
manager.angle('P1','A','P2', 1.170191873)
manager.angle('P2','P1','A', 0.820941794)
manager.angle('C','P2','P1', 0.814178643)
manager.angle('C','P1','P2', 1.162072698)
manager.angle('P1','C','P2', 1.165337919)
manager.angle('P1','C','B', 0.523189108)
manager.angle('C','P1','B', 2.096872985)
manager.angle('C','B','P1', 0.521540257)

print(manager.solve(1E-1, 3))
print(manager.reporter.get_result())
print(manager.reporter.get_points())
print(manager.reporter.get_sum())
