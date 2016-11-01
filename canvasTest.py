import tkinter as tk
import StarSystem
import Orbitals


LARGE_FONT = ("Verdana", 12)


class SpaceGame(tk.Tk):
    def __init__(self, *args, **kwargs):


        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side = "top", fill="both", expand= True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Visit page 1",
                            command= lambda: controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #If these are not equal, then orbitals need to be an oval
        self.canvasH = 1000
        self.canvasW = 1000


        self.canvas = tk.Canvas(self, height = self.canvasH, width = self.canvasW, bg = "grey")
        self.canvas.pack()

        self.zoomLevel = 1
        self.zoomLevelChange = 0.2

        #Current centre of the system - the star centre upon creation
        self.starX = self.canvasW / 2
        self.starY = self.canvasH / 2

        #The centre of the canvas
        self.centreX = self.starX
        self.centreY = self.starY

        self.zoomOffsetX = 0
        self.zoomOffsetY = 0


        self.starRadius = 25
        self.planetRadius = 5
        self.starTextOffset = 5 + self.starRadius * 1.3
        self.planetTextOffset = 5 + self.planetRadius * 1.3

        self.planetWidgets = []
        self.mySystem = StarSystem.StarSystem(10000000, 25)
        self.mySystem.generate()

        self.planetWidgets = []
        self.planetName = []


        #tkinter stuff related to the class
        button1 = tk.Button(self, text="Update", width = 75,
                command = self.redrawCanvas)
        button1.pack()

        #keybindngs
        self.focus_set()
        self.bind('=', self.keyonCanvas)
        self.bind('-', self.keyonCanvas)
        self.bind('w', self.keyonCanvas)
        self.bind('s', self.keyonCanvas)
        self.bind('a', self.keyonCanvas)
        self.bind('d', self.keyonCanvas)

        self.canvas.bind('<Button-1>', self.focusOnClick)

        self.generateCanvas()


    def focusOnClick(self, event):

        returnedID = self.canvas.find_closest(event.x, event.y, halo = 5)[0]

        if returnedID in self.planetWidgets:


            print(event.x, event.y)
            self.canvas.itemconfig(self.planetName[self.planetWidgets.index(returnedID)], fill="white")


            #exact cordinates of the object on the canvas
            x, y = self.getCircleCoords(returnedID)

            #now the offset are equal to the distance from the star
            self.zoomOffsetX = self.starX - x
            self.zoomOffsetY = self.starY - y

            #Adjust the star to its new position, alloowing the clicked object to the centre
            self.starX = self.centreX + self.zoomOffsetX
            self.starY = self.centreY + self.zoomOffsetY



            self.canvas.delete('all')
            self.generateCanvas()



    def keyonCanvas(self, event):
        if event.char == '-':
            if self.zoomLevel > 0.4:


                print(self.zoomOffsetX)


                self.zoomLevel -= self.zoomLevelChange

                zFactor = (self.zoomLevel - 1) / self.zoomLevelChange

                self.zoomOffsetX -= (1 - 1 / 1.2) * self.zoomOffsetX
                self.zoomOffsetY -= (1 - 1 / 1.2) * self.zoomOffsetY

                self.starX = self.centreX + self.zoomOffsetX
                self.starY = self.centreY + self.zoomOffsetY



        elif event.char == '=':
            self.zoomLevel += self.zoomLevelChange

            # self.zoomOffsetX += (self.zoomLevel - 5) * self.zoomLevelChange
            # self.zoomOffsetY += (self.zoomLevel - 5) * self.zoomLevelChange


            print(self.zoomOffsetX)
            zFactor = (self.zoomLevel - 1) / self.zoomLevelChange

            self.zoomOffsetX *= 1.2
            self.zoomOffsetY *= 1.2

            #selected planet is at centre so offset to star to relative to centre
            self.starX = self.centreX + self.zoomOffsetX
            self.starY = self.centreY + self.zoomOffsetY




        elif event.char == 'w':
            self.starY -= 20
            #self.zoomOffsetY -= 20

        elif event.char == 's':
            self.starY += 20
            #self.zoomOffsetY -= 20

        elif event.char == 'a':
            self.starX -= 20
            #self.zoomOffsetX -= 20

        elif event.char == 'd':
            self.starX += 20
            #self.zoomOffsetX += 20

        self.canvas.delete('all')
        self.generateCanvas()


    def generateCanvas(self):

        self.planetWidgets = []
        self.planetName = []


        for p in self.mySystem.children:

            if isinstance(p, Orbitals.Star):
                applyColor = "yellow"
                radius = self.starRadius
                self.circle(self.starX, self.starY, radius, fill=applyColor)
                self.canvas.create_text(self.starX, self.starY + self.starTextOffset, text=p.name)

            else:
                applyColor = "blue"
                radius = self.planetRadius
                pX, pY = self.getCanvasXY(p)

                #Note - If Canvas is not a square, this needs to be an oval

                orbRadius = (p.orbitalDistance / self.mySystem.maxOrbitalDistance) * self.canvasH
                orbRadius *= ((1 + self.zoomLevelChange) ** ((self.zoomLevel - 1) / self.zoomLevelChange))
                #test

                self.circle(self.starX, self.starY, orbRadius, fill="")

                self.planetWidgets.append(self.circle(pX, pY, radius, fill=applyColor))
                self.planetName.append(self.canvas.create_text(pX, pY + self.planetTextOffset, text=p.name,))



    def circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval( x - r, y - r, x + r, y + r, **kwargs)




    def getCanvasXY(self, obj):
        ''''
        Takes in a StarSystem.Planet object

        Calculate the x and y distances of the planet in terms of the canvas size

        then adjust these to the centre of the star


        :returns

        x and y coordinates for the canvas object
        '''

        x, y = obj.getCoords()


        maxRadius = self.mySystem.maxOrbitalDistance

        #number of times plus or minus on zoom level
        zFactor = (self.zoomLevel - 1) / self.zoomLevelChange
        if zFactor > -1:
            x = ((1 + self.zoomLevelChange) ** zFactor) * ( (x / maxRadius * self.canvasW)) + self.starX
            y = ((1 + self.zoomLevelChange) ** zFactor) * ( (y / maxRadius * self.canvasH)) + self.starY
        else:
            #the number is smaller so 0.8 ** zFactor * -1
            x = ((1 - self.zoomLevelChange) ** (-1 * zFactor) * ( (x / maxRadius * self.canvasW))) + self.starX
            y = ((1 - self.zoomLevelChange) ** (-1 * zFactor) * ( (y / maxRadius * self.canvasH))) + self.starY



        return (x, y)



    def getCircleCoords(self, pObj):
        a = self.canvas.coords(pObj)
        #print(a)
        x = a[0] +  (a[2] - a[0]) / 2
        y = a[1] + (a[3] - a[1]) / 2
        return (x, y)


    def redrawCanvas(self):
        #print(self.planetWidgets)

        self.mySystem.update(80000)


        planetNewCoords = []
        for p in self.mySystem.children:
            if isinstance(p, Orbitals.Planet):
                x , y = self.getCanvasXY(p)

                #These are the newly updated locations
                planetNewCoords.append([x, y])
                #print(x, y)

        #print(self.planetWidgets)
        #print(planetNewCoords)

        #print(self.canvas.coords(self.planetWidgets[i]))
        for i in range(0, len(self.planetWidgets)):
            #Derive old x, y from text displaying name
            oldX, oldY = self.getCircleCoords(self.planetWidgets[i])
            #print (oldX, oldY)
            #print("new - old : " + str(planetNewCoords[j][0]) + " " + str(oldX))

            self.canvas.move(self.planetWidgets[i],
                             planetNewCoords[i][0] - oldX,
                             planetNewCoords[i][1] - oldY)
            self.canvas.move(self.planetName[i],
                             planetNewCoords[i][0] - oldX,
                             planetNewCoords[i][1] - oldY)





