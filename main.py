import game
import canvasMain
import Galaxy as galaxy
import ship


#Initialising project variables within game.py
game.galaxy = galaxy.Galaxy()
game.current_system = game.galaxy.systems[0]


#temporary hack
game.galaxy.systems[0].ships.append(ship.Vessel('Witch', 1000000, 100))

app = canvasMain.SpaceGame()
app.mainloop()