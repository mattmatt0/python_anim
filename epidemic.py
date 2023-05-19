# Caractéristiques de l'épidémie
infectionRadius = 5
infectionTime = 14
infectionChance = 0.2
immunityTime = 30
lethality = 0.25
# Caractéristiques de la population
moveSpeed = 1

#######################################################################################################
###--------------------------------------+---------------------+------------------------------------###
###::::::::::::::::::::::::::::::::::::::|      Définitions    |::::::::::::::::::::::::::::::::::::###
###--------------------------------------+---------------------+------------------------------------###
#######################################################################################################
from betterCanvas import *
from random import *
from math import *
from colorHandler import *
window = Tk()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.setFullScreen()
canvas = BetterCanvas(window, width=width, height=height, bg="#000",highlightthickness=0)
canvas.setFrameRate(50)
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

class Character:
    def __init__(self,x,y):
        self.state = "s"
        self.x = x
        self.y = y
        self.infectionRadius = canvas.create_oval(self.x,self.y,self.x,self.y,outline="#F00",state="hidden")
        self.drawable = canvas.spawn_circle(self.x,self.y,3,fill="#0CF",outline="#0CF",time=.01)
        self.speed = 1
        self.back = False
        self.isolated = False
        self.distanceVectorsX = []
        self.distanceVectorsY = []


    def changeDirection(self,x=None,y=None):
        if x == None: x = randint(int(boxCoords[0]+3),int(boxCoords[2])-3);
        if y == None: y= randint(int(boxCoords[3]+3),int(boxCoords[1])-3);
        self.destinationX,self.destinationY = x,y
        self.directionX = (self.destinationX - self.x)
        self.directionY = (self.destinationY - self.y)
        self.distance = sqrt(self.directionX**2+self.directionY**2)
        self.directionX /= self.distance*canvas.frameRate/100
        self.directionY /= self.distance*canvas.frameRate/100

    def move(self,confin=False,moveSpeed=1,test=False):
        self.x += self.directionX*self.speed
        self.y += self.directionY*self.speed
        canvas.coords(self.drawable, self.x-3, self.y-3, self.x+3, self.y+3)
        if abs(self.x -self.destinationX)<6 and abs(self.y -self.destinationY)<6:
            if not self.isolated:
                self.changeDirection()
                if self.back:
                    self.back = False
                else:
                    self.speed = moveSpeed
            else:
                self.directionX = 0
                self.directionY = 0

        if confin:
            if random() < 0.001 and not self.isolated:
                self.changeDirection(x = (boxCoords[0]+boxCoords[2])/2, y = (boxCoords[1]+boxCoords[3])/2)
                self.speed = 1
                self.back = True
        else:
            if not self.isolated:
                self.speed = 1


    def getSick(self):
        self.state = "i"
        canvas.itemconfig(self.drawable,fill="#F00",outline="#F00")
        canvas.itemconfig(self.infectionRadius,state="normal")
        self.infectionTime = infectionTime + round((random()-.5)*infectionTime/10)


    def checkContact(self, character):
        if (self.x-character.x)**2+(self.y-character.y)**2 < infectionRadius**2:
            if not self.isolated:
                if random() < infectionChance:
                        character.getSick()
            else:
                if random()*8 < infectionChance:
                        character.getSick()

    def checkSocialDistance(self, character):
        if not self.isolated:
            if len(self.distanceVectorsX):
                self.changeDirection(self.x+sum(self.distanceVectorsX)/len(self.distanceVectorsX),self.y+sum(self.distanceVectorsY)/len(self.distanceVectorsY))
            self.distanceVectorsX = []
            self.distanceVectorsY = []
            d = (self.x-character.x)**2+(self.y-character.y)**2
            if d < 256:
                dx, dy = (character.x-self.x), (character.y-self.y)
                character.distanceVectorsX.append(dx)
                character.distanceVectorsY.append(dy)
                return True
            else:
                return False
        else:
            return False



    def pulse(self,time):
        pS = (pulseState+time*5)%100
        canvas.coords(self.infectionRadius,self.x+infectionRadius*pS/100,self.y+infectionRadius*pS/100,self.x-infectionRadius*pS/100,self.y-infectionRadius*pS/100)
        canvas.itemconfig(self.infectionRadius,outline=toHex(int(255-(pS/100)*255),0,0))


    def recover(self):
        canvas.itemconfig(self.drawable,fill="#CCC",outline="#CCC")
        self.state = 'r'
        canvas.itemconfig(self.infectionRadius,state="hidden")
    def heal(self,confin=False):
        canvas.itemconfig(self.drawable,fill="#0F0",outline="#0F0")
        self.state = 'h'
        canvas.itemconfig(self.infectionRadius,state="hidden")
        self.immunityTime = immunityTime + round((random()-.5))*immunityTime/10
        self.isolated = False
        if not confin:
            self.speed = 1
    def reset(self):
        self.state = 's'
        canvas.itemconfig(self.drawable,fill="#0AF",outline="#0AF")
    def die(self):
        self.state = "d"
        canvas.itemconfig(self.drawable,fill="#000",outline="#333")
        canvas.itemconfig(self.infectionRadius,state="hidden")
    def isolate(self):
        self.changeDirection(boxCoords[0]-width/40,(boxCoords[1]+boxCoords[3])/2)
        self.speed = 3
        self.isolated = True


