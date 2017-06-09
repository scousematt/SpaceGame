import game
import canvasMain
import Galaxy as galaxy


#Initialising project variables within game.py
game.galaxy = galaxy.Galaxy()
game.current_system = game.galaxy.systems[0]

app = canvasMain.SpaceGame()
app.mainloop()