from betterCanvas import*
from random import*
from colorHandler import*
from time import*
from math import*
from listLoader import *
window=Tk()
window.configure(background="#000")
width=window.winfo_screenwidth()
height=window.winfo_screenheight()
size=1
window.setFullScreen()
canvas=BetterCanvas(window,width=width,height=height,bg="#000")
canvas.setFrameRate(100)
canvas.pack()
canvas.draw_pointSet(readFile('virus'), time=1,color="#FFF",precision=10)
window.mainloop()
