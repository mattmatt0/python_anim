from betterCanvas import *
window = Tk()
window.attributes('-fullscreen', True)
width = 1366
height = 768
canvas = BetterCanvas(window, width = width, height = height, background = "#000")
canvas.setFrameRate(100)
canvas.pack()
canvas.draw_line(0,height/2,width,height/2)
gradAmount = 34
dotDistance = width/gradAmount
axisGrads = [[a*dotDistance,height/2 - 10, a*dotDistance, height/2 + 10] for a in  range(gradAmount + 1)]
axisGrads[int(len(axisGrads)/2)].append("#0CF")
canvas.draw_lines(axisGrads, time=.5, delay=1, transition="easeOut")
"""for a in range(0,gradAmount + 1):
    if a != gradAmount / 2:
        canvas.draw_line(a*dotDistance, height/2 - 10, a*dotDistance, height/2 + 10, time=.03)
    else:
        canvas.draw_line(a*dotDistance, height/2 - 10, a*dotDistance, height/2 + 10, time=.03, fill = "#0CF")
"""
for a in range(0,gradAmount + 1):
    canvas.create_text(a*dotDistance, height/2 + 20,  text = str(int(a - gradAmount/2)), fill = "#FFF",font = ("Georgia",15))
    sleep(.01)
    canvas.update()

axis2 = canvas.draw_line(0,height/2 + 100,width,height/2 + 100)
axisGrads = []
axisMarks = []
for a in range(0,gradAmount*4):
    if a != gradAmount*2:
        axisGrads.append(canvas.draw_line((a-3*gradAmount/2)*dotDistance, height/2 + 90, (a-3*gradAmount/2)*dotDistance, height/2 + 110, time=.03))
    else:
        axisGrads.append(canvas.draw_line((a-3*gradAmount/2)*dotDistance, height/2 + 90, (a-3*gradAmount/2)*dotDistance, height/2 + 110, time=.03, fill = "#0CF"))
    axisMarks.append(canvas.create_text((a-3 * gradAmount/2)*dotDistance, height/2 + 130, text = str(int(a - gradAmount*2)), font=("Georgia", 15), fill = "#FFF"))

arrow0 = canvas.draw_line(width/2,height/2, width/2 + dotDistance, height/2, fill="#F00")
arrow1 = canvas.draw_line(width/2 + dotDistance,height/2 , width/2 + dotDistance - 10, height/2 - 10, fill="#F00", time = .2)
arrow2 = canvas.draw_line(width/2 + dotDistance,height/2 , width/2 + dotDistance - 10, height/2 + 10, fill="#F00", time = .2)
lockY= [True]
def toogleY(event):
    lockY[0] = not lockY[0]

eventCoords = [0,0]
def moveAxis(event):
    if lockY[0]:
        event.y = height/2
    axisEquationX = event.x-width/2
    axisEquationY = event.y - height/2
    distance = (axisEquationX*axisEquationX + axisEquationY*axisEquationY)**.5
    if distance != 0:
        offset = width/distance
    canvas.coords(axis2, width /2 - offset * axisEquationX, height/2 - offset * axisEquationY + 100, width/2 + offset * axisEquationX, height/2 + offset * axisEquationY + 100)
    canvas.coords(arrow0, width/2,height/2, event.x, event.y)
    canvas.coords(arrow1, event.x, event.y , (event.x - axisEquationX/distance * 10)- axisEquationY/distance * 10, (event.y-axisEquationY/distance*10)+ axisEquationX/distance *  10)
    canvas.coords(arrow2, event.x, event.y , (event.x - axisEquationX/distance * 10)+ axisEquationY/distance * 10, (event.y-axisEquationY/distance*10)- axisEquationX/distance *  10)
    for grad in range(len(axisGrads)):
        originX = width/2 + axisEquationX * (grad - len(axisGrads)/2)
        originY = height/2 +100 + axisEquationY * (grad -len(axisGrads)/2)
        canvas.coords(axisGrads[grad],originX + axisEquationY/distance * 10, originY - axisEquationX/distance*10,originX - axisEquationY/distance * 10, originY + axisEquationX/distance*10)
    for mark in range(len(axisMarks)):
        originX = width/2 + axisEquationX * (mark - len(axisMarks)/2)
        originY = height/2 +100 + axisEquationY * (mark -len(axisMarks)/2)
        canvas.coords(axisMarks[mark],originX - axisEquationY/distance * 20, originY + axisEquationX/distance*20)



    X = event.x - width/2
    Y = event.y - height/2
    X /= dotDistance
    Y /= dotDistance
    dx = (X**2 - Y**2)*dotDistance
    dy = 2*X*Y*dotDistance
    eventCoords[0] = dx;
    eventCoords[1] = dy;
    distance = (dx*dx + dy*dy)**.5
    canvas.coords(squareVector[0], width/2, height/2 +100,width/2 + dx, height/2 + dy + 100)
    canvas.coords(squareVector[1], width/2 + dx, height/2 + dy + 100 , (width/2 + dx - dx/distance * 10)- dy/distance * 10, (height/2 + dy -dy/distance*10)+ dx/distance *  10 + 100)
    canvas.coords(squareVector[2], width/2 + dx, height/2 + dy + 100 , (width/2 + dx - dx/distance * 10)+ dy/distance * 10, (height/2 + dy -dy/distance*10)- dx/distance *  10 + 100)

    canvas.update()

squareVector = []
def drawSquareVector(event):
    if len(squareVector) == 0:
        dx,dy = eventCoords[0], eventCoords[1]
        distance = (dx*dx + dy*dy)**.5
        arrow0 = canvas.draw_line(width/2,height/2 + 100, width/2 + dx, height/2 + dy + 100, fill="#0F0")
        arrow1 = canvas.draw_line(width/2 + dx, height/2 + dy + 100 , (width/2 + dx - dx/distance * 10)- dy/distance * 10, (height/2 + dy -dy/distance*10)+ dx/distance *  10 + 100, fill = "#0F0",time=.2)
        arrow2 = canvas.draw_line(width/2 + dx, height/2 + dy + 100 , (width/2 + dx - dx/distance * 10)+ dy/distance * 10, (height/2 + dy -dy/distance*10)- dx/distance *  10 + 100, fill="#0F0", time=.2)
        squareVector.append(arrow0)
        squareVector.append(arrow1)
        squareVector.append(arrow2)

canvas.bind_all('<B1-Motion>', moveAxis)
canvas.bind_all('<Button-1>', moveAxis)
canvas.bind_all('<s>', drawSquareVector)
canvas.bind_all('<l>',toogleY)
window.mainloop()