def simuWithDeath():
    global sir
    global pulseState
    global infectionRadius
    global infectionChance
    [canvas.delete(element) for element in sir]
    sir = canvas.draw_text(width/2-400,height/2+50,"Modèle SIDG",size=50,spacing=50,font="Georgia",method="size")
    D = R
    G = canvas.create_text(width/2-550,height/2+190,text="Guéri      :0", font=('Courier',20), fill="#0F0",anchor='nw')
    (canvas.itemconfig(obj,state="normal") for obj in (*box,*sir,S,I,R,graphRectangle))
    canvas.itemconfig(S,text='Susceptible:'+str(128))
    canvas.itemconfig(I,text='Infecté    :'+str(0))
    canvas.itemconfig(D,text='Décédé     :'+str(0))
    [canvas.itemconfig(obj,state="normal") for obj in [*box,*sir,S,I,R,graphRectangle]]
    simu = True
    while simu:
        test = False
        moveSpeed = 1
        confin=False
        socialDistancing = False
        characters = []
        for n in range(128):
            characters.append(Character(randint(int(boxCoords[0]+3),int(boxCoords[2])-3),randint(int(boxCoords[3]+3),int(boxCoords[1]-3))))
            characters[-1].changeDirection()
        while True:
            canvas.startFrame()
            for character in characters:
                character.move()
            if 'space' in keysPressed:
                characters[0].getSick()
                break
            canvas.update()
            canvas.endFrame()
        susceptibles = characters[1:]
        infecteds = [characters[0]]
        removeds = []
        recovereds = []
        canvas.itemconfig(S,text='Susceptible:'+str(len(susceptibles)))
        canvas.itemconfig(I,text='Infecté    :'+str(len(infecteds)))
        canvas.itemconfig(D,text='Décédé     :'+str(len(removeds)))
        canvas.itemconfig(G,text='Guéri      :'+str(len(recovereds)))
        history = [[1,0,0]]
        time = 1
        graphWidth = width/2-height/5
        graphHeight = 3*height/10
        deltaTime = graphWidth/149
        graph = []
        while True:
            canvas.startFrame()
            [canvas.delete(plot) for plot in graph]
            dIll = 0
            dRec = 0
            dRei = 0
            if socialDistancing:
                for character in range(len(susceptibles+infecteds+recovereds)):
                    for character2 in range(character+1,len(susceptibles+infecteds+recovereds)):
                        if (susceptibles+infecteds+recovereds)[character].checkSocialDistance((susceptibles+infecteds+recovereds)[character2]):
                            if (susceptibles+infecteds+recovereds)[character].state == "i": 
                                (susceptibles+infecteds+recovereds)[character].checkContact((susceptibles+infecteds+recovereds)[character2])
                            elif (susceptibles+infecteds+recovereds)[character2].state == "i": 
                                (susceptibles+infecteds+recovereds)[character2].checkContact((susceptibles+infecteds+recovereds)[character])
            for character in range(len(susceptibles)):
                if susceptibles[character-dIll].state == 'i':
                    infecteds.append(susceptibles[character-dIll])
                    susceptibles.pop(character-dIll)
                    dIll += 1
                else:
                    susceptibles[character-dIll].move(confin,moveSpeed)
            for character in range(len(infecteds)):
                if not socialDistancing:
                    for s in susceptibles:
                        infecteds[character-dRec].checkContact(s)
                infecteds[character-dRec].infectionTime -= .05
                if test:
                    if random() < 0.03:
                        infecteds[character-dRec].isolate()
                if infecteds[character-dRec].infectionTime <= 0:
                    if random() < lethality*(1+(len(infecteds)-16)/128):
                        infecteds[character-dRec].die()
                        removeds.append(infecteds[character-dRec])
                    else:
                        infecteds[character-dRec].heal(confin)
                        recovereds.append(infecteds[character-dRec])
                    infecteds.pop(character-dRec)
                    dRec += 1

                else:
                    infecteds[character-dRec].move(confin,moveSpeed)
                    infecteds[character-dRec].pulse(character)
            for recovered in range(len(recovereds)):
                recovereds[recovered-dRei].move(confin,moveSpeed)
                recovereds[recovered-dRei].immunityTime -= .05
                if recovereds[recovered-dRei].immunityTime <= 0:
                    recovereds[recovered-dRei].reset() 
                    susceptibles.append(recovereds[recovered-dRei])
                    recovereds.pop(recovered-dRei)
                    dRei += 1
            history.append([len(infecteds),len(recovereds),len(removeds)])
            graph = []
            for point in range(149):
                p1 = ((point+1)*len(history))//150
                p2 = (point*len(history))//150
                graph.append(canvas.create_polygon(height/10+deltaTime*point,            4*height/10,
                        height/10+deltaTime*(point+1),    4*height/10,
                        height/10+deltaTime*(point+1),    4*height/10 - graphHeight/128*history[p1][0],
                        height/10+deltaTime*point,        4*height/10 - graphHeight/128*history[p2][0],fill="#F00",outline='#F00'))
                graph.append(canvas.create_polygon(height/10+deltaTime*point,            height/10,
                        height/10+deltaTime*(point+1),        height/10,
                        height/10+deltaTime*(point+1),        height/10 + graphHeight/128*(history[p1][1]+history[p1][2]),
                        height/10+deltaTime*point,            height/10 + graphHeight/128*(history[p2][1]+history[p2][2]),fill="#0F0",outline='#0F0'))
                graph.append(canvas.create_polygon(height/10+deltaTime*point,            height/10,
                        height/10+deltaTime*(point+1),        height/10,
                        height/10+deltaTime*(point+1),        height/10 + graphHeight/128*history[p1][2],
                        height/10+deltaTime*point,            height/10 + graphHeight/128*history[p2][2],fill="#333",outline='#333'))
            if 'c' in keysPressed:
                confin = True
                moveSpeed = 0.1
            if 'd' in keysPressed:
                confin = False
                moveSpeed = 1
                test = False
                socialDistancing = False
                canvas.setFrameRate(50)
                infectionChance = .6
            if 't' in keysPressed:
                test = True
            if 'm' in keysPressed:
                infectionRadius = 2
            if 'e' in keysPressed:
                for character in characters:
                    canvas.delete(character.drawable)
                    canvas.delete(character.infectionRadius)
                for element in graph:
                    canvas.delete(element)
                canvas.setFrameRate(50)
                simu=False
                break
            if 'p' in keysPressed:
                waitUntilSpacePress()

            if 's' in keysPressed:
                socialDistancing = True
                canvas.setFrameRate(30)
            if 'b' in keysPressed:
                infectionChance = .1
            if 'r' in keysPressed:
                for character in characters:
                    canvas.delete(character.drawable)
                    canvas.delete(character.infectionRadius)
                for element in graph:
                    canvas.delete(element)
                break;
            pulseState += 1
            pulseState %= 100
            canvas.itemconfig(S,text='Susceptible:'+str(len(susceptibles)))
            canvas.itemconfig(I,text='Infecté    :'+str(len(infecteds)))
            canvas.itemconfig(D,text='Décédé     :'+str(len(removeds)))
            canvas.itemconfig(G,text='Guéri      :'+str(len(recovereds)))
            canvas.endFrame()
    [canvas.itemconfig(obj,state="hidden") for obj in [*box,*sir,S,I,D,G,graphRectangle]]

