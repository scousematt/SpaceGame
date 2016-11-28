class Zoom:

    def __init__(self, defaultLevel, change, centreX, centreY):
        self.level = self.default = defaultLevel
        self.change = change
        self.offsetX = 0
        self.offsetY = 0
        self.centreX = centreX
        self.centreY = centreY

    def adjustZoomLevel(self, toLevel):
        x = y = 0
        if self.level < toLevel:
           x, y =  self.zoomLevelUp((toLevel - self.level))
        elif self.level > toLevel:
           x, y =  self.zoomLevelDown((self.level - toLevel))
        self.level = toLevel
        return (x, y)


    def resetZoom(self):
        self.level = self.default

    def getZoomLevelText(self):
        return ('Zoom: ' + str(round(self.level / self.change) - 5))

    def canvasXYZoom(self):
        return (1 + self.change) ** ((self.level - 1) / self.change)

    def zoomLevelUp(self, times):
        i = 0
        while i < int(round(times / self.change)):
            self.offsetX *= 1 + self.change
            self.offsetY *= 1 + self.change
            i += 1
        starX = self.centreX + self.offsetX
        starY = self.centreY + self.offsetY
        return (starX, starY)



    def zoomLevelDown(self, times):
        i = 0
        while i < int(round(times / self.change)):
            self.offsetX -= (1 - 1 / (1 + self.change)) * self.offsetX
            self.offsetY -= (1 - 1 / (1 + self.change)) * self.offsetY
            i += 1
        starX = self.centreX + self.offsetX
        starY = self.centreY + self.offsetY
        return (starX, starY)