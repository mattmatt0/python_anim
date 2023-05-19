from betterCanvas import *
from random import *
from colorHandler import *
from time import *
from math import *
window = Tk()
window.configure(background="#000")
width = 1366
height = 768
rotationSpeed = 5/180
window.setFullScreen()
canvas = BetterCanvas(window, width = width, height = height, background = "#000")
canvas.setFrameRate(100)
canvas.pack()
maxLenght = 1
n = 500
maxSize = height/2
lenght = 1/n
linePoints = [0]
lenghts = [1/(2**x) for x in range(n)]
#lenghts = [1,1,1]
totalLenght = sum(lenghts)
for line in range(n):
    linePoints.append(lenghts[line]/totalLenght * maxLenght + linePoints[len(linePoints) - 1])
linePoints = linePoints[1:]

animLine = canvas.draw_line(width/2 + maxSize *linePoints[0],height/2, width/2 + maxSize * linePoints[len(linePoints) - 1], height/2)
canvas.delete(animLine)
lines = []
circles = []
angles = []
speeds = []
lineSizes = []
for line in range(len(linePoints)):
    lineSizes.append((([0]+linePoints)[line+1] - ([0]+linePoints)[line])*maxSize)
for line in range(len(linePoints) - 1):
    lineOriginX = width/2 + maxSize*linePoints[line]
    lineOriginY = height/2
    circleDiameter = maxSize*lenghts[line]/totalLenght
    circles.append(canvas.create_oval(lineOriginX - circleDiameter, lineOriginY - circleDiameter, lineOriginX + circleDiameter, lineOriginY + circleDiameter, outline="#0F0", state="hidden"))
    lines.append(canvas.create_line(lineOriginX, lineOriginY, width/2 + maxSize*linePoints[line+1], height/2, fill = "#FFF"))
    angles.append(0)
    speeds.append(rotationSpeed*(random()*2 - 1))
#speeds = [-1/180,1/180]
canvas.update()
oldPointX = width/2 + maxSize
oldPointY = height/2
plotLines = []
plotPointer = -500
def toogleCircles(event):
    if canvas.itemcget(circles[0],"state") == "hidden":
        for circle in circles:
            canvas.itemconfig(circle, state='normal')
    else:
        for circle in circles:
            canvas.itemconfig(circle, state='hidden')

def toogleLines(event):
    if canvas.itemcget(lines[0],"state") == "hidden":
        for line in lines:
            canvas.itemconfig(line, state='normal')
    else:
        for line in lines:
            canvas.itemconfig(line, state='hidden')
canvas.bind_all('<c>', toogleCircles)
canvas.bind_all('<l>', toogleLines)
speedFactor = 1
while True:
    start = time()
    sigmaAngle = 0
    for line in range(len(lines)):
        if line==0:
            oldX = width/2
            oldY = height/2
        else:
            oldCoords = canvas.coords(lines[line-1])
            oldX = oldCoords[2]
            oldY = oldCoords[3]
            oldAngle = angles[line-1]
        angle = angles[line]
        angle += speeds[line] * (1-speedFactor) 
        angles[line] = angle
        circleDiameter = maxSize*lenghts[line]/totalLenght
        canvas.coords(lines[line], oldX,oldY, oldX + cos(angle)*lineSizes[line], oldY + sin(angle)*lineSizes[line])
        canvas.coords(circles[line], oldX - circleDiameter, oldY - circleDiameter, oldX + circleDiameter, oldY + circleDiameter)
    pointX = canvas.coords(lines[len(lines)-1])[2]
    pointY = canvas.coords(lines[len(lines)-1])[3]
    plotLines.append(canvas.create_line(oldPointX, oldPointY, pointX, pointY, fill = "#0CF"))
    if plotPointer >= 0:
        canvas.delete(plotLines[plotPointer])
    plotPointer += 1
    oldPointX = pointX
    oldPointY = pointY
    canvas.update()
    speedFactor /= 1.001
    while time() - start < .01:
        pass

window.mainloop()
