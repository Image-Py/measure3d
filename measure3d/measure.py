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
    def __init__(self, name, point, isknown=False):
        if len(point)==2: point = tuple(point)+(0,)
        self.point = np.array(point, dtype=np.float)
        # self.src = self.point*1
        self.name = name
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
        if(not self.p2.isknown):self.count(limits,self.p2, dv)
        if(not self.p1.isknown):self.count(limits,self.p1, -dv)
        return limits

    def count(self, limits, p, dv):
        limits[p.name+'-'+'X'] = [p.point[0],dv[0]/norm(dv)]
        limits[p.name+'-'+'Y'] = [p.point[1],dv[1]/norm(dv)]
        if self.e3:
            limits[p.name + '-' + 'Z'] = [p.point[2], dv[2] / norm(dv)]
        
    def sta(self):
        return self.sta1**2 + (self.estimate()/1000 * self.sta2) ** 2

    def value(self): return self.l * 1000

    def estimate(self): return norm(self.p1.point - self.p2.point) * 1000

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
        #self.est = angleX(dv)
        #if self.value() - self.est > np.pi: self.est += np.pi * 2;
        #if self.est - self.value() > np.pi: self.est -= np.pi * 2;
        
        if not self.p2.isknown: self.count(limts, self.p2, dv)
        if not self.p1.isknown: self.count(limts, self.p1, -dv)
        if self.station: limts[self.p1.name+'-'+'OriA'] = [self.oria,-1]
        return limts

    def count(self, limts, p, dv):
        panel, k = dv[0:2], 180*60*60/1000/np.pi
        limts[p.name+'-'+'X'] = [p.point[0], -panel[1]/norm(panel)**2*k]
        limts[p.name+'-'+'Y'] = [p.point[1],  panel[0]/norm(panel)**2*k]
    
    def setOri0(self, oria):
        if self.station: self.oria = oria % (np.pi*2)
        # if self.oria>np.pi: self.oria-=np.pi*2

    def sta(self):return self.staa**2

    def value(self): 
        r = (self.ang + self.oria)%(np.pi*2)
        return r/np.pi*180*60*60

    def estimate(self): 
        v = (self.ang + self.oria)%(np.pi*2)
        r = angleX(self.p2.point - self.p1.point)
        if r - v > np.pi: r -= np.pi * 2
        if v - r > np.pi: r += np.pi * 2
        return r/np.pi*180*60*60

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
        
        sign = np.sign(np.cross(dv1,dv2))
        if not p1.isknown: self.count(limits, p1, dv1 * sign)
        if not p2.isknown: self.count(limits, p2, dv1 * -sign)
        if not p3.isknown: self.count(limits, p3, dv2 * -sign)
        if not p2.isknown: self.count(limits, p2, dv2 * sign)
        return limits

    def count(self, limits, p, dv):
        k = 180*60*60/1000/np.pi
        key = p.name + '-' + 'X'
        if not key in limits: limits[key] = [p.point[0], 0]
        limits[key][1] += dv[1]/norm(dv)**2*k
        key = p.name + '-' + 'Y'
        if not key in limits: limits[key] = [p.point[1], 0]
        limits[key][1] -= dv[0]/norm(dv)**2*k
        
    def sta(self): return self.staA ** 2

    def value(self): return self.ang/np.pi*180*60*60

    def estimate(self): 
        dv1 = (self.p1.point - self.p2.point)[0:2]
        dv2 = (self.p3.point - self.p2.point)[0:2]
        est = np.dot(dv1,dv2)/norm(dv1)/norm(dv2)
        est = np.arccos(min(1,max(-1,est)))
        return est/np.pi*180*60*60
        
class Pitch:
    def __init__(self, p1, p2, ang, staa):
        self.p1, self.p2, self.ang, self.staa = p1, p2, ang, staa
        self.name = 'Pit:%s-%s'%(p1.name, p2.name)
        
    def limit(self):
        limts = {}
        dv = self.p2.point - self.p1.point
        if not self.p2.isknown: self.count(limts, self.p2, dv, 1);
        if not self.p1.isknown: self.count(limts, self.p1, dv, -1);
        return limts

    def count(self, limts, p, dv, sign):
        dt, k = np.cross(dv, [-dv[1], dv[0], 0]), 180*60*60/1000/np.pi
        limts[p.name+'-'+'X'] = [p.point[0], dt[0]/norm(dt)/norm(dv)*k]
        limts[p.name+'-'+'Y'] = [p.point[1], dt[1]/norm(dt)/norm(dv)*k]
        limts[p.name+'-'+'Z'] = [p.point[2], dt[2]/norm(dt)/norm(dv)*k]

    def sta(self): return self.staa**2

    def value(self): return self.ang/np.pi*180*60*60

    def estimate(self):
        dv = self.p2.point - self.p1.point
        return np.arcsin(dv[2]/norm(dv))/np.pi*180*60*60
    
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
    def value(self):return self.h * 1000
    def estimate(self): return (self.p2.point[2] - self.p1.point[2])*1000

class Station:
    def __init__(self, name):
        self.name = name
        self.dirs = []
    
    def addDirect(self, d):self.dirs.append(d)
    
    def getA0(self):
        v = np.zeros(3)
        for d in self.dirs:
            dv = d.p2.point - d.p1.point
            k = 1/60/60/180*np.pi
            v += transZ(dv,-d.value()*k)/norm(dv)
        return angleX(v)

    def setOria(self, oria=None):
        if oria is None:oria = self.getA0()
        for d in self.dirs: d.setOri0(float(oria))
