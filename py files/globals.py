'''File used to declare common variables and functions,
   aswell as to make porting code to different platorms
   easier'''

from os import system #for clearing the console
from time import perf_counter

#used to draw the screen
global o #empty
global x #wall
global p #pivot that's also a wall
global d #empty pivot
o = '.'
x = '#'
p = 'p'
d = 'd'

global rotate, down, left, right #keys
rotate = 'w'
down = 's'
left = 'a'
right = 'd'

#the name precision is used to attempt avoiding using floats
#use: time.clock() * precision
#  ->converts the returned time by perf_counter() in float to an int
global precision
precision = 1000000

global nameLength 
nameLength = 6

pivotList: chr = [p, d]
wallList: chr = [p, x]
emptyList: chr = [d, o]

def isInList(i: chr, lst: chr)->bool:
    for el in lst:
        if el == i:
            return True
    return False

#for the windows console:
'''if we have multiple screens, write here multiple write() methods
   and attach each to a screen object.
'''

#translated chars to what they will appear like on the screen
scrCharDict = {p : '░',
               x : '░',
               d : '.',
               o : '.'}

#calculates the time elapsed since the last cycle of the gameloop
deltaTime = 0 #this is the variable we're interested in
timePrevFrame = 0
timeThisFrame = perf_counter()
def calculateDeltaTime():
    global deltaTime, timePrevFrame, timeThisFrame
    timePrevFrame = timeThisFrame
    timeThisFrame = perf_counter()
    deltaTime = timeThisFrame - timePrevFrame
    

def write1(c):
    if c in scrCharDict:
        print(scrCharDict[c],end='')
    else:
        print(c,end='')
    pass
def sequentialWrite1(s):
    for el in s:
        write1(el)
    pass
def clrScr():
    system('cls')
    pass






    