app = SpaceGame()
app.mainloop()



# class PCanvas(Canvas):
#     def __init__(self, parent, *args, **kwargs):
#         Canvas.__init__(self, parent)
#         self.height = 1000
#         self.width = 1000
#         self.planetWidgets = []
#         self.mySystem = StarSystem.StarSystem(10000000, 25)
#         self.mySystem.generate()
#
#     def circle(self, x, y, r, **kwargs):
#         return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
#
#     def getCanvasXY(self, obj):
#         x, y = obj.getCoords()
#
#         maxRadius = self.mySystem.maxOrbitalDistance
#         # print("Y from orbitals is " + str(y))
#
#         x = self.width / 2 + (((x / maxRadius) * self.width))
#
#         y = self.height / 2 + ((y / maxRadius) * self.height)
#
#         return (x, y)
#
#
#     def drawCanvas(self):
#         for p in self.mySystem.children:
#
#             if isinstance(p, Orbitals.Star):
#                 applyColor = "yellow"
#                 radius = 25
#                 x, y = self.width / 2, self.height / 2
#             else:
#                 applyColor = "blue"
#                 radius = 5
#                 x, y = self.getCanvasXY(p)
#                 # print(y)
#                 # #offset x to the centre
#                 # x += canvas_width / 2
#                 # y += canvas_height / 2
#                 self.circle(self.width / 2, self.height / 2,
#                                 (p.orbitalDistance / self.mySystem.maxOrbitalDistance) * self.height,
#                                 fill="")
#
#             self.planetWidgets.append(self.circle(x, y, radius, fill=applyColor))
#             self.planetWidgets.append(self.create_text(x, y + 5 + (radius * 1.3), text=p.name))
#
#     def drawCircle(self):
#         self.circle(50,50,25)
#
# root = Tk()
# w = PCanvas(root, height = 1000, width = 1000, bg = "white")
# w.pack()
# #w.drawCanvas()
# w.drawCircle
# mainloop()
