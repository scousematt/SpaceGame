import tkinter as tk
import tkinter.ttk as ttk
import Orbitals
import Galaxy
import StarSystem


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # If these are not equal, then orbitals need to be an oval
        self.canvasH = 1000
        self.canvasW = 1000
        # Left Canvas is the planetary treeview
        self.leftCanvas = tk.Canvas(self, height=self.canvasH, width=100, bg='white')
        self.leftCanvas.pack(side=tk.LEFT, expand=1, fill=tk.Y)
        self.tree = ttk.Treeview(self.leftCanvas, columns=('Systems'), height=100)
        # Shows the planet and ships n stuff
        self.canvas = tk.Canvas(self, height=self.canvasH, width=self.canvasW, bg='grey')
        self.canvas.pack(side=tk.LEFT)
        self.zoomLevelDefault = 1
        self.zoomLevel = 1
        self.zoomLevelChange = 0.2
        # Current centre of the system - the star centre upon creation
        self.starX = self.canvasW / 2
        self.starY = self.canvasH / 2
        # The centre of the canvas
        self.centreX = self.starX
        self.centreY = self.starY

        self.zoomOffsetX = 0
        self.zoomOffsetY = 0

        self.starRadius = 25
        self.planetRadius = 5
        self.moonRadius = 3
        self.starTextOffset = 5 + self.starRadius * 1.3
        self.planetTextOffset = 5 + self.planetRadius * 1.3

        self.planetWidgets = []

        # Generate the galaxy here, TODO need to move this to a main at some point
        self.galaxy = Galaxy.Galaxy()
        self.mySystem = self.galaxy.systems[0]

        self.planetWidgets = []
        self.planetName = []

        # tkinter stuff related to the class
        button1 = tk.Button(self, text="Update", width=75,
                            command=self.redrawCanvas)
        button1.pack(side=tk.BOTTOM)

        # keybindngs
        self.bind('=', self.keyonCanvas)
        self.bind('-', self.keyonCanvas)
        self.bind('w', self.keyonCanvas)
        self.bind('s', self.keyonCanvas)
        self.bind('a', self.keyonCanvas)
        self.bind('d', self.keyonCanvas)
        # Mouse button events
        self.canvas.bind('<Button-1>', self.focusOnClickedObject)
        self.bind('<Enter>', self.mouseFocus)
        # Generate Widgets
        self.generateLeftCanvas()
        self.lastItemOnTreeview = ":".join(("STAR", self.galaxy.systems[0].name))
        self.createTreeviewSystemData(self.mySystem, self.lastItemOnTreeview)
        self.treeview.item(self.lastItemOnTreeview, open=True)

        self.generateCanvas()

    def mouseFocus(self, event):
        # print("Mouse focus")
        event.widget.focus_set()

    def generateLeftCanvas(self):
        self.tree.grid(row=2, sticky='nsew')

        # add data
        self.treeview = self.tree

        self.treeview.bind('<Double-1>', self.doubleClickTreeview)
        '''
        Galaxy - StarSystem - children[myStar, planet1, planet2]
        '''
        self.treeview.insert('', 'end', 'ROOT:Systems', text='Systems', open=True)
        # Populate the tree with systems
        for i in range(0, len(self.galaxy.systems)):
            self.treeview.insert('ROOT:Systems', 'end',
                                 ":".join(("STAR", self.galaxy.systems[i].name)),
                                 text=self.galaxy.systems[i].name)

    def doubleClickTreeview(self, event):

        # self.focus_set()

        # for s in self.treeview.get_children():
        #     self.treeview.item(s, open=False)

        itemID = self.tree.identify('item', event.x, event.y)
        itemType, name = itemID.split(':')

        #self.treeview.focus(itemID)

        # Doubleclick on the treeview root, ie: 'root'
        if itemType == 'ROOT':
            return
        if itemType == 'STAR':
            self.starX = self.centreX = self.canvasW / 2
            self.starY = self.centreY = self.canvasH / 2
            self.zoomOffsetX = self.zoomOffsetY = 0
            self.mySystem = self.galaxy.systems[self.galaxy.systemNames.index(name)]
            self.treeview.item(self.lastItemOnTreeview, open=0)
            self.treeview.item(itemID, open=True)
            self.lastItemOnTreeview = itemID
             # If no system has been generated, generate it.
            if len(self.mySystem.children) == 0:
                self.createTreeviewSystemData(self.mySystem, itemID)
            self.zoomLevel = self.zoomLevelDefault
            childrenList = []
            childrenList = self.treeview.get_children(itemID)
            print(childrenList)
            #self.treeview.see(childrenList[0])
            print(itemID, self.treeview.item(itemID, 'open'), self.lastItemOnTreeview)
            self.generateCanvas()
            return
        if itemType == 'PLANET':
            nameList = self.mySystem.getPlanetNames()
            self.centreOnPlanet(self.planetWidgets[nameList.index(name)])


    def createTreeviewSystemData(self, system, itemID):
        system.generate()
        for j in range(1, len(self.mySystem.children)):
            self.treeview.insert(itemID,
                             'end',
                             ":".join(("PLANET", self.mySystem.children[j].name)),
                             text=self.mySystem.children[j].name)

    def focusOnClickedObject(self, event):
        '''
        Processes a mouse click. Currently it only reacts to clicking on a planet
        In the future we can left click on the star, or ships, or setting waypoints and stuff
        :param event:
        :return:
        '''
        self.focus_set()
        returnedID = self.canvas.find_closest(event.x, event.y, halo=1)[0]
        if returnedID in self.planetWidgets:
            self.centreOnPlanet(returnedID)

    def centreOnPlanet(self, returnedID):
        # exact cordinates of the object on the canvas
        x, y = self.getCircleCoords(returnedID)
        # now the offset are equal to the distance from the star
        self.zoomOffsetX = self.starX - x
        self.zoomOffsetY = self.starY - y
        # Adjust the star to its new position, alloowing the clicked object to the centre
        self.starX = self.centreX + self.zoomOffsetX
        self.starY = self.centreY + self.zoomOffsetY
        self.generateCanvas()

    def keyonCanvas(self, event):
        # self.canvas.focus_set()
        if event.char == '-':
            # Check that we are at the minimum zoom level or above
            if self.zoomLevel > 1:
                self.zoomLevel -= self.zoomLevelChange
                self.zoomOffsetX -= (1 - 1 / 1.2) * self.zoomOffsetX
                self.zoomOffsetY -= (1 - 1 / 1.2) * self.zoomOffsetY
                self.starX = self.centreX + self.zoomOffsetX
                self.starY = self.centreY + self.zoomOffsetY
        elif event.char == '=':
            self.zoomLevel += self.zoomLevelChange
            self.zoomOffsetX *= 1.2
            self.zoomOffsetY *= 1.2
            # selected planet is at centre so offset to star to relative to centre
            self.starX = self.centreX + self.zoomOffsetX
            self.starY = self.centreY + self.zoomOffsetY
        elif event.char == 'w':
            self.starY += 20
            self.zoomOffsetY += 20
        elif event.char == 's':
            self.starY -= 20
            self.zoomOffsetY -= 20
        elif event.char == 'a':
            self.starX += 20
            self.zoomOffsetX += 20
        elif event.char == 'd':
            self.starX -= 20
            self.zoomOffsetX -= 20
        self.generateCanvas()

    def generateCanvas(self):
        self.canvas.delete('all')
        self.planetWidgets = []
        self.planetName = []
        for p in self.mySystem.children:
            if isinstance(p, Orbitals.Star):
                applyColor = self.mySystem.children[0].stellarColor
                radius = self.starRadius
                self.planetWidgets.append(self.circle(self.starX, self.starY, radius, fill=applyColor))
                self.planetName.append(self.canvas.create_text(self.starX, self.starY + self.starTextOffset, text=p.name))
            elif isinstance(p, Orbitals.Planet):
                applyColor = "blue"
                pX, pY = self.getCanvasXY(p)
                self.drawPlanetsAndMoon(self.starX, self.starY,
                                        p.orbitalDistance, self.starRadius, self.planetRadius,
                                        applyColor, pX, pY, p.name)
            elif isinstance(p, Orbitals.Moon):
                applyColor = "blue"
                parentX, parentY = self.getCanvasXY(p.planet_orbited)
                pX, pY = self.getCanvasXY(p)
                pX += parentX - self.starX
                pY += parentY - self.starY
                self.drawPlanetsAndMoon(parentX, parentY, p.orbitalDistance,
                                        self.planetRadius, self.moonRadius, applyColor,
                                        pX, pY, p.name)

    def drawPlanetsAndMoon(self, centreX, centreY, orbDistance, parentRadius, radius, applyColor, x, y, name):
        orbRadius = (orbDistance / self.mySystem.maxOrbitalDistance) * self.canvasH
        orbRadius *= ((1 + self.zoomLevelChange) ** ((self.zoomLevel - 1) / self.zoomLevelChange))
        if orbRadius - 5 > parentRadius:
            self.circle(centreX, centreY, orbRadius, fill="")
            self.planetWidgets.append(self.circle(x, y, radius, fill=applyColor))
            self.planetName.append(self.canvas.create_text(x, y + self.planetTextOffset, text = name))
        else:
            self.planetWidgets.append(self.circle(x, y, radius, fill=applyColor, tags="deleteme"))
            self.planetName.append(self.canvas.create_text(x, y + self.planetTextOffset, text = name, tags="deleteme"))
            self.canvas.delete('deleteme')


    def circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

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
        # number of times plus or minus on zoom level
        zFactor = (self.zoomLevel - 1) / self.zoomLevelChange
        if zFactor > -1:
            x = ((1 + self.zoomLevelChange) ** zFactor) * ((x / maxRadius * self.canvasW)) + self.starX
            y = ((1 + self.zoomLevelChange) ** zFactor) * ((y / maxRadius * self.canvasH)) + self.starY
        else:
            # the number is smaller so 0.8 ** zFactor * -1
            x = ((1 - self.zoomLevelChange) ** (-1 * zFactor) * ((x / maxRadius * self.canvasW))) + self.starX
            y = ((1 - self.zoomLevelChange) ** (-1 * zFactor) * ((y / maxRadius * self.canvasH))) + self.starY
        return (x, y)

    def getCircleCoords(self, pObj):
        '''
        :param pObj: A circular canvas widget object ID

        Checks to see if the object exists on the canvas as objects close
        to the star are not displayed if they overlap
        :return: The x , y coordinates of the centre of the pObject
        '''
        a = self.canvas.coords(pObj)
        if a == []:
            return False
        x = a[0] + (a[2] - a[0]) / 2
        y = a[1] + (a[3] - a[1]) / 2
        return x, y

    def redrawCanvas(self):
        # Temp: The redraw canvas should be an update method
        self.mySystem.update(80000)
        planetNewCoords = [self.getCanvasXY(p) for p in self.mySystem.children \
                           if isinstance(p, Orbitals.Planet)]

        for i in range(0, len(self.planetWidgets)):
            coords = self.getCircleCoords(self.planetWidgets[i])
            #print(str(i) + " " + str(coords) + " " + str(planetNewCoords[i]))
            # Check to see planetWidget exists on canvas
            if coords != False:
                self.canvas.move(self.planetWidgets[i],
                                 planetNewCoords[i][0] - coords[0],
                                 planetNewCoords[i][1] - coords[1])
                self.canvas.move(self.planetName[i],
                                 planetNewCoords[i][0] - coords[0],
                                 planetNewCoords[i][1] - coords[1])