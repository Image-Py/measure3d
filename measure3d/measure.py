# -*- coding: utf-8 -*
import numpy as np
from numpy.linalg import norm

def angleX(v):
    a = np.arccos(v[0] / norm(v[:2]))
    return a if v[1]>0 else np.pi * 2 - a
    
def transZ(v, a):
    M = np.array([[np.cos(a),-np.sin(a),0],
        [np.sin(a),np.cos(a),0], [0,0,1]])
    return np.dot(M, v).flatten()
    
# 点对象
class Point:
    def __init__(self, number, name, point, dh=0, isknown=False):
        self.point = np.array(point, dtype=np.float)
        self.dh = dh
        self.src = self.point*1
        self.name = name
        self.number = number
        self.isknown = isknown

    def __str__(self):
        return '%s %s %s'%(self.name, self.point, self.isknown)


# 距离观测
class Distance:
    def __init__(self, p1, p2, l, sta1, sta2, is3d):
        self.p1, self.p2, self.l = p1, p2, l
        self.sta1, self.sta2, self.e3 = sta1, sta2, is3d
        self.name = 'dis:%s-%s'%(p1.name, p2.name)

    def limit(self):
        dv = self.p2.point - self.p1.point
        limits = {}
        if(not self.p2.isknown):self.addLimits(limits,self.p2, dv)
        if(not self.p1.isknown):self.addLimits(limits,self.p1, -dv)
        return limits

    def addLimits(self, limits, p, dv):
        limits[p.name+'-'+'X'] = [p.point[0],dv[0]/norm(dv)]
        limits[p.name+'-'+'Y'] = [p.point[1],dv[1]/norm(dv)]
        if self.e3:
            limits[p.name + '-' + 'Z'] = [p.point[2], dv[2] / norm(dv)]
        
    def sta(self): return (self.sta1 + self.l * self.sta2) ** 2
    def value(self): return self.l
    def estimate(self): return norm(self.p1.point - self.p2.point)

class Direction:
    def __init__(self, p1, p2, ang, staa, station):
        print(ang)
        self.p1, self.p2, self.oria = p1, p2, 0
        self.ang, self.staa, self.station = ang, staa, station
        #self.est = angleX(self.p2.point - self.p1.point)
        self.name = 'dir:%s-%s'%(p1.name, p2.name)

    def limit(self):
        limts = {}                
        dv = self.p2.point - self.p1.point;
        self.est = angleX(dv)
        if self.value() - self.est > np.pi: self.est += np.pi * 2;
        if self.est - self.value() > np.pi: self.est -= np.pi * 2;
                
        if not self.p2.isknown: self.addLimts(limts, self.p2, dv)
        if not self.p1.isknown: self.addLimts(limts, self.p1, -dv)
        if self.station: limts[self.p1.name+'-'+'OriA'] = [self.oria,-1]
        return limts

    def addLimts(self, limts, p, dv):
        panel = dv[0:2]
        limts[p.name+'-'+'X'] = [p.point[0], -panel[1]/norm(panel)/norm(panel)]
        limts[p.name+'-'+'Y'] = [p.point[1], panel[0]/norm(panel)/norm(panel)]
        
    def setOri0(self, oria):
        if self.station: self.oria = oria % (np.pi*2)
        if self.oria>np.pi: self.oria-=np.pi*2

    def sta(self):return self.staa**2
    def value(self): 
        print('ang...', self.ang)
        return (self.ang + self.oria)%(np.pi*2)
    def estimate(self): return angleX(self.p2.point - self.p1.point)

class Angle:
    def __init__(self, p1, p2, p3, ang, staA):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.ang, self.staA = ang, staA
        if ang > np.pi: self.ang = np.pi*2 - ang
        self.name = 'ang:%s-%s'%(p1.name, p2.name)

    def limit(self):
        p1, p2, p3, limits = self.p1, self.p2, self.p3, {}
        dv1 = (p1.point - p2.point)[0:2]
        dv2 = (p3.point - p2.point)[0:2]
        est = np.dot(dv1,dv2)/norm(dv1)/norm(dv2)
        self.est = np.arccos(min(1,max(-1,est)))
        
        sign = np.sign(np.cross(dv1,dv2))
        if not p1.isknown: self.addLimits(limits, p1, dv1 * sign)
        if not p2.isknown: self.addLimits(limits, p2, dv1 * -sign)
        if not p3.isknown: self.addLimits(limits, p3, dv2 * -sign)
        if not p2.isknown: self.addLimits(limits, p2, dv2 * sign)
        return limits

    def addLimits(self, limits, p, dv):
        key = p.name + '-' + 'X'
        if not limits.has_key(key): limits[key] = [p.point[0], 0]
        limits[key][1] += dv[1]/np.dot(dv,dv)
        key = p.name + '-' + 'Y'
        if not limits.has_key(key): limits[key] = [p.point[1], 0]
        limits[key][1] -= dv[0]/np.dot(dv,dv)
        
    def sta(self): return self.staA ** 2
    def value(self): return self.ang
    def estimate(self): return self.est
        
class Pitch:
    def __init__(self, p1, p2, ang, staa):
        self.p1, self.p2, self.ang, self.staa = p1, p2, ang, staa
        self.name = 'Pit:%s-%s'%(p1.name, p2.name)
        
    def limit(self):
        limts = {}
        dv = self.p2.point - self.p1.point
        if not self.p2.isknown: self.addLimts(limts, self.p2, dv, 1);
        if not self.p1.isknown: self.addLimts(limts, self.p1, dv, -1);
        return limts;

    def addLimts(self, limts, p, dv, sign):
        dt = np.cross(dv, [-dv[1], dv[0], 0])
        limts[p.name+'-'+'X'] = [p.point[0], dt[0]/norm(dt)/norm(dv)]
        limts[p.name+'-'+'Y'] = [p.point[1], dt[1]/norm(dt)/norm(dv)]
        limts[p.name+'-'+'Z'] = [p.point[2], dt[2]/norm(dt)/norm(dv)]

    def sta(self): return self.staa**2
    def value(self): return self.ang
    def estimate(self):
        dv = self.p2.point - self.p1.point
        return np.arcsin(dv[2]/norm(dv))
    
class Level:
    def __init__(self, p1, p2, h, s, sta1, sta2):
        self.p1, self.p2, self.h = p1, p2, h
        self.sta1, self.sta2, self.s = sta1, sta2, s
        self.name = 'level:%s-%s'%(p1.name, p2.name)

    def limit(self):
        limts = {}
        if not self.p2.isknown:limts[self.p2.name + '-Z'] = [self.p2.point[2], 1]
        if not self.p1.isknown:limts[self.p1.name + '-Z'] = [self.p1.point[2], -1]
        return limts

    def sta(self): return (self.sta1 + self.s * self.sta2)**2
    def value(self):return self.h
    def estimate(self): return self.p2.point[2] - self.p1.point[2]
        
class Station:
    def __init__(self, name):
        self.name = name
        self.dirs = []
    
    def addDirect(self, d):self.dirs.append(d)
    
    def getA0(self):
        v = np.zeros(3)
        for d in self.dirs:
            dv = d.p2.point - d.p1.point
            print(d.value())
            v += transZ(dv,-d.value())/norm(dv)
        return angleX(v)

    def setOria(self, oria=None):
        if oria is None:oria = self.getA0()
        for d in self.dirs: d.setOri0(float(oria))
