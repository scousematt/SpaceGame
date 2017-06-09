import tkinter as tk
import tkinter.ttk as ttk

import math

import Orbitals
import canvasMain
import CanvasZoom
import game


import StarSystem



LARGE_FONT = ("Verdana", 12)


# class SpaceGame(tk.Tk):
#
#     def __init__(self, game, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         self.game = game
#
#         container = tk.Frame(self)
#
#         container.pack(side = "top", fill="both", expand= True)
#
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight = 1)
#
#         self.frames = {}
#         for F in (StartPage, PageOne):
#             frame = F(container, self)
#             self.frames[F] = frame
#             frame.grid(row = 0, column=0, sticky="nsew")
#         self.show_frame(StartPage)
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()
#
#
#
# class StartPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Start Page", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#
#         button1 = tk.Button(self, text="Visit page 1",
#                             command=lambda: controller.show_frame(PageOne))
#         button1.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #import game object which includes all game informati

         # If these are not equal, then orbitals need to be an oval
        self.canvasH = 750
        self.canvasW = 750
        # Left Canvas is the planetary treeview
        self.leftCanvas = tk.Canvas(self, height=self.canvasH, width=6, bg='white')
        self.leftCanvas.pack(side=tk.LEFT, expand=1, fill=tk.Y)
        self.tree = ttk.Treeview(self.leftCanvas, columns=('Systems'), height=100)
        # Shows the planet and ships n stuff
        self.canvas = tk.Canvas(self, height=self.canvasH, width=self.canvasW, bg='grey')
        self.canvas.pack(side=tk.LEFT)

        # # Current centre of the system - the star centre upon creation
        self.starX = self.canvasW / 2
        self.starY = self.canvasH / 2
        # The centre of the canvas
        self.centreX = self.starX
        self.centreY = self.starY
        self.cz = CanvasZoom.Zoom(1, 0.2, self.centreX, self.centreY)

        self.starRadius = 25
        self.planetRadius = 5
        self.moonRadius = 3
        self.starTextOffset = 5 + self.starRadius * 1.3
        self.planetTextOffset = 5 + self.planetRadius * 1.3

        # Generate the galaxy here, TODO need to move this to a main at some point
        # self.galaxy = Galaxy.Galaxy()
        # self.current_system = self.galaxy.systems[0]

        self.planetWidgets = []
        self.planetName = []

        #tkinter stuff related to the class
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

        self.lastItemOnTreeview = ":".join(("STAR", game.current_system.name))
        self.createTreeviewSystemData(game.current_system, self.lastItemOnTreeview)
        self.treeview.item(self.lastItemOnTreeview, open=True)

        self.generateCanvas()

        ###############################################################
        #
        # GUI

        button1 = tk.Button(self, text="Main Menu",
                            command=lambda: controller.show_frame(canvasMain.StartPage))
        button1.pack()


        print('after generatecanvas')

    def mouseFocus(self, event):
        # print("Mouse focus")
        event.widget.focus_set()

    def generateLeftCanvas(self):
        self.tree.grid(row=2, sticky='nsew')

        # add data
        self.treeview = self.tree
        self.treeview.column('#0', width=210)
        self.treeview.column('#1', width=30)

        self.treeview.bind('<Double-1>', self.doubleClickTreeview)
        '''
        Galaxy - StarSystem - children[myStar, planet1, planet2]
        '''
        self.treeview.insert('', 'end', 'ROOT:Systems', text='Systems', open=True)
        # Populate the tree with systems
        #for i in range(0, len(game.game.galaxy.systems)):
        for system in game.galaxy.systems:
            self.treeview.insert('ROOT:Systems', 'end',
                                 ":".join(("STAR", system.name)),
                                 text=system.name)

    def doubleClickTreeview(self, event):
        #itemID is the tree id
        itemID = self.tree.identify('item', event.x, event.y)
        itemType, name = itemID.split(':')
        idOfCanvasObj = ''
        # Doubleclick on the treeview root, ie: 'root'
        if itemType == 'ROOT':
            return
        if itemType == 'STAR':
            self.cz.level = 1
            self.starX = self.centreX = self.canvasW / 2
            self.starY = self.centreY = self.canvasH / 2
            # self.zoomOffsetX = self.zoomOffsetY = 0

            game.current_system = game.galaxy.systems[game.galaxy.systemNames.index(name)]
            self.treeview.item(self.lastItemOnTreeview, open=0)
            self.treeview.item(itemID, open=True)
            self.lastItemOnTreeview = itemID
             # If no system has been generated, generate it.
            if len(game.current_system.children) == 0:
                self.createTreeviewSystemData(game.current_system, itemID)
            self.cz.resetZoom()
            childrenList = []
            childrenList = self.treeview.get_children(itemID)
            print(childrenList)
            #self.treeview.see(childrenList[0])
            print(itemID, self.treeview.item(itemID, 'open'), self.lastItemOnTreeview)
            self.generateCanvas()
            return
        if itemType == 'PLANET':
            #nameList = self.current_system.getPlanetNames()
            #print(self.planetName[name], self.planetWidgets.index(self.planetName[name]-1))
            #print(self.planetWidgets)
            self.cz.adjustZoomLevel(4)
            #Wasteful do I need to break up generate Canvas so I dont draw to the canvas?
            self.generateCanvas()

            idOfCanvasObj =  self.planetWidgets[self.planetWidgets.index(self.planetName[name]-1)]
        if itemType == 'MOON':
            '''
            Need to zoom in and centre on the moons parent
            Need to cycle through self.current_system until
            '''
            #There should be only one moon with a given name
            moon = [i for i in game.current_system.children if i.name == name]
            self.cz.adjustZoomLevel(10)
            self.generateCanvas()
            idOfCanvasObj = self.planetWidgets[self.planetWidgets.index(self.planetName[moon[0].name]-1)]
        if  [item for item in self.canvas.find_all() if idOfCanvasObj == item] == []:
            #Should this be an isExistsCanvasID(Canvas, ID)   ?

            #need to zoom in more
            self.cz.adjustZoomLevel(18)
            self.generateCanvas()
            #centre the canvas on the object for its parent (planet/ moon)
        self.centreOnPlanet(idOfCanvasObj)


    def createTreeviewSystemData(self, system, itemID):
        '''

        :param system: the system from self.current_system
        :param itemID: The last item inserted into the Treeview - used as the parent
        :return:
        '''
        system.generate()
        textType = ''
        parent = tempID =  ''
        #for j in range(1, len(self.current_system.children)):
        for body in game.current_system.children:
            if isinstance(body, Orbitals.Planet):
                textType = 'PLANET'
                parent = itemID
            elif isinstance(body, Orbitals.Moon):
                textType = 'MOON'
                if parent == itemID:
                    parent = tempID
            tempID = self.treeview.insert(parent, 'end',
                                        ":".join((textType, body.name)),
                                        text=body.name)


    def focusOnClickedObject(self, event):
        '''
        Processes a mouse click. Currently it only reacts to clicking on a planet
        In the future we can left click on the star, or ships, or setting waypoints and stuff
        :param event:
        :return:
        '''
        self.focus_set()
        returnedID = self.canvas.find_closest(event.x, event.y, halo=1)[0]
        print(returnedID)
        if returnedID in self.planetWidgets:
            self.centreOnPlanet(returnedID)

    def centreOnPlanet(self, returnedID):
        # exact coordinates of the object on the canvas
        x, y = self.getCircleCoords(returnedID)
        # now the offset are equal to the distance from the star
        self.cz.offsetX = self.starX - x
        self.cz.offsetY = self.starY - y
        # Adjust the star to its new position, allowing the clicked object to the centre
        self.starX = self.centreX + self.cz.offsetX
        self.starY = self.centreY + self.cz.offsetY
        self.generateCanvas()


    def keyonCanvas(self, event):
        # self.canvas.focus_set()
        if event.char == '-':
            # Check that we are at the minimum zoom level or above
            if self.cz.level > 1:
                self.cz.level -= self.cz.change
                self.starX, self.starY = self.cz.zoomLevelDown(self.cz.change)

        elif event.char == '=':
            self.cz.level += self.cz.change
            self.starX, self.starY = self.cz.zoomLevelUp(self.cz.change)
            # selected planet is at centre so offset to star to relative to centre

        elif event.char == 'w':
            self.starY += 20
            self.cz.offsetY += 20
        elif event.char == 's':
            self.starY -= 20
            self.cz.offsetY -= 20
        elif event.char == 'a':
            self.starX += 20
            self.cz.offsetX += 20
        elif event.char == 'd':
            self.starX -= 20
            self.cz.offsetX -= 20
        self.generateCanvas()

    def generateCanvas(self):

        #TODO check to see what the radius is for the circle we are drawing as the orbital path and if it is
        #too big replace it with a tangent
        self.canvas.delete('all')
        self.planetWidgets = []
        self.planetName = {}
        for p in game.current_system.children:
            if isinstance(p, Orbitals.Star):
                applyColor = game.current_system.get_star_color()
                radius = self.starRadius
                self.planetWidgets.append(self.circle(self.starX, self.starY,0,0, radius, fill=applyColor))
                self.planetName[p.name] = self.canvas.create_text(self.starX, self.starY + self.starTextOffset, text=p.name)
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
        self.canvas.create_text(30, self.canvasH - 50, text=self.cz.getZoomLevelText())

    def drawPlanetsAndMoon(self, centreX, centreY, orbDistance, parentRadius, radius, applyColor, x, y, name):
        orbRadius = (orbDistance / game.current_system.maxOrbitalDistance) * self.canvasH
        orbRadius *= (1 + self.cz.change) ** ((self.cz.level - 1) / self.cz.change)
        if orbRadius - 5 > parentRadius:
            #Draws Orbital Path if not too close to the parent
            self.circle(centreX, centreY,0,0, orbRadius, fill="")
            #Draws blue blob to show planet
            self.planetWidgets.append(self.circle(x, y, centreX, centreY, radius, fill=applyColor))
            self.planetName[name] = self.canvas.create_text(x, y + self.planetTextOffset, text = name)
        else:
            self.planetWidgets.append(self.circle(x, y, centreX, centreY, radius, fill=applyColor, tags="deleteme"))
            self.planetName[name] = self.canvas.create_text(x, y + self.planetTextOffset, text = name, tags="deleteme")
            self.canvas.delete('deleteme')


    def circle(self, centre_x, centre_y, circ_x, circ_y,  r, **kwargs):
        '''

        :param centre_x: centre of the circle
        :param centre_y:
        :param circ_x:
        :param circ_y:
        :param r: radius
        :param kwargs:
        :return: If the radius is less than an amount - there are errors when zoomed in, so there are
        times when a line will be drawn
        '''
        if  r > 500:    #fill == '' means drawing orbital path, Arbitary radius
            #Return a line
            x = centre_x - circ_x
            y = centre_y - circ_y
            angle = math.radians(90 - math.acos(y/x))
            #Lets make the canvas 1000 - worst case scenario
            dx = math.sin(angle) * 1000
            dy = math.cos(angle) * 1000

            #Need the angle from the vertical to the centre
            #90 - above
            return self.canvas.create_line(centre_x,centre_y,centre_x - dx,centre_y - dy)
        else:
            return self.canvas.create_oval(centre_x - r, centre_y - r, centre_x + r, centre_y + r, **kwargs)

    def getCanvasXY(self, obj):
        ''''
        Takes in a StarSystem.Planet object
        Calculate the x and y distances of the planet in terms of the canvas size
        then adjust these to the centre of the star
        :returns
        x and y coordinates for the canvas object
        '''
        x, y = obj.getCoords()
        maxRadius = game.current_system.maxOrbitalDistance
        # number of times plus or minus on zoom level
        x = (self.cz.canvasXYZoom()) * ((x / maxRadius * self.canvasW)) + self.starX
        y = (self.cz.canvasXYZoom()) * ((y / maxRadius * self.canvasH)) + self.starY
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
        '''Throws time at the system and moves all planetary bodies accordingly'''
        game.update_time(80000)
        self.generateCanvas()



