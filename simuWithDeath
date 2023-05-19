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
                if random() < lethality:
                    infecteds[character-dRec].die()
                    removeds.append(infecteds[character-dRec])
                else:
                    infecteds[character-dRec].heal()
                    recovereds.append(infecteds[character-dRec])
                infecteds.pop(character-dRec)
                dRec += 1

            else:
                infecteds[character-dRec].move()
                infecteds[character-dRec].pulse(character)
        for recovered in range(len(recovereds)):
            recovereds[recovered-dRei].move()
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
                    height/10+deltaTime*(point+1),        height/10 + graphHeight/128*(history[p1][1]+history[((point+1)*len(history))//200][2]),
                    height/10+deltaTime*point,            height/10 + graphHeight/128*(history[p2][1]+history[(point*len(history))//200][2]),fill="#0F0",outline='#0F0'))
            graph.append(canvas.create_polygon(height/10+deltaTime*point,            height/10,
                    height/10+deltaTime*(point+1),        height/10,
                    height/10+deltaTime*(point+1),        height/10 + graphHeight/128*history[p1][2],
                    height/10+deltaTime*point,            height/10 + graphHeight/128*history[p2][2],fill="#333",outline='#333'))
        if 'c' in keysPressed:
            moveSpeed = 0.1
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
        canvas.itemconfig(D,text='Décédé     :'+str(len(removeds)))
        canvas.itemconfig(G,text='Guéri      :'+str(len(recovereds)))
        canvas.endFrame()
[canvas.itemconfig(obj,state="hidden") for obj in [*box,*sir,S,I,D,G,graphRectangle]]

