from random import randint
from time import perf_counter, sleep
from msvcrt import getwch, kbhit #for getting keyboard input

import globals
import cl_player
import cl_screen
import cl_tile

o = globals.o
x = globals.x
p = globals.p
d = globals.d


tileT = cl_tile.Tile([x,p,x],
                     [o,x,o])
tileU = cl_tile.Tile([x,d,x], #for showcasing an empty pivot (d)
                     [x,x,x])
tileI = cl_tile.Tile([x],
                     [p],
                     [x],
                     [x])

tileS = cl_tile.Tile([o,x],
                [p,x],
                [x,o])
tileIS = cl_tile.Tile([x,o],
                      [x,p],
                      [o,x])
tileL = cl_tile.Tile([x,o],
                [x,o],
                [p,x])
tileIL = cl_tile.Tile([o,x],
                 [o,x],
                 [x,p])

tileList = [tileT, tileI, tileS, tileIS, tileL, tileIL]
scr1 = cl_screen.Screen(26,12)

p1 = cl_player.Player("NoName", scr1, tileList)





#game loop
while True:

    if kbhit(): #if any key was pressed this cycle
        inp = getwch() #gets the last keypress
        p1.loopScrTile(p1.dltScrTile)

        if inp == globals.rotate:
            p1.assignedTile.rotation += 90
            p1.assignedTile.rotate(p1.assignedTile.rotation)
            #if no col, keep rot. else, rot -=90.
            p1.loopScrTile(p1.checkCollision)
            p1.doScrUpdate = True

            if p1.isColliding == True:
                p1.assignedTile.rotation -= 90
                p1.assignedTile.rotate(p1.assignedTile.rotation)
                p1.isColliding = False
                p1.doScrUpdate = False


        if inp == globals.down:
            prevScrY = p1.scrY
            
            p1.y += globals.precision #move 1 line down
            p1.y2scrY()

            if prevScrY != p1.scrY:
                p1.doScrUpdate = True

                p1.loopScrTile(p1.checkCollision)
                if p1.isColliding == True:
                    p1.collisionDown()

        if ((inp == globals.left) or (inp == globals.right)):
            prevX = p1.scrX
            
            if inp == globals.left:
                p1.scrX -= 1
            if inp == globals.right:
                p1.scrX += 1

            p1.loopScrTile(p1.checkCollision)
            if p1.isColliding == True:
                p1.scrX = prevX
                p1.isColliding = False

            else:
                p1.doScrUpdate = True

    prevScrY = p1.scrY

    p1.loopScrTile(p1.dltScrTile)
    p1.y += int(globals.precision * p1.fallSpeed * globals.deltaTime)
    p1.y2scrY()

    if prevScrY != p1.scrY:
        p1.doScrUpdate = True

    '''put here so that when in gameOver, the player doesn't move.
       the player moves because deltaTime gets calculated properly
       even if the game has been on halt for long. (see how deltaTime
       gets calculated in globals.py using perf_counter() for more info).
       To get over this, instead of manipulating deltaTime, we set the
       falling speed to zero when in gameOver and to normal everywhere
       else, which means in the next line:'''
    p1.fallSpeed = p1.actualFallSpeed #gets set to normal, because if a
                                      #gameover happens, fallSpeed is 0.

    #after incrementing the y in the y2scrY line above, check coll. down
    p1.loopScrTile(p1.checkCollision)
    if p1.isColliding == True:
        p1.collisionDown()
        

    if p1.doScrUpdate:
        p1.assignedScr.clearScr()
        p1.loopScrTile(p1.putRotTileToScr)

        

        p1.assignedScr.printScrBuffer()
        p1.doScrUpdate = False
        print("score:",p1.score) #lazy, temporary way of printing

    globals.calculateDeltaTime()

    


    

    





    
