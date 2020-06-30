import globals

o = globals.o
x = globals.x
p = globals.p
d = globals.d

#NOTE: Everything is indexed as y,x and not as x,y !!!
class Screen():
    width: int = 0
    height: int = 0
    
    scrBuffer = None #the 2D list representing the screen

    #where the tile's pivot gets placed when the player gets a new tile
    spawnY = 10
    spawnX = 5

    write = None #function for writing to the device's screen

    def __init__(self, h, w, writeFunc=globals.write1):
        self.width = w
        self.height = h
        self.initScrBuffer(h, w)
        self.write = writeFunc

        #give the screen borders

        #left and right
        for el in self.scrBuffer:
            el[0] = x
            el[self.width-1] = x

        #down
        for xxx in range(0,self.width-1):
            self.scrBuffer[self.height-1][xxx] = x
        pass

    #clear the scrBuffer, but not the walls
    def clearInsideBorders(self):
        for yyy in range(1,self.height-1):
            for xxx in range(1,self.width-1):
                self.scrBuffer[yyy][xxx] = o
        

    def initScrBuffer(self, h, w,):
        self.scrBuffer = self.height*[o]
        for iii in range(0,h):
            self.scrBuffer[iii] = w*[o]

    def printScrBuffer(self):
        for yyy in range(9,len(self.scrBuffer)):
            for xxx in range (0,len(self.scrBuffer[0])):
                self.write(self.scrBuffer[yyy][xxx])
            self.write('\n')

    def clearScr(self):
        globals.clrScr()


    pass
