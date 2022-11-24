#!/usr/bin/env python3
from tkinter import Tk, Button
import sys
str().center
def _quit():
    root.quit()
root = Tk()
root.geometry('100x20+20+20')
c = Button(root, text="点我退出循环", command=_quit)
c.pack()
root.mainloop()
