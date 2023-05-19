from betterCanvas import *
import tkinter
from random import *
from math import *
window = Tk()
window.setFullScreen()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
canvas = BetterCanvas(window, width = width, height = height, bg = "#000", highlightthickness = 0)
canvas.setFrameRate(100)
canvas.pack()

keysPressed = set()
def keyPressed(event):
    keysPressed.add(event.keysym)

def keyReleased(event):
    keysPressed.discard(event.keysym)

canvas.bind_all('<KeyPress>',keyPressed)
canvas.bind_all('<KeyRelease>',keyReleased)

def waitUntilSpacePress():
    while 'space' in keysPressed:
        canvas.update()
    while not 'space' in keysPressed:
        canvas.update()

waitUntilSpacePress()

axisX = canvas.draw_arrow(width/50,height - width/50,width/50,width/50,time=.5)
axisY = canvas.draw_arrow(width/50,height - width/50,width-width/50,height-width/50,time=.5)
points = [canvas.spawn_circle(randint(width//50,width-width//50),randint(width//50,height-width//50), width/500, fill = "#3A9", outline = "#3A9", time=.01) for n in range(100)]

waitUntilSpacePress()
pointCoords = [] 
for point in points:
    canvas.startFrame()
    pointX = randint(width//50,width-width//50)
    pointY = (height-width/50) - (pointX * (height-width/25)/(width-width/25)) + (random()-.5) * height/10
    pointCoords.append((pointX-width/2,pointY-height/2))
    canvas.coords(point,pointX - width/500, pointY - width/500, pointX + width/500, pointY + width/500) 
    canvas.endFrame()

waitUntilSpacePress()

for frame in range(100):
    canvas.startFrame()
    fact = (49-frame)/50
    for point in range(len(points)):
        pointX = width/2 + pointCoords[point][0]
        pointY = height/2 + pointCoords[point][1]*fact
        canvas.coords(points[point], pointX - width/500, pointY - width/500, pointX + width/500, pointY + width/500)
    canvas.endFrame()


waitUntilSpacePress()

[canvas.delete(obj) for obj in [*points, *axisX, *axisY]]
covariance = canvas.draw_text(width/2,height/2 - width/25,text="cov(X,Y)",size=int(width/25),method='fade',color="#FFF",transition='linear',anchor='c',time=.5)
frac = canvas.draw_line(width/2 +  5*width/25,height/2,width/2 - 5*width/25,height/2,time=.5)
ecartType = canvas.draw_text(width/2,height/2 + width/25,text="σ(X)×σ(Y)",size=int(width/25),method='fade',color="#FFF",transition='linear',anchor='c',time=.5)


waitUntilSpacePress()

[canvas.itemconfig(obj, state="hidden") for obj in (covariance, frac, ecartType)]
a = tkinter.PhotoImage(file="covariance.gif")
formuleCovariance = canvas.create_image(width/2,height/2,image=a)

waitUntilSpacePress()

canvas.move_objects([formuleCovariance], 0, height/2-133, mode = "relative", transition="easeInOut")

graphLenght = width/3
originX = width/3
originY = 53*width/150
axisX = canvas.draw_arrow(originX,originY,originX+graphLenght,originY,time = .5)
axisY = canvas.draw_arrow(originX,originY,originX,originY-graphLenght, time = .5)

points = [canvas.spawn_circle(
    randint(int(originX), int(originX + graphLenght)),
    randint(int(originY - graphLenght), int(originY)),
    1,outline = "#FFF",time=.01) for point in range(30)]
coords = [(
    (canvas.coords(point)[0] + canvas.coords(point)[2])/2,
    (canvas.coords(point)[1] + canvas.coords(point)[3])/2,
    
    ) for point in points]
averageX = sum([coord[0] for coord in coords])/len(coords)
averageY = sum([coord[1] for coord in coords])/len(coords)
average = canvas.spawn_circle(averageX, averageY, 5, fill = "#FF0", outline = "#FF0")

waitUntilSpacePress()

a = tkinter.PhotoImage(file="covariance1.gif")
canvas.itemconfig(formuleCovariance, image=a)
box0 = canvas.draw_lines([[averageX, coords[0][1], coords[0][0], coords[0][1]],
    [averageX, averageY, coords[0][0], averageY]], fill = "#0FC", time = .5)
sleep(.1)

a = tkinter.PhotoImage(file="covariance2.gif")
canvas.itemconfig(formuleCovariance, image=a)
box1 = canvas.draw_lines([[coords[0][0], averageY, coords[0][0], coords[0][1]],
    [averageX, averageY, averageX, coords[0][1]]],fill = "#FC0", time = .5)

waitUntilSpacePress()

a = tkinter.PhotoImage(file="covariance3.gif")
canvas.itemconfig(formuleCovariance, image=a)
area = canvas.create_rectangle(averageX,averageY,coords[0][0],coords[0][1],fill="#000")
canvas.fade(area,"#0F0")

waitUntilSpacePress()
canvas.delete(area)

separateurX = canvas.draw_line(originX, averageY, originX + graphLenght, averageY)
separateurY = canvas.draw_line(averageX, originY, averageX, originY - graphLenght)

waitUntilSpacePress()

a = tkinter.PhotoImage(file="covariance.gif")
canvas.itemconfig(formuleCovariance, image=a)
zoneRouge = canvas.create_rectangle(originX,originY, originX + graphLenght, originY - graphLenght, fill = "#F00")
zoneVerte1 = canvas.create_rectangle(averageX,averageY, originX, originY, fill = "#0F0")
zoneVerte2 = canvas.create_rectangle(averageX,averageY, originX+graphLenght, originY-graphLenght, fill = "#0F0")

waitUntilSpacePress()

[canvas.delete(obj) for obj in [formuleCovariance,zoneRouge, zoneVerte1, zoneVerte2,separateurX,separateurY,*box0, *box1]]
[canvas.itemconfig(obj, state="hidden") for obj in [average, *points, *axisX, *axisY]]

a = tkinter.PhotoImage(file="ecartType.gif")
formuleEcartType = canvas.create_image(width/2,height/2, image=a)

waitUntilSpacePress()

a = tkinter.PhotoImage(file="ecartType2.gif")
canvas.itemconfig(formuleEcartType, image=a)

waitUntilSpacePress()

a = tkinter.PhotoImage(file="ecartType3.gif")
canvas.itemconfig(formuleEcartType, image=a)


waitUntilSpacePress()

a = tkinter.PhotoImage(file="ecartType4.gif")
canvas.itemconfig(formuleEcartType, image=a)

waitUntilSpacePress()

canvas.move_objects([formuleEcartType], 0, height/2-133, mode = "relative", transition="easeInOut")
side1 = canvas.draw_line(width/2-width/20,height/2, width/2+width/20,height/2, transition="easeOut", time=.5)
side2 = canvas.draw_line(width/2+width/20,height/2, width/2+width/20,height/2-width/20, transition="easeOut", time=.5)
hypothenuse = canvas.draw_line(width/2+width/20,height/2-width/20, width/2-width/20,height/2, transition="easeOut", time=.5)
hypoCoords = canvas.coords(hypothenuse)
lenght = sqrt((hypoCoords[0]-hypoCoords[2])**2 + (hypoCoords[1]-hypoCoords[3])**2)
canvas.fade(side1, "#000",time=.5)
canvas.fade(side2, "#000",time=.5)


angle = acos(abs(hypoCoords[0]-hypoCoords[2])/lenght)
startX = width/2 - lenght/2
for x in range(100):
    canvas.startFrame()
    canvas.coords(hypothenuse, startX, height/2, startX + lenght*cos(angle), height/2 + width/20*sin(angle))
    angle *= 0.5
    canvas.endFrame()
canvas.coords(side2, startX + lenght*cos(angle), height/2, startX + lenght* cos(angle), height/2-width/20)
canvas.itemconfig(side2, fill="#FFF")
canvas.delete(side1)
side1 = canvas.draw_line(startX, height/2, startX + lenght* cos(angle), height/2-width/20)

waitUntilSpacePress()

canvas.delete(side1)
canvas.delete(side2)
canvas.delete(hypothenuse)
canvas.spawn_circle(width/2,height/4, 3, fill="#FFF")
rotate = canvas.spawn_circle(width/2,height/2, 3, fill="#FFF")
areaRectangle = canvas.create_rectangle(width/2,height/4,width/2,height/2, fill="#FFF",outline="#FFF")
areaL = canvas.create_line(width/2,height/4,width/2,height/2, fill="#FFF")
angle = pi/2
while True:
    canvas.startFrame()
    canvas.coords(rotate, width/2+cos(angle)*height/4 + 3,height/4+sin(angle)*height/4-3, width/2+cos(angle)*height/4 - 3,height/4+sin(angle)*height/4-3)
    canvas.coords(areaRectangle, width/2,height/4, width/2+cos(angle)*height/4,height/4+sin(angle)*height/4)
    canvas.coords(areaL, width/2,height/4, width/2+cos(angle)*height/4,height/4+sin(angle)*height/4)
    angle += 0.01
    areaCoords = canvas.coords(areaRectangle)
    area = (areaCoords[0]-areaCoords[2])*(areaCoords[1]-areaCoords[3])
    if area > 0:
        canvas.itemconfig(areaRectangle,fill="#0F0",outline= "#0F0")
    if area < 0:
        canvas.itemconfig(areaRectangle,fill="#F00",outline= "#F00")
    canvas.endFrame()
window.mainloop()
