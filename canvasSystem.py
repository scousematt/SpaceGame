import tkinter as tk
import tkinter.ttk as ttk

import math

import Orbitals
import canvasMain
import canvasMenu
import CanvasZoom
import game


import StarSystem



LARGE_FONT = ("Verdana", 12)

class PageOne(canvasMenu.GameFrame):

    def __init__(self, parent, controller):
        canvasMenu.GameFrame.__init__(self, parent, controller)

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




    def doubleclick_on_star(self, treeview_item):
        self.cz.level = 1
        self.starX = self.centreX = self.canvasW / 2
        self.starY = self.centreY = self.canvasH / 2
        # self.zoomOffsetX = self.zoomOffsetY = 0

        game.current_system = game.galaxy.systems[game.galaxy.systemNames.index(star_name)]
        self.treeview.item(self.lastItemOnTreeview, open=0)
        self.treeview.item(itemID, open=True)
        self.lastItemOnTreeview = itemID
        # If no system has been generated, generate it.
        if len(game.current_system.children) == 0:
            self.createTreeviewSystemData(game.current_system, itemID)
        self.cz.resetZoom()
        # childrenList = []
        childrenList = self.treeview.get_children(itemID)
        # print(childrenList)
        # self.treeview.see(childrenList[0])
        # print(itemID, self.treeview.item(itemID, 'open'), self.lastItemOnTreeview)
        self.generateCanvas()

    def doubleClickTreeview(self, event):
        #itemID is the tree id

        '''

        :param event:
        :return:
        '''
        #TODO clicking on any part of a tree should change to that system
        '''


        This produces
        'STAR: Rigel'
        'PLANET: Rigel i'
        'MOON: Rigel i A'
        '''
        itemID = self.tree.identify('item', event.x, event.y)
        itemType, item_name = itemID.split(':')

        parent_id = self.tree.parent(itemID)
        parent_type, parent_name = parent_id.split(':')

        while parent_type != 'STAR' and parent_type != 'ROOT':
            parent_id = self.tree.parent(parent_id)
            parent_type, parent_name = parent_id.split(':')
        if itemType == 'STAR':
            parent_name = item_name
        # Need something like:
        # if game.galaxy.systems[game.current_system].name != parent_name: generate_canvas(parent_name)
        if game.current_system.name != parent_name:
            #We are clicking on a planet not in the current displayed system
            print(parent_name + ' clicked while showing ' + game.current_system.name)
            itemType = 'STAR'
            item_name = parent_name
            #game.current_system = game.galaxy.systems[game.galaxy.systemNames.index(parent_name)]


        id_of_canvas_obj = '' # Not sure what this is doing yet
        # Doubleclick on the treeview root, ie: 'root'
        if itemType == 'ROOT':
            return

        # Doubleclick on the star name
        if itemType == 'STAR':

            self.cz.level = 1
            self.starX = self.centreX = self.canvasW / 2
            self.starY = self.centreY = self.canvasH / 2
            # self.zoomOffsetX = self.zoomOffsetY = 0

            game.current_system = game.galaxy.systems[game.galaxy.systemNames.index(item_name)]
            self.treeview.item(self.lastItemOnTreeview, open=0)
            self.treeview.item(itemID, open=True)
            self.lastItemOnTreeview = itemID
             # If no system has been generated, generate it.
            if len(game.current_system.children) == 0:
                self.createTreeviewSystemData(game.current_system, itemID)
            self.cz.resetZoom()
            #childrenList = []
            #childrenList = self.treeview.get_children(itemID)
            #print(childrenList)
            #self.treeview.see(childrenList[0])
            #print(itemID, self.treeview.item(itemID, 'open'), self.lastItemOnTreeview)
            self.generateCanvas()
            return
        if itemType == 'PLANET':
            #nameList = self.current_system.getPlanetNames()
            #print(self.planetName[name], self.planetWidgets.index(self.planetName[name]-1))
            #print(self.planetWidgets)
            self.cz.adjustZoomLevel(4)
            #Wasteful do I need to break up generate Canvas so I dont draw to the canvas?
            self.generateCanvas()

            id_of_canvas_obj =  self.planetWidgets[self.planetWidgets.index(self.planetName[item_name]-1)]
        if itemType == 'MOON':
            # There should be only one moon with a given name but this returns a list of objects with the
            # same name
            moon = [i for i in game.current_system.children if i.name == item_name]
            self.cz.adjustZoomLevel(10)
            self.generateCanvas()
            '''
             This should return the canvasID of the moons parent. Not sure what it's supposed to do but
             currently, the moons are drawn orbiting the star
             moon[0].orbited is the parent object
            self.planetWidgets are the id's of the canvas objects drawn - orbital paths and blue circles
            self.planetNames are the name labels.
            
            We need to set id_of_canvas_obj to be moon[0].orbited.name
            '''
            name_id = self.planetName[moon[0].orbited.name] #This is the next canvas obj after the planet circle
            id_of_canvas_obj = name_id - 1
            

        if  [item for item in self.canvas.find_all() if id_of_canvas_obj == item] == []:
            #Should this be an isExistsCanvasID(Canvas, ID)   ?

            #need to zoom in more
            self.cz.adjustZoomLevel(18)
            self.generateCanvas()
            #centre the canvas on the object for its parent (planet/ moon)
        self.centreOnPlanet(id_of_canvas_obj)


    def createTreeviewSystemData(self, system, star_ID):
        '''

        :param system: the system from self.current_system
        :param star_ID: The last item inserted into the Treeview - used as the parent
        :return:
        '''

        system.generate()
        textType = ''
        parent = body_ID = planet_ID =  ''
        body_type = ''
        '''
        Any planets we add to the treeview will go under star_ID,
        we want moons to be placed under the planet so we record each additional entry as body_ID which will become
        the parent for the first moon afterwards
        '''
        for body in game.current_system.children[1:]: # Ignore star as that is already under Systems
            body_type = body.get_class_name() # isinstance returns parent classes for subclassses
            if body_type == 'Planet':
                textType = 'PLANET'
                parent = star_ID  # Under the star
                planet_ID = '' # Reset for any moons around this body
            elif body_type == 'Moon':
                textType = 'MOON'
                if planet_ID == '': # Is this the first moon?
                    planet_ID = body_ID
                parent = planet_ID
            body_ID = self.treeview.insert(parent, 'end',
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
            if p.get_class_name() == 'Star':
                applyColor = game.current_system.get_star_color()
                radius = self.starRadius
                self.planetWidgets.append(self.circle(self.starX, self.starY, radius, fill=applyColor))
                self.planetName[p.name] = self.canvas.create_text(self.starX, self.starY + self.starTextOffset, text=p.name)
            elif p.get_class_name() == 'Planet':
                applyColor = "blue"
                pX, pY = self.getCanvasXY(p)
                self.drawPlanetsAndMoon(self.starX, self.starY,
                                        p.orbitalDistance, self.starRadius, self.planetRadius,
                                        applyColor, pX, pY, p.name)
            elif p.get_class_name() == 'Moon':
                applyColor = "blue"
                parentX, parentY = self.getCanvasXY(p.orbited)
                pX, pY = self.getCanvasXY(p)
                pX += parentX - self.starX
                pY += parentY - self.starY
                self.drawPlanetsAndMoon(parentX, parentY, p.orbitalDistance,
                                        self.planetRadius, self.moonRadius, applyColor,
                                        pX, pY, p.name)
        self.canvas.create_text(30, self.canvasH - 50, text=self.cz.getZoomLevelText())

    def drawPlanetsAndMoon(self, parent_x, parent_y, orbDistance, parentRadius, radius, applyColor,
                           child_x, child_y, name):
        orb_radius = (orbDistance / game.current_system.maxOrbitalDistance) * self.canvasH
        orb_radius *= (1 + self.cz.change) ** ((self.cz.level - 1) / self.cz.change)
        if orb_radius - 5 > parentRadius:
            #Draws Orbital Path if not too close to the parent
            #If we zoom in too far then the path is placed in the wrong place, so replace with a line if radius too big
            if orb_radius > 15000:
                #draw a tangent through child_x square to line to parent_x
                self.draw_tangent(parent_x, parent_y, child_x, child_y)
            else:
                self.circle(parent_x, parent_y, orb_radius, fill="")
            #Draws blue blob to show planet
            self.planetWidgets.append(self.circle(child_x, child_y, radius, fill=applyColor))
            self.planetName[name] = self.canvas.create_text(child_x, child_y + self.planetTextOffset, text = name)
        else:
            self.planetWidgets.append(self.circle(child_x, child_y, radius, fill=applyColor, tags="deleteme"))
            self.planetName[name] = self.canvas.create_text(child_x, child_y + self.planetTextOffset, text = name, tags="deleteme")
            self.canvas.delete('deleteme')

    def draw_tangent(self, px, py, cx, cy):
        '''
        x, y   rotate ccw -> -y, x around origin
        :param px:
        :param py:
        :param cx:
        :param cy:
        :return:
        '''

        #Make cx, cy the origin

        size_factor = (px - cx) / self.canvasH - 100
        x, y = (px - cx) / size_factor, (py - cy) / size_factor

        x1, y1 = -y + cx, x + cy
        x2, y2 = y + cx, -x + cy
        return self.canvas.create_line(x1, y1, x2, y2)


    def circle(self, x, y,  r, **kwargs):

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



