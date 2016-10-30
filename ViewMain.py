from tkinter import *
import StarSystem
import Orbitals


#class PlanetCanvas

#Adding a member to the canvas class???
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


def getCanvasXY(obj, maxRadius):
    x, y = obj.getCoords()
    #print("Y from orbitals is " + str(y))

    x =canvas_width / 2 +  (((x / maxRadius) * canvas_width))

    y =canvas_height / 2 +   ((y / maxRadius) * canvas_height)

    return(x, y)


mySystem = StarSystem.StarSystem(10000000, 25)
mySystem.generate()

print(type(mySystem.children[0]))


master = Tk()

canvas_width = 1000
canvas_height = 1000


w = Canvas(master,
           width = canvas_width,
           height = canvas_height,
           bg = "white")
w.pack()

x = int(canvas_width / 2)
y = int(canvas_height / 2)

print("maxOrbitalDistance = " + str(mySystem.maxOrbitalDistance))


wObjs = []
for p in mySystem.children:

    if isinstance(p, Orbitals.Star):
        applyColor = "yellow"
        radius = 25
        x, y = canvas_width / 2 , canvas_height / 2
    else:
        applyColor = "blue"
        radius = 5
        x,y = getCanvasXY(p, mySystem.maxOrbitalDistance)
        #print(y)
        # #offset x to the centre
        # x += canvas_width / 2
        # y += canvas_height / 2
        w.create_circle(canvas_width / 2, canvas_height / 2,
                        (p.orbitalDistance / mySystem.maxOrbitalDistance) * canvas_height,
                        fill="")

    wObjs.append(w.create_circle(x, y, radius, fill = applyColor))
    wObjs.append(w.create_text(x, y + 5 + (radius * 1.3), text = p.name))

def redrawCanvas():
    global w
    update_canvas(w)
def update_canvas(w):
    global wObjs, x, y
    for ob in wObjs:
        w.move(ob, 10, 0)





counter = 0



# def drawCanvas():
#     global counter, w
#     mySystem.update(counter)
#     counter += 500000
#     print("This is the counter :" + str(counter))
#     counterCanvas(w)
#
#counterCanvas(w)
button = Button(master, text="Update", width = 75,
                command = redrawCanvas)
button.pack()
mainloop()

