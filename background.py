from betterCanvas import *
from random import *
from colorHandler import *
from time import *
window = Tk()
window.attributes('-fullscreen', True)
window.configure(background="#000")
width = 1366
height = 768
canvas = BetterCanvas(window, width = width, height = height, background = "#000")
canvas.setFrameRate(100)
canvas.pack()
#canvas.wait(10);
messageBienvenue = canvas.create_text(width/2,height/2,text="Bienvenue", fill = "#000", font=("Georgia",90),anchor = "center")
messageLive = canvas.create_text(width/2,height/2 + 90,text="Le live va bientôt commencer", fill = "#000", font=("Georgia",30))

for message in (messageBienvenue,messageLive):
    opacity = 0
    while opacity < 255:
        color = (int(opacity) for a in range(3))
        canvas.itemconfigure(message, fill = toHex(*color))
        opacity += (256 - opacity)/100
        canvas.update()
        sleep(.01)
fontSize = 90
while fontSize>40:
    fontSize -= 1
    canvas.itemconfigure(messageBienvenue, font=("Georgia",fontSize))
    canvas.update()
    sleep(.01)
while fontSize > 30:
    fontSize /= 1.01
    canvas.itemconfigure(messageBienvenue, font=("Georgia",int(fontSize)))
    canvas.update()
    sleep(.01)

fontSize = 30
while fontSize>15:
    fontSize -= 1
    canvas.itemconfigure(messageLive, font=("Georgia",fontSize))
    canvas.update()
    sleep(.01)
while fontSize > 10:
    fontSize /= 1.01
    canvas.itemconfigure(messageLive, font=("Georgia",int(fontSize)))
    canvas.update()
    sleep(.01)

posX = width/2
posY = height/2 + 90
targetX = 3*width/4
targetY = height/2 + 30
while int(posX) + 1 < targetX:
    posX += (targetX - posX)/10
    posY = (targetY - height/2 - 90)*(1-(targetX-posX)/(targetX - width/2)) + height/2 + 90
    for message in (messageBienvenue,messageLive):
        canvas.move(message,posX - canvas.coords(message)[0], 0)
    canvas.move(messageLive,0,posY - canvas.coords(messageLive)[1])
    canvas.update()
    sleep(.01)

centerX = int(width/3)
centerY = int(height/2)
print(centerX)
triangleHeight = int(height * 9 /10)
triangleSide = int(2 * triangleHeight / (3.0**.5 ))
trianglePoints = [centerX,centerY - triangleHeight / 2, centerX - triangleSide/2, centerY + triangleHeight/2, centerX + triangleSide/2, centerY + triangleHeight/2]
canvas.draw_line(*trianglePoints[0:4], fill="#FFF", transition="easeOut",time=1)
canvas.draw_line(*trianglePoints[2:6], fill="#FFF", transition="easeOut",time=1)
canvas.draw_line(*(trianglePoints[4:6] + trianglePoints[0:2]), fill="#FFF", transition="easeOut",time=1)

line = canvas.create_line(0,0,1,1)
a = canvas.create_line(0,0,1,1)
movingPoint = canvas.create_line(0,0,1,1)
counter = 0;
a1 = random()
a2 = random()
if a1 + a2 > 1:
    a1 = 1 - a1
    a2 = 1 - a2
pointX = trianglePoints[0] + a1 * (trianglePoints[2]-trianglePoints[0])\
      +                  a2 * (trianglePoints[4]- trianglePoints[0])

pointY = trianglePoints[1] + a1 * (trianglePoints[3]-trianglePoints[1])\
    + a2 * (trianglePoints[5]- trianglePoints[1])
for x in range(10):
    canvas.delete(a)
    a = canvas.create_oval(pointX-x//2,pointY-x//2,pointX+x//2+1,pointY+x//2+1,outline='#3CF',fill = "#3CF")
    canvas.update()
    sleep(.1)
events = set()
canvas.update()
def eventAdd(event):
    events.add(event.keysym)
def eventRemove(event):
    events.remove(event.keysym)
canvas.bind_all('<KeyPress>', eventAdd)
canvas.bind_all('<KeyRelease>', eventRemove)
while True:
    trianglePoint = randint(0,2)
    trianglePointX = trianglePoints[trianglePoint * 2]
    trianglePointY = trianglePoints[trianglePoint * 2 + 1]
    lineX = pointX
    lineY = pointY
    while abs(int(lineX) - int(trianglePointX)) > 3 and abs(int(lineY) - int(trianglePointY)) > 3:
        line = canvas.create_line(pointX, pointY, lineX, lineY, fill="#CCF")
        canvas.update()
        lineX -= (lineX - trianglePointX)/20
        lineY -= (lineY - trianglePointY)/20
        canvas.delete(line);
        sleep(.01)
    line = canvas.create_line(pointX, pointY, trianglePointX, trianglePointY, fill = "#CCF")
    movingPointX = pointX
    movingPointY = pointY
    pointX = (pointX + trianglePointX)/2
    pointY = (pointY + trianglePointY)/2
    while int(movingPointX) != int(pointX):
        canvas.delete(movingPoint)
        movingPointX -= (movingPointX - pointX)/20
        movingPointY -= (movingPointY - pointY)/20
        movingPoint = canvas.create_oval(movingPointX-5,movingPointY-5,movingPointX+5,movingPointY+5, outline="#0F0",fill = "#0F0")
        canvas.update()
        sleep(.01)
    canvas.delete(movingPoint)
    canvas.delete(line)
    plot = canvas.create_oval(pointX-5,pointY-5,pointX+5,pointY+5,outline="#0F0",fill="#0F0")
    color = [0,255,0]
    while abs(color[0] - 51) > 10:
        color[0] -= int((color[0] - 51)/10)
        color[1] -= int((color[1] - 204)/10)
        color[2] -= int((color[2] - 255)/10)
        plotColor = toHex(*color)
        canvas.itemconfig(plot, fill = plotColor, outline = plotColor)
        sleep(.05)
        canvas.update()
    counter += 1;
    sleep(.5)
    canvas.delete(line)
    if 'f' in events:
        break;
while True:
    trianglePoint = randint(0,2)
    trianglePointX = trianglePoints[trianglePoint * 2]
    trianglePointY = trianglePoints[trianglePoint * 2 + 1]
    pointX = (pointX + trianglePointX)/2
    pointY = (pointY + trianglePointY)/2
    plot = canvas.create_oval(pointX-5,pointY-5,pointX+5,pointY+5,outline="#3CF",fill="#3CF")
    canvas.update()
window.mainloop()