#######################################################################################################
###--------------------------------------+---------------------+------------------------------------###
###::::::::::::::::::::::::::::::::::::::|        Titre        |::::::::::::::::::::::::::::::::::::###
###--------------------------------------+---------------------+------------------------------------###
#######################################################################################################
waitUntilSpacePress()
txt = canvas.draw_text(width/2-width/3,height/2-width/30,"Épidémiologie",size=int(width/30),spacing=int(width/30),font="Georgia",method="size")
waitUntilSpacePress()
txt2 = canvas.draw_text(width/20,height/2+int(width/30),text="Étude des facteurs liés à l'apparition, au développement, et parfois la transmission de variations\n de l'état de santé dans une population. Cela inclut les maladies infectieuses (où l'on étudie \naussi la fréquence d'apparition d'une épidémie), mais aussi les cancers ou encore le diabète \npar exemple.",size=int(width/75),method='fade',time=1,color="#FFF",transition='linear',anchor='w')
waitUntilSpacePress()
canvas.delete_text(txt,method='shrink',time=5)
for n in range(1000):
    canvas.move(txt2, 0,-1)
    canvas.update()
canvas.delete(txt2)
stats = canvas.draw_text(width/2,height/2-int(width/20),"Statistiques",size=int(width/30),spacing=int(width/30),font="Georgia",method="size")
prevs = canvas.draw_text(width/2,height/2,"Prévisions",size=int(width/30),spacing=int(width/30),font="Georgia",method="size")
prevn = canvas.draw_text(width/2,height/2+int(width/20),"Prévention",size=int(width/30),spacing=int(width/30),font="Georgia",method="size")
pointer = canvas.draw_arrow(width/2-width/6,height/2+int(width/20),width/2-width/10,height/2+int(width/20))
waitUntilSpacePress()
canvas.delete_text(prevs,method="shrink",time=.5)
canvas.delete_text(prevn,method="shrink",time=.5)
for n in range(3):
    canvas.delete(pointer[n])
    canvas.update()
    sleep(.01)
for n in range(80):
    [canvas.move(obj, 0, int(width/20)/80) for obj in stats]
    canvas.update()
    sleep(.01)
waitUntilSpacePress()




#######################################################################################################
###---------------------------+--------------------------------------------+------------------------###
###:::::::::::::::::::::::::::|                 Statistiques               |::::::::::::::::::::::::###
###---------------------------+--------------------------------------------+------------------------###
#######################################################################################################
canvas.move_objects(stats, width/2,width/30,independant=False,transition="easeInOut")
drawings = []
diseased = []
d1 = []
d2 = []
studyRectangle = canvas.create_rectangle(width/15-width/300,
        width/30 +(height-40*width/100)/2-width/300,
        width/15+width/300,
        width/30 +(height-40*width/100)/2-width/300+40*width/100-width/300,fill="#000",outline="#000")
for n in range(40):
    for a in range(40):
        drawings.append(canvas.spawn_circle(width/15 + n*width/100,width/30 +(height-40*width/100)/2+a*width/100,width/300,time=.01,fill="#0AF",outline="#0AF"))

for n in range(40):
    d1.append(0)
    d2.append(0)
    for a in range(40):
        if randint(0,5)==5:
            canvas.itemconfig(drawings[40*n+a],fill="#B0B",outline="#B0B")
            d1[-1] += 1
        if randint(0,5)==5:
            diseased.append(canvas.spawn_circle(width/15 + n*width/100,width/30 +(height-40*width/100)/2+a*width/100,width/500,time=.01,fill="#FF0",outline="#FF0"))
            d2[-1] += 1
        canvas.update()
