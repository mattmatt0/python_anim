from betterCanvas import *
from random import *
from colorHandler import *
from time import *
from math import *
import fourierReverseEng
def plot(points):
    for point in range(len(points)):
        sX = points[point-1][0] * size + width/2
        sY = points[point-1][1] * size + height/2
        eX = points[point][0]   * size + width/2
        eY = points[point][1]   * size + height/2
        canvas.create_line(sX,sY,eX,eY,fill = "#FFF")
        canvas.create_oval(sX-3,sY-3,sX+3,sY+3,fill="#0F0",outline="#0F0")
    canvas.update()

window = Tk()
window.configure(background="#000")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
size = 1
window.setFullScreen()
canvas = BetterCanvas(window, width = width, height = height, bg = "#000")
canvas.setFrameRate(100)
canvas.pack()
speed = 2*pi/canvas.frameRate/10

angle = 0;
lenght = 1;
z = fourierReverseEng.function
vectors = fourierReverseEng.reverse(z,997)
plot(z)
speeds = vectors[0]
lineCoordsComplex = vectors[1]
canvas.update()
lineCoordsTrigo = [[sqrt(lineCoordsComplex[a][0]**2+lineCoordsComplex[a][1]**2),  acos(lineCoordsComplex[a][0]/sqrt(lineCoordsComplex[a][0]**2+lineCoordsComplex[a][1]**2)),speeds[a]] for a in range(len(lineCoordsComplex)) if lineCoordsComplex[a] != [0,0]]
#print(lineCoordsTrigo)
lines = []
oldX = width/2
oldY = height/2
for line in lineCoordsTrigo:
    x = oldX + line[0]*cos(line[1])*size
    y = oldY + line[0]*sin(line[1])*size
    #lines.append(canvas.draw_line(oldX,oldY,x,y,time=.01,transition="easeOut"))
    lines.append(canvas.create_line(oldX,oldY,x,y,fill='#FFF'))
    oldX = x
    oldY = y
plots = []
cycleFrame = 0
initialCycleDone = False
while True:
    canvas.startFrame()
    oldX = width/2
    oldY = height/2
    oldTipX = x
    oldTipY = y
    for lineID in range(len(lineCoordsTrigo)):
        line = lineCoordsTrigo[lineID]
        line[1] += (speed * line[2])%(pi*2)
        x = oldX + line[0]*cos(line[1])*size
        y = oldY + line[0]*sin(line[1])*size
        canvas.coords(lines[lineID],oldX, height-oldY,x,height- y)
        oldX = x
        oldY = y
    cycleFrame += 1
    cycleFrame = cycleFrame%int(canvas.frameRate*10 - canvas.frameRate/5)
    if initialCycleDone:
        canvas.delete(plots[cycleFrame])
        plots[cycleFrame] = canvas.create_line(oldTipX,height-oldTipY,x,height-y,fill="#0CF")
    else:
        plots.append(canvas.create_line(oldTipX,height-oldTipY,x,height-y,fill="#0CF"))
    if cycleFrame < 1:
        initialCycleDone = True
        
    canvas.update()
    canvas.endFrame()

"""prec = 1
while True:
    canvas.delete('all')
    vectors = fourierReverseEng.reverse(fourierReverseEng.function,prec)
    speeds = vectors[0]
    lineCoordsComplex = vectors[1]
    lineCoordsTrigo = [[sqrt(lineCoordsComplex[a][0]**2+lineCoordsComplex[a][1]**2),  acos(lineCoordsComplex[a][0]/sqrt(lineCoordsComplex[a][0]**2+lineCoordsComplex[a][1]**2)),speeds[a]] for a in range(len(lineCoordsComplex)) if lineCoordsComplex[a] != [0,0]]
    lines = []
    oldX = width/2
    oldY = height/2
    for line in lineCoordsTrigo:
        x = oldX + line[0]*cos(line[1])*size
        y = oldY + line[0]*sin(line[1])*size
        #lines.append(canvas.draw_line(oldX,oldY,x,y,time=.01,transition="easeOut"))
        lines.append(canvas.create_line(oldX,oldY,x,y,fill='#FFF'))
        oldX = x
        oldY = y
    plots = []
    for n in range(999):
        oldX = width/2
        oldY = height/2
        oldTipX = x
        oldTipY = y
        for lineID in range(len(lineCoordsTrigo)):
            line = lineCoordsTrigo[lineID]
            line[1] += (2*pi/999 * line[2])%(pi*2)
            x = oldX + line[0]*cos(line[1])*size
            y = oldY + line[0]*sin(line[1])*size
            oldX = x
            oldY = y
        plots.append(canvas.create_line(oldTipX,oldTipY,x,y,fill="#0CF"))
    prec += 1
    print(prec)
    canvas.update()"""


window.mainloop()
