# -*- coding: utf-8 -*
from measure import *
from solver import Solver
from result import Reporter
def dms(a):
    s = a/np.pi*180
    d = int(s)
    m = int((s-d)*60)
    s = np.round(((s-d)*60-m)*60, 2)
    return '%s.%s%s'%(d,m,s)

class Manager:
    def __init__(self, dfSta1=1, dfSta2=1, dfStaA=1):
        self.dfSta1, self.dfSta2 = dfSta1, dfSta2
        self.dfStaA = dfStaA
        self.points, self.measures = {}, []
        self.stations, self.station = {}, None
        self.tshelper = {}
        self.enable3d = True
        self.reporter = None

    def setStaAnd3D(self, sta1, sta2, staa, i3d):
        self.dfSta1, self.dfSta2, self.dfStaA, self.enable3d = sta1, sta2, staa, i3d
        
    def addPoint(self, number, name, x, y, z, dh, isknown):
        p = Point(number, name, (x, y, z), dh, isknown)
        self.points[name] = p

    def getPoints(self):
        x, y = [], []
        for point in sorted(self.points.items()):
            x.append(point[1].point[0])
            y.append(point[1].point[1])
        return (x, y)

    def addLevel(self, a, b, h, s):
        if sum([self.points[i].isknown for i in (a,b)])==2: return
        self.measures.append(Level(self.points[a], self.points[b], h, s, self.dfSta1, self.dfSta2))

    def addDistance(self, a, b, l):
        if sum([self.points[i].isknown for i in (a,b)]) == 2: return
        self.measures.append(
            Distance(self.points[a],self.points[b],l,self.dfSta1,self.dfSta2,self.enable3d))

    def addAngle(self, a,b,c, ang):
        if sum([self.points[i].isknown for i in (a,b,c)]) == 3: return
        self.measures.append(Angle(self.points[a], self.points[b],
                 self.points[c], ang, self.dfStaA))
                 
    def addPitch(self, a, b, ang):
        if sum([self.points[i].isknown for i in (a,b)]) == 2: return
        self.measures.append(Pitch(self.points[a], self.points[b], ang, self.dfStaA)); 

    def startStation(self, name):
        self.station = Station(name)
        
    def endStation(self):
        self.station.setOria()
        for m in self.station.dirs:
            self.measures.append(m)
        self.stations[self.station.name] = self.station
        self.station = None
        
    def addDirection(self, c, o, dire):
        if self.station != None: 
            self.station.addDirect(Direction(self.points[c], self.points[o], dire, self.dfStaA, True))
        else: self.measures.append(Direction(self.points[c], self.points[o], dire, self.dfStaA, False))
        
    def addTS(self, p1, p2, angx, angy, l):
        if not p1 in self.tshelper:
            self.tshelper[p1] = []
        self.tshelper[p1].append((p1, p2, angx, angy, l))
        self.addDistance(p1, p2, l)
        self.addDirection(p1, p2, angx)
        if self.enable3d:
            self.addPitch(p1, p2, angy)

    def addMeasure(self, meas):
        self.measures.extend(meas)
    
    def solve(self, accu=1E-4, maxiter=5):
        self.solver = Solver(self.points, self.measures, self.stations)
        result = self.solver.solve(accu, int(maxiter))
        if result and self.reporter == None:
            self.reporter = Reporter(self.solver)
        return result

    def output(self):
        cont = []
        cont .append('%s,%s,%s'%(self.dfStaA, self.dfSta1, self.dfSta2))
        for i in self.points.values():
            if not i.isknown : continue
            cont.append('%s,%s,%s'%(i.name, i.point[0], i.point[1]))
        for i in self.tshelper:
            cont.append(i)
            for j in self.tshelper[i]:
                cont.append('%s,L,%s'%(j[1], dms(j[2])))
                cont.append('%s,S,%s'%(j[1], j[4]))
        return '\n'.join(cont)
        
if __name__ == '__main__':
    manager = Manager()
    manager.setStaAnd3D(1e-3,1e-6,0.5/60/60/180*np.pi, False)
    manager.addPoint('TN2', 'TN2', 1000, 1000, 0, 0, True)
    manager.addPoint('TN8', 'TN8', 1367.77286, 1117.43005, 0, 0, True)
    manager.addPoint('TN9', 'TN9', 1294.76794, 1789.72043, 0, 0, True)
    manager.addPoint('TN1', 'TN1', 893, 1603, 0, 0, False)
    manager.startStation('TN1')
    manager.addTS('TN1', 'TN2', 0, 0, 612.41862)
    manager.addTS('TN1', 'TN8', (34+18/60+34.46/60/60)/180*np.pi, 0, 678.73168)
    manager.addTS('TN1', 'TN9', (104+56/60+55.39/60/60)/180*np.pi, 0, 442.39598)
    manager.endStation()
    print(manager.output())
    b = manager.solve(1e-3, 3)
    print(b)
    print(manager.solver.B)
    from result import Reporter
    reporter = Reporter(manager.solver)
    print(reporter.get_points())
    print(reporter.get_result())
    #-0.2358, 9.7653