canvas.fade(studyRectangle,"#C80",time=.5)
canvas.itemconfig(studyRectangle,outline="#C80")
sizeOfScreen = 40 * width/100
arrowX = canvas.draw_arrow(width/2,height/5+sizeOfScreen,width/2+sizeOfScreen,height/5+sizeOfScreen,fill="#B0B")
arrowY = canvas.draw_arrow(width/2,height/5+sizeOfScreen,width/2, height/5,fill="#FF0")
plots = []
waitUntilSpacePress()
for n in range(40):
    plots.append(canvas.spawn_circle(width/2+d1[n]*sizeOfScreen/20,height/5+sizeOfScreen-sizeOfScreen/20*d2[n],3,fill='#B0B',outline="#FF0",time=.1))
    if n ==39:
        canvas.fade(studyRectangle,"#000",time=.5)
    else:
        canvas.move_objects([studyRectangle],width/100,0,mode="relative",independant=True,time=.1,transition="easeInOut")

waitUntilSpacePress()
[canvas.delete(plot) for plot in plots]
canvas.move(studyRectangle,-39*width/100,0)

[canvas.itemconfig(obj,fill="#0AF",outline="#0AF") for obj in drawings]
d1,d2,d3,plots = [],[],[],[]
for n in range(40):
    d1.append(0)
    d2.append(0)
    d3.append(0)
    for a in range(40):
        if randint(0,1)==1:
            canvas.itemconfig(drawings[40*n+a],fill="#B0B",outline="#B0B")
            d1[-1] += 1
            if randint(0,1)==1:
                diseased.append(canvas.spawn_circle(width/15 + n*width/100,width/30 +(height-40*width/100)/2+a*width/100,width/500,time=.01,fill="#FF0",outline="#FF0"))
                d2[-1] += 1
                d3[-1] += 1
        else:
            if randint(0,40)==40:
                diseased.append(canvas.spawn_circle(width/15 + n*width/100,width/30 +(height-40*width/100)/2+a*width/100,width/500,time=.01,fill="#FF0",outline="#FF0"))
                d2[-1] += 1
        canvas.update()
canvas.fade(studyRectangle,"#C80",time=.5)
waitUntilSpacePress()
for n in range(40):
    plots.append(canvas.spawn_circle(width/2 + d1[n]*sizeOfScreen/40,height/5+sizeOfScreen - sizeOfScreen/40*d2[n],3,fill='#B0B',outline="#FF0",time=.1))
    if n ==39:
        canvas.fade(studyRectangle,"#000",time=.5)
    else:
        canvas.move_objects([studyRectangle],width/100,0,mode="relative",independant=True,time=.1,transition="easeInOut")
waitUntilSpacePress()
k = sum([d2[n]/d1[n] for n in range(len(d1))])/len(d1)
med1 = sum(d1)/len(d1)
med2 = sum(d2)/len(d2)
tendencies = [canvas.draw_line(width/2,height/5+sizeOfScreen,width/2+600,height/5+sizeOfScreen-k*600,transition="easeInOut"),
canvas.draw_line(width/2+med1*sizeOfScreen/40,height,width/2+med1*sizeOfScreen/40,0,transition="easeInOut"),
canvas.draw_line(width/2,height/5+sizeOfScreen-med2*sizeOfScreen/40,width,height/5+sizeOfScreen-med2*sizeOfScreen/40,transition="easeInOut")]
waitUntilSpacePress()
cache = canvas.create_rectangle(0,0,width,0,fill="#000",outline="#000")
for n in range(int(log(height)/log(1.07)+1)):
    canvas.coords(cache,0,0,width,1.1**n)
    canvas.update()
[canvas.delete(plot) for plot in plots]
[canvas.delete(obj) for obj in [*drawings,*diseased,studyRectangle,*stats,*arrowX,*arrowY,*tendencies]]

doubt = [canvas.spawn_circle(width/2-50,height/2-50,25,fill="#B0B",outline="#B0B",time=.5),
*canvas.draw_arrow(width/2-20,height/2-50,width/2+20,height/2-50,time=.5),
canvas.spawn_circle(width/2+50,height/2-50,15,fill="#FF0",outline="#FF0",time=.5),
#
canvas.spawn_circle(width/2-50,height/2,15,fill="#FF0",outline="#FF0",time=.5),
*canvas.draw_arrow(width/2-20,height/2,width/2+20,height/2,time=.5),
canvas.spawn_circle(width/2+50,height/2,25,fill="#B0B",outline="#B0B",time=.5),
#
canvas.spawn_circle(width/2-50,height/2+50,25,fill="#B0B",outline="#B0B",time=.5),
*canvas.draw_arrow(width/2-5,height/2+50,width/2-20,height/2+50,arrowScale = 3,time=.2),
canvas.draw_text(width/2+5,height/2+50,"?",time=.5,size=30,method="fade"),
*canvas.draw_arrow(width/2+15,height/2+50,width/2+30,height/2+50,arrowScale = 3,time=.2),
canvas.spawn_circle(width/2+50,height/2+50,15,fill="#FF0",outline="#FF0",time=.5)]

waitUntilSpacePress()
[canvas.delete(obj) for obj in doubt]






