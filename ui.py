
# -*- coding: utf-8 -*-  
import Tkinter
from Tkinter import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append('.')
converter=__import__("converter")

top = Tkinter.Tk()
top.geometry('320 X 480')

# Code to add widgets will go here...
start = Tkinter.Button(top,text=u'start',command=converter.convert_main)
start.pack()



top.mainloop()

