# -*- coding: utf-8 -*
import numpy as np

class Solver:
    def __init__(self, points, meas, stations={}):
        self.meas = meas
        self.points = points
        self.stations = stations

    def build(self):
        index,x0,meas = [],[],self.meas
        for m in meas:
            limits = m.limit()
            for k,v in sorted(limits.items()):
                if not k in index:
                    index.append(k)
                    x0.append(v[0])
        
        B = np.zeros((len(meas),len(index)))
        l,l0 = np.zeros((2,len(meas),1))
        P = np.zeros(len(meas))
        
        for i in range(len(meas)):
            P[i] = meas[i].sta()
            l[i] = meas[i].value()
            l0[i] = meas[i].estimate()
            for k,v in sorted(meas[i].limit().items()):
                B[i,index.index(k)] = v[1]

        self.titles = index
        # 系数矩阵， 观测向量， 近似观测向量， 概算值，协方差矩阵
        self.B,self.L,self.L0 = np.mat(B),np.mat(l),np.mat(l0)
        self.X0,self.P = np.mat(x0).T, np.mat(np.diag(P))

    def update(self):
        for n in range(len(self.titles)):
            p,i = self.titles[n].split('-')
            if i in 'XYZ':
                # print self.points[p].point
                self.points[p].point['XYZ'.index(i)] = self._X_[n]
            if i == 'OriA':
                self.stations[p].setOria(self._X_[n])
        #for i in range(len(self.titles)):
        #    self.adjusts[self.titles[i]].adjust(self._X_[i])

    def step(self):
        self.build()
        B,P,L,L0, = self.B, self.P, self.L, self.L0
        self.Dx = (B.T @ P.I @ B).I
        self.x = self.Dx @ -B.T @ P.I @ (L0-L)
        self.e = -B * self.x + L - L0
        self._L_ = -B * self.x + L0

        k = [(1000, 1/np.pi*180*60*60)['OriA' in i] for i in self.titles]
        self._X_ = self.X0 + self.x / np.array(k)[:,None]
        # print(self._X_)
        self.staAfter = self.e.T * P.I * self.e
        
        if B.shape[0] == B.shape[1]:self.staAfter=1
        else: self.staAfter = float(self.staAfter/(B.shape[0]-B.shape[1]))
        self.var = np.sqrt(self.Dx[np.eye(len(self.x))>0] * self.staAfter)
        self.update()
        
    def solve(self, accu, maxiter):
        for i in range(maxiter):
            self.step()
            if np.abs(self.x).max()<accu:
                return True
        return False
                       