#######################################################################################################
###---------------------------+--------------------------------------------+------------------------###
###:::::::::::::::::::::::::::|Animation de l'appartition de la simulation |::::::::::::::::::::::::###
###---------------------------+--------------------------------------------+------------------------###
#######################################################################################################
prev = canvas.draw_text(width/2,height/10,"Prévision",size=50,spacing=50,font="Georgia",method="size")
simu = canvas.draw_text(width/2,9*height/10,"Exemple: simulation d'une épidémie",size=40)
#sir = canvas.draw_text(width/2-400,height/2+50,"Modèle SIR",size=50,spacing=50,font="Georgia",method="size")
sir = canvas.draw_text(width/2,height/2,"Modèle SIR",size=50,spacing=50,font="Georgia",method="size")
waitUntilSpacePress()
canvas.delete_text(prev,method='shrink', time=1)
canvas.delete_text([simu],method='shrink', time=1)
canvas.move_objects(sir, width/2-400,height/2+50,mode="absolute",transition="easeInOut",time=1)
waitUntilSpacePress()
S = canvas.create_text(width/2-1050,height/2+100,text="Susceptible", font=('Courier',20), fill="#0AF",anchor='nw')
I = canvas.create_text(width/2-1050,height/2+130,text="Infected", font=('Courier',20), fill="#F00",anchor='nw')
R = canvas.create_text(width/2-1050,height/2+160,text="Removed", font=('Courier',20), fill="#CCC",anchor='nw')
graphRectangle = canvas.create_rectangle(height/10, height/10, width/2 - 1*height/10,4*height/10,fill="#0AF",outline="#FFF")
for n in range(25):
    canvas.startFrame()
    canvas.move(S,20,0)
    canvas.move(I,20,0)
    canvas.move(R,20,0)
    canvas.update()
    canvas.endFrame()
waitUntilSpacePress()
textS = ['S','u','s','c','e','p','t','i','b','l','e',' ',' ',' ',' ']
textI = ['I','n','f','e','c','t','e','d',' ',' ',' ',' ',' ',' ',' ']
textR = ['R','e','m','o','v','e','d',' ',' ',' ',' ',' ',' ',' ',' ']   
for letter in range(len("Susceptible:128")):
    textS[letter] = '|'
    textI[letter] = '|'
    textR[letter] = '|'
    canvas.itemconfig(S,text=''.join(textS))
    canvas.itemconfig(I,text=''.join(textI))
    canvas.itemconfig(R,text=''.join(textR))
    sleep(.02)
    canvas.update()
    textS[letter] = "Susceptible:128"[letter]
    textI[letter] = "Infecté    :0  "[letter]
    textR[letter] = "Sorti      :0  "[letter]
    canvas.itemconfig(S,text=''.join(textS))
    canvas.itemconfig(I,text=''.join(textI))
    canvas.itemconfig(R,text=''.join(textR))
    sleep(.02)
    canvas.update()
pulseState = 0
boxCoords = [width - 9*height/10, height/2+4*height/10, width-height/10, height/2- 4*height/10]
lineCoords = [[*boxCoords[:2],boxCoords[2],boxCoords[1]],
        [boxCoords[2],boxCoords[1],*boxCoords[2:]],
        [*boxCoords[2:],boxCoords[0],boxCoords[3]],
        [boxCoords[0],boxCoords[3],*boxCoords[:2]]]
box = canvas.draw_lines(lineCoords,time=.6,delay=10,transition="linear")









