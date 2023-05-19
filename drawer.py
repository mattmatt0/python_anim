from betterCanvas import *
from random import *
from colorHandler import *
from time import *
from math import *
file2write = input('fichier à écrire:')
file2write = open(file2write,'w')
window = Tk()
window.configure(background="#000")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
size = 1
window.setFullScreen()
canvas = BetterCanvas(window, width = width, height = height, bg = "#000")
canvas.setFrameRate(100)
canvas.pack()
pointMatrix = []
def addPoints(event):
    if len(pointMatrix):
        canvas.create_line(pointMatrix[-1][0],pointMatrix[-1][1],event.x,event.y,fill="#fff")
    pointMatrix.append([event.x,event.y])
    canvas.update()
def stopDraw(event):
    print(pointMatrix)
    file2write.write(str(pointMatrix))
    file2write.close()
    window.destroy()
window.bind_all('<B1-Motion>',addPoints)
window.bind_all('<s>',stopDraw)
window.mainloop()
