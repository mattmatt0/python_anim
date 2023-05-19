import tkinter
import math
import time as timeModule
import colorHandler
def convertToFunction(pointList):
    functions = []
    sigmaDistance = 0
    for point in range(len(pointList)):
        pointX = pointList[point][0]
        pointY = pointList[point][1]
        originX = pointList[point-1][0]
        originY = pointList[point-1][1]
        if not (pointX == originX and pointY == originY):
            distance = math.sqrt((pointX-originX)**2 + (pointY-originY)**2)
            dx = (pointX-originX)/distance
            dy = (pointY-originY)/distance
            sigmaDistance += distance
            functions.append([originX,originY,dx,dy,sigmaDistance,distance])
    return functions
def functionsToPoints(functions,pointAmount):
    points = []
    totalLenght = functions[-1][4]
    partSize = totalLenght/pointAmount
    functionID = 0
    for x in range(pointAmount):
        while x*partSize >= functions[functionID][4]:
            functionID += 1
        sideDistance = functions[functionID][5]
        xSideDelta = (x/pointAmount*totalLenght - functions[functionID][4]+ functions[functionID][5])/totalLenght
        originX = functions[functionID][0]
        originY = functions[functionID][1]
        dx = functions[functionID][2]
        dy = functions[functionID][3]
        points.append([originX + xSideDelta*dx*totalLenght,originY + xSideDelta*dy*totalLenght])

    return points
sleep = timeModule.sleep
class Tk(tkinter.Tk):
    def setFullScreen(self):
        self.attributes('-fullscreen', True)
