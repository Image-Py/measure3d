# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:15:03 2015

@author: Administrator
"""

import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
from . import Maroc

class NotePad:
    def __init__(self, rble = True):
        self.maroc = Maroc()
        self.root = root = tk.Tk(className="Measure3d")
        self.txt_code = txt_code = tkscrolledtext.ScrolledText(root, width=60, height=50)
        self.txt_result = txt_result = tk.scrolledtext.ScrolledText(root)
        self.txt_code.insert('1.0','# welcom to measure3d\n')
        menu = tk.Menu(root)
        root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        #filemenu.add_command(label="New", command=main)
        if rble : filemenu.add_command(label="Open...", command=self.open_command)
        filemenu.add_command(label="Save", command=self.saving)
        filemenu.add_command(label='Export', command=self.save_rst_command)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_command)
        helpmenu = tk.Menu(menu)
        runmenu = tk.Menu(menu)
        if rble : menu.add_cascade(label='Run', menu=runmenu)
        runmenu.add_command(label='solve', command=self.run_command)
        runmenu.add_command(label='plot', command=self.plot_command)
        runmenu.add_separator()
        runmenu.add_command(label='clear codes', 
            command=lambda:self.txt_code.delete('1.0',tk.END))
        runmenu.add_command(label='clear result', 
            command=lambda:self.txt_result.delete('1.0',tk.END))
        menu.add_cascade(label="Help", menu=helpmenu)
        files = ['level_demo','distance_demo','angle_demo','ts_demo','-',
                 'add_point','add_distance','add_station','new_measure']
        cmds = {'distance_demo': lambda:self.demo_command('./data/distance_demo.txt', True),
                'ts_demo': lambda:self.demo_command('./data/ts_demo.txt',True),
                'angle_demo':lambda:self.demo_command('./data/angle_demo.txt',True),
                'level_demo':lambda:self.demo_command('./data/level_demo.txt',True),
                'add_point':lambda:self.demo_command('./data/add_point.txt',False),
                'add_distance':lambda:self.demo_command('./data/add_distance.txt',False), 
                'add_station':lambda:self.demo_command('./data/add_station.txt',False),               
                'new_measure':lambda:self.demo_command('./data/new_measure.txt',False)}

        for i in files:
            if i=='-':helpmenu.add_separator()
            else:helpmenu.add_command(label=i, command = cmds[i])
        helpmenu.add_separator()
        helpmenu.add_command(label="About...", command=self.about_command)
        txt_code.pack(side=tk.LEFT,fill='y')
        txt_result.pack(expand='yes',fill='both')
        self.maroc.out = self.out
        root.mainloop()
        
    def demo_command(self, name, clear = False):
        file = open(name)
        cont = file.read()
        file.close()
        if clear:self.txt_code.delete('1.0', tk.END)
        self.txt_code.insert(tk.INSERT, cont)
        
        #self.txt_code.setvar
    def out(self, cont):
        self.txt_result.insert(tk.END, str(cont)+'\n')
        
    def run_command(self):
        data = self.txt_code.get('1.0', tk.END+'-1c')
        self.maroc.runs(data.splitlines())
        
    def plot_command(self):
        self.maroc.manager.plot()
        
    def save_rst_command(self):
        self.save_command(self.txt_result.get('1.0', tk.END+'-1c'))
        
    def open_command(self):
        file = tkfiledialog.askopenfile(parent=self.root,mode='rb',title='Select a file')
        if file != None:
            contents = file.read()
            self.txt_code.insert('1.0',contents)
            file.close()

    def saving(self):
        self.save_command(self.txt_code.get('1.0', tk.END+'-1c'))
        
    def save_command(self, data):
        file = tkfiledialog.asksaveasfile(mode='w')
        if file != None:
        # slice off the last character from get, as an extra return is added
            file.write(data)
            file.close()
         
    def exit_command(self):
        if tkmessagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()
 
    def about_command(self):
        #NotePad(rble=False)
        label=tkmessagebox.showinfo('About', 'Measure3D by yan xiaolong')

if __name__ == '__main__':
    NotePad()
