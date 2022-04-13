# -*- coding: utf-8 -*
import numpy as np
from .measure import *
        
class Reporter:
    def __init__(self, solver):
        self.solver = solver
        self.std = solver.B * solver.Dx * solver.staAfter * solver.B.T

    def get_points(self):
        sb = []
        sb.append(u'点名列表:')
        sb.append('%10s%15s%15s%15s%10s'%('Name', 'X', 'Y', 'Z', 'isKnown'))
        sb.append('-'*68)
        for p in self.solver.points.values():
            sb.append('%10s%15.5f%15.5f%15.5f%10s'%(p.name,p.point[0], p.point[1], p.point[2],p.isknown))
        return '\n'.join(sb)

    def get_result(self):
        sb, solver = [], self.solver
        titles, Dx, staAfter = solver.titles, solver.Dx, solver.staAfter
        sb.append(u'结果及精度:')
        sb.append('%10s%15s%15s%15s%15s%15s%15s'%('Name', 'X', 'Y', 'Z', 'Dx', 'Dy', 'Dz'))
        sb.append('-'*105)
        for p in self.solver.points.values():
            items = [p.name+'-'+i for i in 'XYZ']
            idx = [titles.index(i) if i in titles else -1 for i in items]
            sta = ['%15.4f'%(np.sqrt(Dx[i,i] * staAfter)) if i>-1 else '-' for i in idx]
            sb.append('%10s%15.5f%15.5f%15.5f%15s%15s%15s'%(p.name, p.point[0], p.point[1], p.point[2], sta[0], sta[1], sta[2])) 
        return '\n'.join(sb)

    def get_dist(self):
        sb = []
        sb.append(u'斜距观测:')
        sb.append('%10s%10s%15s%15s%10s'%('From', 'To', 'Mea', 'Reg', 'Dl'))
        sb.append('-'*68)
        for mea in self.solver.meas:
            if not isinstance(mea, Distance): continue
            i = self.solver.meas.index(mea)
            sb.append('%10s%10s%15.4f%15.4f%15.4f'%(mea.p1.name, mea.p2.name, mea.value(), mea.estimate(), np.sqrt(self.std[i,i])*1000))
        return '\n'.join(sb)

    def get_pitch(self):
        sb = []
        sb.append(u'倾斜观测:')
        sb.append('%10s%10s%15s%15s%10s'%('From', 'To', 'Mea', 'Reg', 'Da'))
        sb.append('-'*68)
        for mea in self.solver.meas:
            if not isinstance(mea, Pitch): continue
            i = self.solver.meas.index(mea)
            sb.append('%10s%10s%15.4f%15.4f%15.4f'%(mea.p1.name, mea.p2.name, mea.value(), mea.estimate(), np.sqrt(self.std[i,i])/np.pi * 180 * 3600))
        return '\n'.join(sb)

    def get_dir(self):
        sb = []
        sb.append(u'方位观测:')
        sb.append('%10s%10s%15s%15s%10s'%('From', 'To', 'Mea', 'Reg', 'Da'))
        sb.append('-'*68)
        for mea in self.solver.meas:
            if not isinstance(mea, Direction): continue
            i = self.solver.meas.index(mea)
            sb.append('%10s%10s%15.4f%15.4f%15.4f'%(mea.p1.name, mea.p2.name, mea.value(), mea.estimate(), np.sqrt(self.std[i,i])/np.pi * 180 * 3600))
        return '\n'.join(sb)

    def get_angel(self):
        sb = []
        sb.append(u'角度观测:')
        sb.append('%10s%10s%10s%15s%15s%10s'%('From', 'O', 'To', 'Mea', 'Reg', 'Da'))
        sb.append('-'*72)
        for mea in self.solver.meas:
            if not isinstance(mea, Angle): continue
            i = self.solver.meas.index(mea)
            sb.append('%10s%10s%10s%15.4f%15.4f%15.4f'%(mea.p1.name, mea.p2.name, mea.p3.name, mea.value(), mea.estimate(), np.sqrt(self.std[i,i])/np.pi * 180 * 3600))
        return '\n'.join(sb)

    def get_level(self):
        sb = []
        sb.append(u'水准观测:')
        sb.append('%10s%10s%15s%15s%10s'%('From', 'To', 'Mea', 'Reg', 'Da'))
        sb.append('-'*68)
        for mea in self.solver.meas:
            if not isinstance(mea, Level): continue
            i = self.solver.meas.index(mea)
            sb.append('%10s%10s%15.4f%15.4f%15.4f'%(mea.p1.name, mea.p2.name, mea.value(), mea.estimate(), np.sqrt(self.std[i,i])*1000))
        return '\n'.join(sb)

    def get_sum(self):
        sb, solver = [], self.solver
        sb.append(u'信息汇总:')
        sb.append('-'*38)
        sb.append('\t\t%-15s:%.4f'%('Sta Error', self.solver.staAfter))
        sb.append('\t\t%-15s:%s'%('Free Item', solver.B.shape[1]))
        sb.append('\t\t%-15s:%s'%('Mea Count', solver.B.shape[0]))
        sb.append('\t\t%-15s:%s'%('Inessential:', solver.B.shape[0]-solver.B.shape[1]))
        return  '\n'.join(sb)
