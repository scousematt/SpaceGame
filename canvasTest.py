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

        self.canvasH = 1000
        self.canvasW = 1000
        self.canvas = tk.Canvas(self, height = self.canvasH, width = self.canvasW, bg = "grey")
        self.canvas.pack()

        self.zoomLevel = 1
        self.zoomLevelChange = 0.2
        self.x = self.canvasW / 2
        self.y = self.canvasH / 2


        self.centreX = self.x
        self.centreY = self.y


        self.starRadius = 25
        self.planetRadius = 5
        self.starTextOffset = 5 + self.starRadius * 1.3
        self.planetTextOffset = 5 + self.planetRadius * 1.3

        self.planetWidgets = []
        self.mySystem = StarSystem.StarSystem(10000000, 25)
        self.mySystem.generate()

        self.planetWidgets = []
        self.planetOrbits = []


        #tkinter stuff related to the class
        button1 = tk.Button(self, text="Update", width = 75,
                command = self.redrawCanvas)
        button1.pack()

        #keybindngs
        self.focus_set()
        self.bind('=', self.zoomCanvas)
        self.bind('-', self.zoomCanvas)
        self.bind('w', self.moveCanvas)
        self.bind('s', self.moveCanvas)
        self.bind('a', self.moveCanvas)
        self.bind('d', self.moveCanvas)

        self.generateCanvas()



    def zoomCanvas(self, event):
        if event.char == '-':
            self.zoomLevel -= self.zoomLevelChange
        else:
            self.zoomLevel += self.zoomLevelChange
        self.canvas.delete('all')
        self.generateCanvas()

    def moveCanvas(self, event):
        print(event.char)

    def generateCanvas(self):
        for p in self.mySystem.children:

            if isinstance(p, Orbitals.Star):
                applyColor = "yellow"
                radius = self.starRadius
                self.circle(self.centreX, self.centreY, radius, fill=applyColor)
                self.canvas.create_text(self.x, self.y + self.starTextOffset, text=p.name)


                #Assuming first item is star? self.x, y are already set
                #x, y = self.width / 2, self.height / 2
            else:
                applyColor = "blue"
                radius = self.planetRadius
                self.x, self.y = self.getCanvasXY(p)
                # print(y)
                # #offset x to the centre
                # x += canvas_width / 2
                # y += canvas_height / 2

                #Draw orbits
                self.circle(self.centreX, self.centreY,
                                (p.orbitalDistance / self.mySystem.maxOrbitalDistance)\
                             * self.canvasH * self.zoomLevel,
                                fill="")

                self.planetWidgets.append(self.circle(self.x, self.y, radius, fill=applyColor))
                self.planetWidgets.append(self.canvas.create_text(self.x,
                                                                  self.y + self.planetTextOffset,
                                                                  text=p.name))



    def circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval( x - r, y - r, x + r, y + r, **kwargs)




    def getCanvasXY(self, obj):
        ''''
        Converts the angle and radius of the planets location into
        a form that fits inside the canvas.

        Adjusts to the centre of the canvas and returns x,y suited to the canvas
        '''
        x, y = obj.getCoords()

        maxRadius = self.mySystem.maxOrbitalDistance
        # print("Y from orbitals is " + str(y))

        x = self.zoomLevel * (self.canvasW / 2 + (((x / maxRadius) * self.canvasW)) )

        y = self.zoomLevel * (self.canvasH / 2 + ((y / maxRadius) * self.canvasH))

        return (x, y)



    def getCircleCoords(self, pObj):
        a = self.canvas.coords(pObj)
        #print(a)
        x = a[0] +  (a[2] - a[0]) / 2
        y = a[1] + (a[3] - a[1]) / 2
        return (x, y)

    def redrawCanvas(self):
        #print(self.planetWidgets)

        self.mySystem.update(800000)


        planetNewCoords = []
        for p in self.mySystem.children:
            if isinstance(p, Orbitals.Planet):
                x , y = self.getCanvasXY(p)

                #These are the newly updated locations
                planetNewCoords.append([x, y])
                #print(x, y)

        #print(self.planetWidgets)
        #print(planetNewCoords)
        j = 0
        #print(self.canvas.coords(self.planetWidgets[i]))
        for i in range(0, len(self.planetWidgets), 2):
            #Derive old x, y from text displaying name
            oldX, oldY = self.getCircleCoords(self.planetWidgets[i])
            #print (oldX, oldY)
            #print("new - old : " + str(planetNewCoords[j][0]) + " " + str(oldX))

            self.canvas.move(self.planetWidgets[i],
                             planetNewCoords[j][0] - oldX,
                             planetNewCoords[j][1] - oldY)
            self.canvas.move(self.planetWidgets[i+1],
                             planetNewCoords[j][0] - oldX,
                             planetNewCoords[j][1] - oldY)
            j += 1




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