class BetterCanvas(tkinter.Canvas):
    def startFrame(self):
        self.frameTime = timeModule.time()
    def endFrame(self):
        self.update()
        while timeModule.time() < self.frameTime + 1/self.frameRate:
            pass
    def setFrameRate(self,framerate):
        self.frameRate = framerate
    def draw_line(self, startX, startY, endX, endY, fill = "#FFF", transition = "linear", time = 1):
        steps = time * self.frameRate;
        deltaX = endX - startX;
        deltaY = endY - startY;
        distance = math.sqrt(deltaX**2+deltaY**2)
        errorProp = 1/distance
        line = self.create_line(0,0,0,0)
        frames = self.generateFrames(transition, steps, errorProp);
        for frame in frames:
            self.startFrame()
            self.delete(line);
            line = self.create_line(startX, startY, startX + frame*deltaX, startY + frame * deltaY, fill=fill)
            self.endFrame()
        self.delete(line)
        line = self.create_line(startX,startY,endX,endY,fill=fill)
        self.update()
        return line


    def draw_lines(self, lines,fill="#FFF",transition="linear",time=1,delay=0):
        steps = time * self.frameRate
        errorProp = 0.001
        frames = self.generateFrames(transition, steps, errorProp)
        drawnLines = [self.create_line(-1,-1,-1,-1,fill = (lambda x: x[4] if len(x) == 5 else fill)(line)) for line in lines]
        for frameID in range(len(frames) + delay*len(lines)):
            self.startFrame()
            for line in range(len(lines)):
                frameRelativeID = frameID - line * delay
                if frameRelativeID < 0:
                    frame = 0;
                elif frameRelativeID >= len(frames):
                    frame = 1
                else:
                    frame = frames[frameRelativeID]
                startX, startY, endX, endY = lines[line][:4]
                dx = endX - startX
                dy = endY - startY
                if not frame == 0:
                    self.coords(drawnLines[line],startX, startY, startX + dx*frame, startY + dy * frame)
            self.endFrame()
        return drawnLines

    def generateFrames(self,transition, steps, errorProp):
        steps = int(steps)
        if transition == "easeOut":
            frames = self.transitionEaseOut(steps, errorProp)
        elif transition == "linear":
            frames = self.transitionLinear(steps, errorProp)
        elif transition == "easeIn":
            frames = self.transitionEaseIn(steps, errorProp)
        elif transition == "easeInOut":
            frames = self.transitionEaseInOut(steps, errorProp)
        else:
            print("Warning: invalid transition: \"{0}\"".format(transition))
            frames = [0]
        return frames

    def draw_polygon(self, *sides, time=1, transition="linear"):
        coordLists = [sides[2*c, 2*c+1] for c in range(int(len(sides)/2))]

        if len(sides) % 2 ==1:
            raise(RuntimeError("Invalid sideLenght"))
        else:
            sideAmount = int(len(sides)/2)
            steps = time*self.frameRate
            frames = self.generateFrames(transition)



    def wait(self,time):
        frames = time * self.frameRate;
        for frame in range(frames):
            sleep(1/self.frameRate);
            self.update();


    def transitionEaseOut(self, steps, error=0.01):
        f = error**(-1/steps)
        frames = []
        factor = 1
        for frame in range(steps):
            factor /= f
            frames.append(1 - factor)
        frames.append(1)
        return frames

    def transitionEaseIn(self, steps, error=0.01):
        f = error**(-1/steps)
        frames = []
        factor = error
        for frame in range(steps):
            factor *= f
            frames.append(factor)
        frames.append(1)
        return frames

    def transitionLinear(self,steps,error=0.01):
        return [(frame+1)/(steps-1) for frame in range(steps-1)]

    def transitionEaseInOut(self,steps,error=0.01):
        transEaseIn = [n/2 for n in self.transitionEaseIn(steps//2+steps%2,error)]
        transEaseOut= [.5 + n/2 for n in self.transitionEaseOut(steps//2,error)]
        return transEaseIn + transEaseOut

    def draw_text(self,x,y,text,font='Georgia',size=10,color="#FFF",spacing=10,spacingsIn=[],spacingsOut=[],transition='linear',method='fade',time=1,anchor='center'):
        if method == "size":
            spacingsIn = [spacing for n in range(len(text))] 
            spacingsOut = [spacing*-.3 for n in range(len(text))]
            if font == "Georgia":
                for letter in range(len(text)):
                    if text[letter] == 'É':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.25
                    if text[letter] == 'p':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.25
                    if text[letter] == 'i':
                        spacingsIn[letter] = spacing*.8
                        spacingsOut[letter] = spacing*-.5
                    if text[letter] == 'd':
                        spacingsIn[letter] = spacing*1.0
                        spacingsOut[letter] = spacing*-.35
                    if text[letter] == 'é':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'm':
                        spacingsIn[letter] = spacing*1.3
                        spacingsOut[letter] = spacing*-.1
                    if text[letter] == 'o':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == 'l':
                        spacingsIn[letter] = spacing*.8
                        spacingsOut[letter] = spacing*-.5
                    if text[letter] == 'g':
                        spacingsIn[letter] = spacing*0.9
                        spacingsOut[letter] = spacing*-.25
                    if text[letter] == 'e':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == 'M':
                        spacingsIn[letter] = spacing*.95
                        spacingsOut[letter] = spacing*-.1
                    if text[letter] == 'è':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == ' ':
                        spacingsIn[letter] = spacing
                        spacingsOut[letter] = spacing*-.5
                    if text[letter] == 'S':
                        spacingsIn[letter] = spacing*1.1
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == 'I':
                        spacingsIn[letter] = spacing*.9
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == 'R':
                        spacingsIn[letter] = spacing
                        spacingsOut[letter] = spacing*-.2
                    if text[letter] == ',':
                        spacingsIn[letter] = spacing*.8
                        spacingsOut[letter] = spacing*-.2
                    if text[letter] == 't':
                        spacingsIn[letter] = spacing*.9
                        spacingsOut[letter] = spacing*-.35
                    if text[letter] == 'q':
                        spacingsIn[letter] = spacing*1.1
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == 'u':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.3
                    if text[letter] == 's':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'a':
                        spacingsIn[letter] = spacing*.9
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'P':
                        spacingsIn[letter] = spacing*.9
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'r':
                        spacingsIn[letter] = spacing*.9
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'v':
                        spacingsIn[letter] = spacing*1
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'n':
                        spacingsIn[letter] = spacing*.9
                        spacingsOut[letter] = spacing*-.4
                    if text[letter] == 'D':
                        spacingsIn[letter] = spacing
                        spacingsOut[letter] = spacing*-.1
                    if text[letter] == 'G':
                        spacingsIn[letter] = spacing
                        spacingsOut[letter] = spacing*-.1

            canvasLetters = []
            totalMove = sum(spacingsIn)+sum(spacingsOut[:-1])
            for letter in range(len(text)):
                delta = sum(spacingsIn[:(letter+1)])+sum(spacingsOut[:(letter)])
                canvasLetters.append(self.create_text(x+delta-totalMove/2,y,text=text[letter],font=(font,1),fill=color))

            for letterSize in self.generateFrames(transition,30,.1)[1:]:
                for n in range(len(text)):
                        self.itemconfig(canvasLetters[n],font=(font,int(letterSize*size)))
                        self.update()
        if method == 'fade':
            bg  = self['background']
            canvasLetters = self.create_text(x,y,text=text,font=(font,size),fill=bg,anchor=anchor)
            if len(bg) == 4:
                bgR = int(bg[1]*2,16)
                bgG = int(bg[2]*2,16)
                bgB = int(bg[3]*2,16)
            else:
                bgR = int(bg[1:3],16)
                bgG = int(bg[3:5],16)
                bgB = int(bg[5:7],16)
            if len(color) == 4:
                cR = int(color[1]*2,16)
                cG = int(color[2]*2,16)
                cB = int(color[3]*2,16)
            else:
                cR = int(color[1:3],16)
                cG = int(color[3:5],16)
                cB = int(color[5:7],16)
            for frame in self.generateFrames(transition,time*self.frameRate,.001):
                self.startFrame()
                textColorR = hex(int(bgR+(cR-bgR)*frame))[2:]
                textColorG = hex(int(bgG+(cG-bgG)*frame))[2:]
                textColorB = hex(int(bgB+(cB-bgB)*frame))[2:]
                if len(textColorR) == 1:
                    textColorR = '0'+textColorR
                if len(textColorG) == 1:
                    textColorG = '0'+textColorG
                if len(textColorB) == 1:
                    textColorB = '0'+textColorB
                self.itemconfig(canvasLetters, fill='#'+textColorR+textColorG+textColorB)
                self.update()
                self.endFrame()
        return canvasLetters
    def delete_text(self,text,method="none",transition='linear',time=0):
        font=self.itemcget(text[0],'font').split(' ')
        if method == 'shrink':
            frames = self.generateFrames(transition, 5, .1)+ [1]
            for frameID in range(len(frames)*len(text)):
                for letter in range(len(text)):
                    fID =0
                    if letter<=frameID:
                        fID = frameID - letter
                    if fID >= len(frames):
                        size =-1              
                    else:
                        size=int((1-frames[fID])*int(font[1]))

                    self.itemconfig(text[letter], font=(font[0],size))
                self.update()
        for letter in text:
            self.delete(letter)
    def spawn_circle(self,x,y,radius, fill=None,outline=None,time=1,transition='linear'):
        frames = self.generateFrames(transition, time*self.frameRate, errorProp=.001)
        circle = self.create_oval(x,y,x,y,fill=fill,outline=outline)
        for frame in frames:
            self.startFrame()
            self.coords(circle ,x-radius*frame,y-radius*frame,x+radius*frame,y+radius*frame)
            self.update()
            self.endFrame()
        self.coords(circle ,x-radius,y-radius,x+radius,y+radius)
        self.update()
        return circle;
    def draw_pointSet(self,pointSet,time=1,transition='linear',color="#FFF",precision=1):
        pointSet = functionsToPoints(convertToFunction(pointSet),time*self.frameRate*precision)
        pointPerFrame = len(pointSet)/(self.frameRate*time)
        pointPerFrame = int(pointPerFrame)
        for frame in range(self.frameRate*time):
            self.startFrame()
            for point in range(int(pointPerFrame)):
                self.create_line(pointSet[frame*pointPerFrame+point][0],
                        pointSet[frame*pointPerFrame+point][1],
                        pointSet[frame*pointPerFrame+point-1][0],
                        pointSet[frame*pointPerFrame+point-1][1],fill=color)
            
            self.update()
            self.endFrame()
        for missingFrame in range(pointPerFrame*self.frameRate*time,len(pointSet)):
            self.create_line(pointSet[missingFrame][0],
                    pointSet[missingFrame][1],
                    pointSet[missingFrame-1][0],
                    pointSet[missingFrame-1][1],fill=color)
        self.update()
    def draw_arrow(self,x1,y1,x2,y2,fill="#FFF",transition='linear',time=1,arrowScale=10):
        distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
        dX = (x2-x1)/distance
        dY = (y2-y1)/distance
        arrow0 = self.draw_line(x1,y1,x2,y2,fill=fill,time=3*time/5,transition=transition)

        arrow1 = self.draw_line(x2,y2,x2-arrowScale*(dX+dY),y2-arrowScale*(dY-dX),fill=fill,time=time/5,transition=transition)
        arrow2 = self.draw_line(x2,y2,x2-arrowScale*(dX-dY),y2-arrowScale*(dY+dX),fill=fill,time=time/5,transition=transition)
        return [arrow0,arrow1,arrow2]
    def move_objects(self,objects,x,y,mode="absolute",transition="linear",time=1,independant=False):
        frames = self.generateFrames(transition,time*self.frameRate,0.01)
        oX = [self.coords(obj)[0] for obj in objects]
        oY = [self.coords(obj)[1] for obj in objects]
        if mode == "absolute" and independant:
            dX = [x-self.coords(obj)[0] for obj in objects]
            dY = [y-self.coords(obj)[1] for obj in objects]
        if mode == "absolute" and not independant:
            X = sum([self.coords(obj)[0] for obj in objects])/len(objects)
            Y = sum([self.coords(obj)[1] for obj in objects])/len(objects)
            dX = [x-X for obj in objects]
            dY = [y-Y for obj in objects]
        if mode == "relative":
            dX = [x for obj in objects]
            dY = [y for obj in objects]
        mX = [0 for obj in objects]
        mY = [0 for obj in objects]
        for frame in frames:
            self.startFrame()
            for obj in range(len(objects)):
                mvX = dX[obj]*frame - mX[obj]
                mvY = dY[obj]*frame - mY[obj]
                self.move(objects[obj], mvX,mvY)
                mX[obj] += mvX
                mY[obj] += mvY
            self.update()
            self.endFrame()

    def fade(self,objectID,targetColor,transition="linear",time=1):
        sourceColor = self.itemcget(objectID, "fill")[1:]
        targetColor = targetColor[1:]
        if len(targetColor)==3:
            sourceR = int(sourceColor[0]*2,16)
            sourceG = int(sourceColor[1]*2,16)
            sourceB = int(sourceColor[2]*2,16)
        else:
            sourceR = int(sourceColor[0:2],16)
            sourceG = int(sourceColor[2:4],16)
            sourceB = int(sourceColor[4:6],16)

        if len(targetColor)==3:
            targetR = int(targetColor[0]*2,16)
            targetG = int(targetColor[1]*2,16)
            targetB = int(targetColor[2]*2,16)
        else:
            targetR = int(targetColor[0:2],16)
            targetG = int(targetColor[2:4],16)
            targetB = int(targetColor[4:6],16)
        dR,dG,dB = targetR-sourceR,targetG-sourceG,targetB-sourceB
        frames = self.generateFrames(transition,self.frameRate*time,errorProp=0.001)
        for frame in frames:
            self.startFrame()
            self.itemconfig(objectID, fill=colorHandler.toHex(int(sourceR+dR*frame),int(sourceG+dG*frame),int(sourceB+dB*frame)))
            self.update()
            self.endFrame()
class PhotoImage(tkinter.PhotoImage):
    pass