#######################################################################################################
###--------------------------------------+---------------------+------------------------------------###
###::::::::::::::::::::::::::::::::::::::| Première Simulation |::::::::::::::::::::::::::::::::::::###
###--------------------------------------+---------------------+------------------------------------###
#######################################################################################################
simu = True
while simu:
    characters = []
    for n in range(128):
        characters.append(Character(randint(int(boxCoords[0]+3),int(boxCoords[2])-3),randint(int(boxCoords[3]+3),int(boxCoords[1]-3))))
        characters[-1].changeDirection()
    while True:
        canvas.startFrame()
        for character in characters:
            character.move()
        if 'space' in keysPressed:
            characters[0].getSick()
            break
        canvas.update()
        canvas.endFrame()
    susceptibles = characters[1:]
    infecteds = [characters[0]]
    removeds = []
    canvas.itemconfig(S,text='Susceptible:'+str(len(susceptibles)))
    canvas.itemconfig(I,text='Infecté    :'+str(len(infecteds)))
    canvas.itemconfig(R,text='Guéri      :'+str(len(removeds)))
    history = [[1,0]]
    time = 1
    graphWidth = width/2-height/5
    graphHeight = 3*height/10
    deltaTime = graphWidth/200
    graph = []
    while True:
        canvas.startFrame()
        [canvas.delete(plot) for plot in graph]
        dIll = 0
        dRec = 0
        for character in range(len(susceptibles)):
            if susceptibles[character-dIll].state == 'i':
                infecteds.append(susceptibles[character-dIll])
                susceptibles.pop(character-dIll)
                dIll += 1
            else:
                susceptibles[character-dIll].move()
        for character in range(len(infecteds)):
            for s in susceptibles:
                infecteds[character-dRec].checkContact(s)
            infecteds[character-dRec].infectionTime -= .05
            if infecteds[character-dRec].infectionTime <= 0:
               infecteds[character-dRec].recover()
               removeds.append(infecteds[character-dRec])
               infecteds.pop(character-dRec)
               dRec += 1
            else:
                infecteds[character-dRec].move()
                infecteds[character-dRec].pulse(character)
        for removed in removeds:
            removed.move()
        history.append([len(infecteds),len(removeds)])
        graph = []
        for point in range(199):
            graph.append(canvas.create_polygon(height/10+deltaTime*point,            4*height/10,
                    height/10+deltaTime*(point+1),    4*height/10,
                    height/10+deltaTime*(point+1),    4*height/10 - graphHeight/128*history[((point+1)*len(history))//200][0],
                    height/10+deltaTime*point,        4*height/10 - graphHeight/128*history[(point*len(history))//200][0],fill="#F00",outline='#F00'))
            graph.append(canvas.create_polygon(height/10+deltaTime*point,            height/10,
                    height/10+deltaTime*(point+1),        height/10,
                    height/10+deltaTime*(point+1),        height/10 + graphHeight/128*history[((point+1)*len(history))//200][1],
                    height/10+deltaTime*point,            height/10 + graphHeight/128*history[(point*len(history))//200][1],fill="#CCC",outline='#CCC'))
        canvas.update()
        if 'c' in keysPressed:
            moveSpeed = 0
        if 'd' in keysPressed:
            moveSpeed = 1
        if 'e' in keysPressed:
            for character in characters:
                canvas.delete(character.drawable)
                canvas.delete(character.infectionRadius)
            for element in graph:
                canvas.delete(element)
            simu=False
            break
        if 'p' in keysPressed:
            waitUntilSpacePress()
        if 'r' in keysPressed:
            for character in characters:
                canvas.delete(character.drawable)
                canvas.delete(character.infectionRadius)
            for element in graph:
                canvas.delete(element)
            break;
        pulseState += 1
        pulseState %= 100
        canvas.itemconfig(S,text='Susceptible:'+str(len(susceptibles)))
        canvas.itemconfig(I,text='Infecté    :'+str(len(infecteds)))
        canvas.itemconfig(R,text='Sorti      :'+str(len(removeds)))
        canvas.endFrame()

#######################################################################################################
###---------------------------+----------------------------------------+----------------------------###
###:::::::::::::::::::::::::::|         Les maladies diffèrent         |::::::::::::::::::::::::::::###
###---------------------------+----------------------------------------+----------------------------###
#######################################################################################################
[canvas.itemconfig(obj,state="hidden") for obj in [*box,*sir,S,I,R,graphRectangle]]
canvas.itemconfig(S,text='Susceptible:128')
canvas.itemconfig(I,text='Infecté    :0')
canvas.itemconfig(R,text='Sorti      :0')
canvas.update()
virusBody = canvas.spawn_circle(width/2,height/2,100,transition = 'easeIn',outline="#FFF",time=.5)
lines = [[width/2+100*cos(angle/30*2*pi),
    height/2+100*sin(angle/30*2*pi),
    width/2+120*cos(angle/30*2*pi),
    height/2+120*sin(angle/30*2*pi)] for angle in range(30)]
virusSpikes = canvas.draw_lines(lines,time=.1)
virusCircles = [canvas.spawn_circle(*[lines[n][2],lines[n][3]],5,fill="#FFF",outline='#FFF',time=.05) for n in range(30)]
waitUntilSpacePress()
for n in range(30):
    canvas.startFrame()
    [canvas.move(obj,-n,0) for obj in [virusBody,*virusSpikes,*virusCircles]]
    canvas.update()
    canvas.endFrame()
waitUntilSpacePress()
texts = ["- Bactérie", "- Virus","- Champignon","- Parasite","- Prion"]
pathogs = [canvas.draw_text(width/2,height/2-100+50*text,text=texts[text],size=30,method='fade',time=.2,color="#FFF",transition='easeOut',anchor = 'w') for text in range(5)]
waitUntilSpacePress()
[canvas.delete(obj) for obj in [virusBody,*virusSpikes,*virusCircles,*pathogs]]







#######################################################################################################
###---------------------------+----------------------------------------+----------------------------###
###:::::::::::::::::::::::::::|     Meurt / immunisé temporairement    |::::::::::::::::::::::::::::###
###---------------------------+----------------------------------------+----------------------------###
#######################################################################################################

simuWithDeath()



#######################################################################################################
###---------------------------+----------------------------------------+----------------------------###
###:::::::::::::::::::::::::::|       Change le rayon d'infection      |::::::::::::::::::::::::::::###
###---------------------------+----------------------------------------+----------------------------###
#######################################################################################################
for radiusChange in [6.25,9]:
    if radiusChange > infectionRadius:
        mode = 1
    else:
        mode = 0
    infectedExample = canvas.spawn_circle(width/2,height/2,5,fill="#F00")
    examplePulse = canvas.create_oval(width/2,height/2,width/2,height/2,outline="#F00")
    pS = 0
    radiusDisplay = canvas.draw_text(height/10,9*height/10,size=30,text="Rayon d'infection:"+str(round(infectionRadius,2)),anchor='w')
    while True:
        canvas.startFrame()
        canvas.coords(examplePulse,width/2+5+infectionRadius*pS/100,height/2+5+infectionRadius*pS/100,width/2-5-infectionRadius*pS/100,height/2-5-infectionRadius*pS/100)
        canvas.itemconfig(examplePulse,outline=toHex(int(255-(pS/100)*255),0,0))
        pS %= 100
        pS += 1
        if 'r' in keysPressed:
            while round(infectionRadius,2) != round(radiusChange,2):
                pS = 100
                canvas.coords(examplePulse,width/2+5+infectionRadius*pS/100,height/2+5+infectionRadius*pS/100,width/2-5-infectionRadius*pS/100,height/2-5-infectionRadius*pS/100)
                canvas.itemconfig(examplePulse,outline='#F00')
                if mode == 0:
                    infectionRadius -= .05
                if mode == 1:
                    infectionRadius += .05
                canvas.itemconfig(radiusDisplay,text="Rayon d'infection:"+str(round(infectionRadius,2)))
                canvas.update()
        if 'e' in keysPressed:
            break
        canvas.update()
        canvas.endFrame()
    for n in range(0,64):
        canvas.startFrame()
        canvas.coords(infectedExample, width/2 + 5*n,height/2+5*n,width/2-5*n,height/2-5*n)
        canvas.coords(examplePulse,width/2+5*(n+1),height/2+5*(n+1),width/2-5*(n+1),height/2-5*(n+1))
        canvas.itemconfig(examplePulse,fill=toHex(int(255-4*n),0,0),outline=toHex(int(255-4*n),0,0))
        canvas.itemconfig(infectedExample,outline=toHex(int(255-4*n),0,0))
        if n < 32:
            canvas.itemconfig(radiusDisplay,fill=toHex(int(255-8*n),int(255-8*n),int(255-8*n)))
        if n == 32:
            canvas.delete(radiusDisplay)
        canvas.update()
        canvas.endFrame()
    waitUntilSpacePress()

    canvas.delete(infectedExample)
    canvas.delete(examplePulse)
    simuWithDeath()





infectionRadius = 5
#######################################################################################################
###-----------------------------------+---------------------------+---------------------------------###
###:::::::::::::::::::::::::::::::::::|        Probabilité        |:::::::::::::::::::::::::::::::::###
###-----------------------------------+---------------------------+---------------------------------###
#######################################################################################################
prob = canvas.draw_text(width/2,height/2,text="Probabilité d'infection:",method="fade",size=int(width/30))
dispProb = canvas.draw_text(3*width/4,height/2,text=str(round(infectionChance,3)),method="fade",size=int(width/30),anchor="w")
canvas.setFrameRate(800)
infectionChance = .2
for n in range(800):
    canvas.startFrame()
    infectionChance += 0.001
    canvas.itemconfig(dispProb,text=str(round(infectionChance,3)))
    canvas.endFrame()
waitUntilSpacePress()
canvas.fade(dispProb,"#000",time=.5)
canvas.fade(prob,"#000",time=.5)
canvas.delete(dispProb)
canvas.delete(prob)
canvas.setFrameRate(50)
simuWithDeath()


#######################################################################################################
###-----------------------------------+---------------------------+---------------------------------###
###:::::::::::::::::::::::::::::::::::|     Variation létalité    |:::::::::::::::::::::::::::::::::###
###-----------------------------------+---------------------------+---------------------------------###
#######################################################################################################
infectionRadius=5
infectionChance=.3
for multiplier in (-1,2):
    prob = canvas.draw_text(width/2,height/2,text="Létalité:",method="fade",size=int(width/30))
    dispProb = canvas.draw_text(19*width/32,height/2,text=str(round(lethality,3)),method="fade",size=int(width/30),anchor="w")
    canvas.setFrameRate(250)
    for n in range(250):
        canvas.startFrame()
        lethality += 0.001*multiplier
        canvas.itemconfig(dispProb,text=str(round(lethality,3)))
        canvas.endFrame()
    waitUntilSpacePress()
    canvas.fade(dispProb,"#000",time=.5)
    canvas.fade(prob,"#000",time=.5)
    canvas.delete(dispProb)
    canvas.delete(prob)
    canvas.setFrameRate(50)
    simuWithDeath()






lethality = .25

#######################################################################################################
###-----------------------------------+---------------------------+---------------------------------###
###:::::::::::::::::::::::::::::::::::| Actions contre l'épidémie |:::::::::::::::::::::::::::::::::###
###-----------------------------------+---------------------------+---------------------------------###
#######################################################################################################

" Masques "
rectLines = [width/5+width/40,height/2+width/100,width/5-width/40,height/2+width/30]

circleLines = [[cos(2*pi*(n-1)/25),sin(2*pi*(n-1)/25),cos(2*pi*(n)/25),sin(2*pi*(n)/25)] for n in range(25)]
circleLines = [[n[0]*width/20+width/5,  n[1]*width/20+height/2,  n[2]*width/20+width/5,  n[3]*width/20+height/2] for n in circleLines]

masked = canvas.draw_lines(circleLines+
        [[width/5+width/20*cos(-.2),height/2+width/20*sin(-.2),rectLines[0],rectLines[1]],
    [width/5+width/20*cos(pi+.2),height/2+width/20*sin(pi+.2),rectLines[2],rectLines[1]],
    [width/5+width/20*cos(.9),height/2+width/20*sin(.9),rectLines[0],rectLines[3]],
    [width/5+width/20*cos(pi-.9),height/2+width/20*sin(pi-.9),rectLines[2],rectLines[3]],
    [rectLines[0],rectLines[1],rectLines[2],rectLines[1]],
    [rectLines[2],rectLines[1],rectLines[2],rectLines[3]],
    [rectLines[2],rectLines[3],rectLines[0],rectLines[3]],
    [rectLines[0],rectLines[3],rectLines[0],rectLines[1]],
    ],time=.2,delay=1)

" Distanciation Physique "


lines = [[13*width/40, height/2+width/20, 14*width/40, height/2+width/60],
         [15*width/40, height/2+width/20, 14*width/40, height/2+width/60],
         [14*width/40, height/2-width/60, 14*width/40, height/2+width/60],
         [14*width/40, height/2-width/60, 13*width/40, height/2+width/60],
         [14*width/40, height/2-width/60, 15*width/40, height/2+width/60],

         [17*width/40, height/2+width/20, 18*width/40, height/2+width/60],
         [19*width/40, height/2+width/20, 18*width/40, height/2+width/60],
         [18*width/40, height/2-width/60, 18*width/40, height/2+width/60],
         [18*width/40, height/2-width/60, 17*width/40, height/2+width/60],
         [18*width/40, height/2-width/60, 19*width/40, height/2+width/60]
         ]
bodies = canvas.draw_lines(lines,time=.2)
heads = [canvas.spawn_circle(14*width/40,height/2-2*width/60,width/60,outline='#FFF',time=.1),
canvas.spawn_circle(18*width/40,height/2-2*width/60,width/60,outline='#FFF',time=.1)]
physicalDistance = canvas.draw_lines([
    [16*width/40, height/2, 17*width/40, height/2],
    [16*width/40, height/2, 15*width/40, height/2],
    ],time=.2) + canvas.draw_lines([
    [15*width/40, height/2, 15*width/40+width/100, height/2-width/100],
    [17*width/40, height/2, 17*width/40-width/100, height/2+width/100],
    [15*width/40, height/2, 15*width/40+width/100, height/2+width/100],
    [17*width/40, height/2, 17*width/40-width/100, height/2-width/100],
    ],time=.2,delay=1)

" Gestes barrières "


barrier = canvas.draw_lines([
    [21*width/40, height/2, 27*width/40, height/2],
    [27*width/40, height/2, 27*width/40, height/2-width/60],
    [27*width/40, height/2-width/60, 21*width/40, height/2-width/60],
    [21*width/40, height/2-width/60, 21*width/40, height/2],
    [21*width/40, height/2+width/20, 22*width/40, height/2],
    [27*width/40, height/2+width/20, 26*width/40, height/2],
    ],time=.4)
polygons = [canvas.create_polygon((42+3*n)*width/80,height/2,(44+3*n)*width/80,height/2,(45+3*n)*width/80,height/2-width/60+1,(43+3*n)*width/80,height/2-width/60+1, fill="#000") for n in range(4)]

[canvas.fade(polygon,"#FFF",time=.1) for polygon in polygons]

" Tests "


testRod = canvas.draw_line(35*width/40, height/2-width/20, 30*width/40, height/2+width/30,transition="easeIn",time=.3)
spawnCoords = (30*width/40, height/2+width/30,29*width/40+width/200,height/2+width/20-width/200)
canvas.setFrameRate(800)
testCotton = []
for n in range(100):
    canvas.startFrame()
    testCotton.append(canvas.spawn_circle(
            spawnCoords[0]+n/99*(spawnCoords[2]-spawnCoords[0]),
            spawnCoords[1]+n/99*(spawnCoords[3]-spawnCoords[1]),
            width/200,time=0,fill="#FFF",outline="#FFF"))
    canvas.endFrame()
canvas.setFrameRate(50)
waitUntilSpacePress()

" Disparition masque "
for n in range(30):
    canvas.startFrame()
    [canvas.move(obj,-width/5,-height/2) for obj in masked]
    [canvas.coords(obj, *[c * (30-n)/50 for c in canvas.coords(obj)]) for obj in masked]
    [canvas.move(obj,width/5,height/2) for obj in masked]
    canvas.endFrame()
[canvas.delete(obj) for obj in masked]

" Disparition distanciation physique "
canvas.move_objects(bodies[:5]+[heads[0]],-width,0,mode="relative",transition="easeIn",time=.2)
canvas.move_objects(bodies[5:]+[heads[1]],width,0,mode="relative",transition="easeIn",time=.2)
canvas.move_objects(physicalDistance,0,height,mode="relative",transition="easeIn",time=.3)
[canvas.delete(obj) for obj in bodies+physicalDistance]

" Disparition de la barrière "
for n in range(1,50):
    canvas.startFrame()
    canvas.coords(barrier[4], 22*width/40, height/2, 22*width/40-width/40/n, height/2+width/20/n)
    canvas.coords(barrier[5], 26*width/40, height/2, 26*width/40+width/40/n, height/2+width/20/n)
    [27*width/40, height/2+width/20, 26*width/40, height/2]
    canvas.endFrame()
canvas.delete(barrier[4])
canvas.delete(barrier[5])

for n in range(20):
    canvas.startFrame()
    [canvas.coords(obj,
        canvas.coords(obj)[0] + 0*width/1600,
        canvas.coords(obj)[1],
        canvas.coords(obj)[2] + 3*width/1600,
        canvas.coords(obj)[1],
        canvas.coords(obj)[4] + 2*width/1600,
        canvas.coords(obj)[5],
        canvas.coords(obj)[6] - width/1600,
        canvas.coords(obj)[7]) for obj in polygons]
    canvas.coords(polygons[-1], 
        canvas.coords(polygons[-1])[0],
        canvas.coords(polygons[-1])[1],
        canvas.coords(polygons[-1])[2]-2*width/1600,
        canvas.coords(polygons[-1])[3],
        canvas.coords(polygons[-1])[4]-2*width/1600,
        canvas.coords(polygons[-1])[5],
        canvas.coords(polygons[-1])[6]-0*width/1600,
        canvas.coords(polygons[-1])[7])
    canvas.endFrame()
cover = canvas.create_rectangle(21*width/40,height/2,27*width/40,height/2-width/60,fill="#FFF")
[canvas.delete(obj) for obj in polygons+barrier]
canvas.fade(cover,"#000",time=.3)
canvas.delete(cover)
" Disparition du test "

maskRod = canvas.draw_line(35*width/40, height/2-width/20, 30*width/40, height/2+width/30,transition="easeIn",time=.3,fill="#000")
canvas.delete(testRod)
canvas.delete(maskRod)
for cotton in testCotton:
    canvas.delete(cotton)
    canvas.update()
    sleep(.001)

#######################################################################################################
###-----------------------------------+---------------------------+---------------------------------###
###:::::::::::::::::::::::::::::::::::|         Confinement       |:::::::::::::::::::::::::::::::::###
###-----------------------------------+---------------------------+---------------------------------###
#######################################################################################################
infectionRadius = 9
while True:
    simuWithDeath()

#######################################################################################################
###-----------------------------------+---------------------------+---------------------------------###
###:::::::::::::::::::::::::::::::::::|           Tests           |:::::::::::::::::::::::::::::::::###
###-----------------------------------+---------------------------+---------------------------------###
#######################################################################################################

window.mainloop()
