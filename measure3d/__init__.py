from .manager import Manager
from .solver import Solver
from .result import Reporter

class Maroc:
    def __init__(self):
        self.measure()
        
    def out(self, cont):
        print(cont)
        
    def measure(self):
        manager = self.manager = Manager()
        self.dic = {
            'mea':self.measure, 'point':manager.point,
            'lev':manager.level, 'dis':manager.distance,
            'ang':manager.angle, 'pit':manager.pitch,
            'sta':manager.start, 'ends':manager.end,
            'dir':manager.direction, 'ts':manager.ts,
            'set':manager.config, 'solve':manager.solve,
            'rp_pts': lambda : manager.reporter.get_points(),
            'rp_rst': lambda : manager.reporter.get_result(),
            'rp_dis': lambda : manager.reporter.get_dist(),
            'rp_pit': lambda : manager.reporter.get_pitch(),
            'rp_dir': lambda : manager.reporter.get_dir(),
            'rp_ang': lambda : manager.reporter.get_angel(),
            'rp_lev': lambda : manager.reporter.get_level(),
            'rp_sum': lambda : manager.reporter.get_sum(),
            'titles':lambda : manager.solver.titles,
            'result':lambda : manager.solver._X_,
            'std':lambda : manager.solver.staAfter,
            'cov':lambda : manager.solver.Dx,
            'var':lambda : manager.solver.var,
            'newline' : lambda:'','>':lambda x:x, '':lambda : ''}
                    
        self.rdic = {
            'mea':('----- new task -----', 0),
            'point':('addpoint:%s', 1),'lev':('add level:%s,%s',2),
            'set':('set std1:%s std2:%s stda:%s 3d:%s',4),
            'sta':('start new station:%s',1),'ts':('add TS:%s,%s',2),
            'dis':('add distance:%s,%s',2),'ang':('add angle:%s,%s,%s',3),
            'ends':('end the station',0),'dir':('add direction:%s,%s',2),
            'pit':('add pitch:%s,%s',2),
            'solve':('solve with accr:%s maxiter:%s',2)}

    def parse(self, p):
        if p=='y': return True
        if p=='n': return False
        try: return float(p)
        except: return p
        
    def parses(self, ps): 
        return [self.parse(i) for i in ps.split(',') if i != '']
        
    def result(self, cmd, para):
        fmt, n = self.rdic[cmd]
        return fmt%tuple(para[:n])
    
    def run(self, cmd):
        if cmd.startswith('>'): cmd = '>:'+cmd[1:]
        else: cmd = cmd.replace(' ','')
        if len(cmd)>0 and cmd[0]=='#': return True
        i = cmd.index(':') if ':' in cmd else len(cmd)
        #try:
        cmd, para = cmd[:i], self.parses(cmd[i+1:])
        if cmd in self.rdic:self.out(self.result(cmd, para))
        if not cmd in self.dic:self.out('unknown command %s'%cmd)
        rst = self.dic[cmd](*para)
        if rst!= None: self.out(rst)
        return True
        # except:
        #     self.out('command error!')
        #     return False
    
    def runs(self, cmds):
        for i in cmds:
            if not self.run(i) : break

def show():
	from .editor import NotePad
	NotePad()