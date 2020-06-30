'''this class is a bit of a mess, since it has a lot of stuff going on'''


from random import randint
from time import sleep, perf_counter
from msvcrt import getwch, getwche, kbhit
import globals
import cl_screen
import cl_tile

x = globals.x
o = globals.o
p = globals.p
d = globals.d

class Player():
    name: str

    scrX = 0 #pivot x in the screen buffer
    scrY = 0 #pivot y -||-

    y = 0 #the actual y value: cca between 0 and scrHeight * precision

    #in cells per second
    fallSpeed = 1 #can be 0 aswell.
    actualFallSpeed = 1 #is the fallspeed which, in a future update, will
                        #get incremented. fallSpeed will normally becomes
                        #this, unless set to 0 due to a gameOver or other
                        #lazy hack
    initialFallSpeed = 1 
    
    assignedScr: cl_screen.Screen(0,0) #the screen buffer
    assignedTile: cl_tile.Tile([x],[p],[x]) #currently controlled tile
    assignedScr = None
    assignedTile = None

    isColliding = False

    tileList = None

    doScrUpdate = True

    score = 0

    def __init__(self, nam="NoName", scr=None, tLst=None):
        self.setName(nam)
        self.assignedScr = scr
        self.tileList = tLst
        self.fallSpeed = self.initialFallSpeed
        if scr==None:
            errMsg = "No screen component attached to player: "
            errMsg += self.name
            globals.sequentialWrite1(errMsg)

        self.assignTile(self.tileList[randint(0,len(self.tileList)-1)])
        self.assignedTile.rotate(0)

    def setName(self, n: str):
        n = n[slice(globals.nameLength)]
        n += (globals.nameLength-len(n)) * "_"
        self.name = n

    def setFallSpeed(self, i):
        self.fallSpeed = i

    def assignTile(self, t):
        self.assignedTile = t
        self.setTileDefaults()

    def assignRandTile(self):
        self.assignTile(self.tileList[randint(0,len(self.tileList)-1)])

    def setTileDefaults(self):
        self.scrY = self.assignedScr.spawnY
        self.scrX = self.assignedScr.spawnX
        self.y = self.scrY * globals.precision

        self.assignedTile.rotation = 0
        self.assignedTile.rotate(self.assignedTile.rotation)

    #convert y (e.g. 1 500 000 to scrY: 1)
    def y2scrY(self): 
        self.scrY = self.y // globals.precision
        #y gets updated in main
        

    #executes func for each cell of the rotTile positioned in the scrBuffer
    def loopScrTile(self, func):
        self.assignedTile.findRotTilePivot()
        
        for yyy in range(0,len(self.assignedTile.rotTile)):
            for xxx in range(0,len(self.assignedTile.rotTile[0])):
                
                xOffFromPiv = xxx - self.assignedTile.rPivotX
                cX = self.scrX + xOffFromPiv #current x in self.assignedScr.scrBuffer

                yOffFromPiv = yyy - self.assignedTile.rPivotY
                cY = self.scrY + yOffFromPiv #current y in self.assignedScr.scrBuffer

                if 0 <= cX < self.assignedScr.width and 0 <= cY < self.assignedScr.height:
                    func(int(cY), int(cX), yyy, xxx)
                    #int() is necessary since cY and cX can become floats such as 4.0

    #put the self.assignedTile.rotTile cell into the screenBuffer
    def putRotTileToScr(self, aY, aX, bY, bX):
        #if self.assignedTile.rotTile[bY][bX] != o:
        if globals.isInList(self.assignedTile.rotTile[bY][bX], globals.emptyList) == False:
            self.assignedScr.scrBuffer[aY][aX] = self.assignedTile.rotTile[bY][bX]

    #delete previous on-screen tile from the screen buffer
    def dltScrTile(self, cY, cX, yyy, xxx):
        
        if self.assignedScr.scrBuffer[cY][cX] == self.assignedTile.rotTile[yyy][xxx]:
            self.assignedScr.scrBuffer[cY][cX] = o

    #NOTE: always check for collision BEFORE putting the rotTile into the scrBuffer
    def checkCollision(self, cY, cX, yyy, xxx):
        if self.isColliding == False:
            #if it isn't an empty space 
            if globals.isInList(self.assignedTile.rotTile[yyy][xxx], globals.wallList):
                if globals.isInList(self.assignedScr.scrBuffer[cY][cX], globals.wallList):
                    self.isColliding = True

    #pretty lazy gameover screen, change it when you'll have the time
    def gameOver(self):
        self.fallSpeed = 0 #so that when you spend some time on the gameover screen and then
                            #play again, the tile won't've been falling for the amount of
                            #time spent on the gameover screen

        start = perf_counter()
        now = 0
        rang = 5 #how long to display the gameover scr for before a new game starts
        inp = None
        prev = 1

        #display text for finite amount of time
        while now < rang:
            now = perf_counter() - start
            
            if int(now) != int(prev):
                prev = now
                self.assignedScr.clearScr()
                print("\n\n   GAME OVER\n\n    score:\n   ",self.score,end='')
                print("\n\n  TAB - info\n  ESC - quit\n  SPACE - retry")
                print("\n\n autoplay in:",rang-int(now))
                
            
            if kbhit():
                inp = getwch()
                if inp == chr(27):
                    raise SystemExit
                if inp == ' ':
                    break
                if inp == '\t': #if TAB
                    self.assignedScr.clearScr()
                    print(" W - rotate    | A,D - move horizontally")
                    print(" S - move down | Hold a key to spam it")
                    print("\n An adaptation of the game Tetris (1984)")
                    print(" by Алексей Леонидович Пажитнов")
                    print("\n Missing features:")
                    print(" - Pause button")
                    print(" - Incremental falling speed")
                    print(" - Next tile prediction")
                    print(" - Stop down-momentum when getting a new tile")
                    print(" - Settings menu")
                    print("\n version 1.0")
                    print(" Made in Python")
                    print(" © 2019 Pavol Pánisz")
                    print("\n press any key to continue",end='')
                    getwche()
                    continue

            
        
                
        self.loopScrTile(self.dltScrTile)
        self.assignedScr.clearInsideBorders()
            
        self.score = 0
        #end of lazy gameover screen

    #what happens when you collide falling down
    def collisionDown(self):
        self.score += 1

        #put the tile into the screenBuffer permanently
        self.scrY -= 1
        self.loopScrTile(self.putRotTileToScr)
        self.scrY += 1

        #is it game over? if no, give the player a new tile to control
        if self.scrY == self.assignedScr.spawnY and self.scrX == self.assignedScr.spawnX:
            self.gameOver()
            
        self.setTileDefaults()
        self.isColliding = False
        self.assignRandTile()
        self.setTileDefaults()
        

        self.attemptClearLine() #whenever a tile gets placed permanently, check if
                                #a full line formed

        #self.loopScrTile(self.checkCollision) #DEBUG - I left this here, don't know why.
                                               #if a bug happens, try uncommenting this.
        
        

    def attemptClearLine(self):
        wallsInLine = 0
        yyy = 24
        while yyy > 0: #does the same as the line below
        #for yyy in range(self.assignedScr.height-2, 0, -1):
            for xxx in range(1,self.assignedScr.width-1):
                if globals.isInList(self.assignedScr.scrBuffer[yyy][xxx], globals.wallList):
                    wallsInLine +=1

            #if the currently checked line is full
            if wallsInLine == self.assignedScr.width - 2:

                

                #set the line to empty-cells
                for lX in range(1,self.assignedScr.width-1):
                    self.assignedScr.scrBuffer[yyy][lX] = o

                #wait for the duration of clearingDelayTime ?
                    #(code here)

                #drag columns down by 1
                for lX in range(1,self.assignedScr.width-1): 
                    for cY in range(yyy, 0, -1):
                        
                        self.assignedScr.scrBuffer[cY][lX] = self.assignedScr.scrBuffer[cY-1][lX]

                yyy += 1 #check the same line, since it could've been changed

            yyy-=1

            
                    
            wallsInLine = 0

            

            

    



        
    
    
    

