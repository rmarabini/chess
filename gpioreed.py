import RPi.GPIO as GPIO
import numpy as np
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
import time

from constants import xMapper, yMapper, yMapperT
class CPIOreed():
    """access reed switch using GPIO.
    some interesting CLIs
     pinout returns raspberry pinout
     gpio readall returns the state of all ports"""
    def __init__(self, size=8, address=0x21):
        self.size = size
        i2c = busio.I2C(board.SCL, board.SDA)
        mcp = MCP23017(i2c, address=address)
        self.GPIOA=[]
        self.GPIOB=[]
        for i in range(size):
            pin = mcp.get_pin(i)
            self.GPIOA.append(pin)
            #set as output
            #pin.direction = Direction.OUTPUT
            pin = mcp.get_pin(i+8)
            # set as input and pull resistence to DOWN
            self.GPIOB.append(mcp.get_pin(i+8))
            #pin.direction = Direction.INPUT
            #pin.pull = Pull.UP

    def reset(self):
        """ test, connect the led (not the reeds)
            to the MCP23017"""
        # for the test all pins should be output
        for i in range(self.size):
            self.GPIOA[i].direction = Direction.OUTPUT
            self.GPIOB[i].direction = Direction.OUTPUT
            self.GPIOA[i].value = True
            self.GPIOB[i].value = False
        # self.matrix = np.zeros((self.size, self.size),dtype=int)


    def testUsingLeds(self):
        self.reset()
        oldI = 0
        oldJ = 0

        for i in range(self.size):
            for j in range(self.size):
                print("i, j", i, j)
                # reset matrix
                self.GPIOA[oldI].value = True
                self.GPIOB[oldJ].value = False
                # set led on
                self.GPIOA[i].value = False
                self.GPIOB[j].value = True
                oldI=i
                oldJ=j
                time.sleep(0.5)

class GPIOreedX():
    """access reed switch using GPIO.
    some interesting CLIs
     pinout returns raspberry pinout
     gpio readall returns the state of all ports"""
    catMapper = {}  # map actual GPIO numbers to columns // C
    anoMapper = {}  # map actual GPIO numbers to rows  // L

    for k, v in zip ([0, 1, 2, 3, 4, 5, 6, 7],
                     [23, 4, 25, 12, 16, 20, 21, 26]):
        anoMapper[k]=v

    for k, v in zip ([0, 1, 2, 3, 4, 5, 6, 7],
                     [ 24, 17, 27, 22,  5,  6, 13, 19]):
        catMapper[k]=v

    def __init__(self, size=8):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # PINs refer to the X in GPIOX label
        catodes = list(self.catMapper.values())[:size]
        anodes  = list(self.anoMapper.values())[:size]
        for cat, ano in zip(catodes, anodes):
            GPIO.setup(ano, GPIO.OUT)
            # in gpio need a pull down/up resistor
            # otherwise measurement will jump from high to low radomly
            GPIO.setup(cat, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.size = size
        self.matrix = np.zeros((size, size),dtype=int)

    def getGPIOMatrix(self, matrixLedObject=None):
        """fill 2D array self.matrix with the state of the reed
        switches. GPIO is used to access to then"""

        # for all rows...
        for row in range(self.size):
            # ...put output as high
            # and measure input
            # if switch is open measurement will be 0
            # otherwise measurement will be 1
            GPIO.output(self.anoMapper[row], GPIO.HIGH)  # cat
            for col in range(self.size):
                if GPIO.input(self.catMapper[col]):
                    self.matrix[row][col] = 1  # close
                else:
                    self.matrix[row][col] = 0  # open
            # put output to low and try with next one
            GPIO.output(self.anoMapper[row], GPIO.LOW)

        if matrixLedObject is not None:
            matrixLedObject.setPixelsMatrixOn(self.matrix)

    def getMatrixChange(self):
        """returns the tuple, (true/false, array of coordinates)
        The first element is false if there is no changes and
        true otherwise.
        Follows an array with positions that have change
        as (x,y) coordinates. If there is no change
        an empty array is returned"""
        oldMatrix = np.copy(self.matrix)
        self.getGPIOMatrix()
        equal_arrays = np.array_equal(oldMatrix, self.matrix)

        if equal_arrays:
            return False, []
        else:
            differences = np.where(oldMatrix != self.matrix)
            cols = differences[0]
            rows = differences[1]
            pairs = []
            for col, row in zip(cols, rows):
                pairs.append(col, row)
            return True, pairs

    def printM(self):
        """Print self.matrix as a 2D array"""
        # (0,0 in matrix should be bottom left
        # in board
        for y in range(self.size -1, -1, -1):
            print(" %d [" % yMapperT[y], end="")
            for x in range(self.size):
                print("%d " % self.matrix[x][y], end="")
            print("]")
        print("   ", end="")
        for item in list(xMapper.keys())[:self.size]:
            print(" %s" % item, end="")
        print("")



