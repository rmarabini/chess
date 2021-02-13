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
        self.matrix = np.zeros((size, size),dtype=int)
        self.GPIOA=[]
        self.GPIOB=[]
        for i in range(size):
            self.GPIOA.append(mcp.get_pin(i))
            self.GPIOB.append(mcp.get_pin(i+8))
        self.reset2()

    def reset(self):
        """ test, connect the led (not the reeds)
            to the MCP23017"""
        # for this test all pins should be output
        self.matrix[:]=0
        for i in range(self.size):
            self.GPIOA[i].direction = Direction.OUTPUT
            self.GPIOB[i].direction = Direction.OUTPUT
            self.GPIOA[i].value = True
            self.GPIOB[i].value = False

    def checkMatrix(self):
        print("Pressed =", end='')
        for row in range(self.size):
            self.checkLine(row)
        print()

    def checkLine(self, row):
        self.GPIOB[row].value = False
        for col in range(self.size):
            if self.GPIOA[col].value == False:
                self.matrix[col][row] = 1
            else:
                self.matrix[col][row] = 0

        self.GPIOB[row].value = True

    def reset2(self):
        """ MCP23017 initial state. All pins
            set to true. Since input is unestable
            when not connected to a source we need to
            use the pull.up resistors. Note the this IC
            does not have pul.down resistors"""
        # for the test all pins should be output
        self.matrix[:]=0
        for i in range(self.size):
            self.GPIOB[i].direction = Direction.OUTPUT
            self.GPIOA[i].direction = Direction.INPUT
            self.GPIOA[i].pull = Pull.UP
            self.GPIOA[i].value = True
            self.GPIOB[i].value = True

        # self.matrix = np.zeros((self.size, self.size),dtype=int)


    def testUsingLeds(self):
        """ Connect MCP23017 to led (A-> negative, B->positive)
        Discontinued"""
        self.reset()
        oldI = 0
        oldJ = 0
        while True:
          for i in range(self.size):  # col
            for j in range(self.size):  # row
                # reset matrix
                self.GPIOA[oldI].value = True
                self.GPIOB[oldJ].value = False
                self.matrix[i:j] = 0
                # set led on
                self.GPIOA[i].value = False
                self.GPIOB[j].value = True
                self.matrix[i][j] = 1
                oldI=i
                oldJ=j
                self.printM()
                time.sleep(0.5)

    def testUsingReeds(self):
        """ Connect MCP23017 to reed switches
             (A-> negative, B->positive"""
        self.reset2()
        while True:
            self.checkMatrix()
            self.printM()
            time.sleep(1)

    def printM(self):
        """Print self.matrix as a 2D array"""
        # (0,0 in matrix should be bottom left
        # in board
        for y in range(self.size -1, -1, -1):
            print(" %d [" % yMapperT[y], end="")
            for x in range(self.size):
                print("%d " % self.matrix[y][x], end="")
            print("]")
        print("   ", end="")
        for item in list(xMapper.keys())[:self.size]:
            print(" %s" % item, end="")
        print("")

    def getMatrixChange(self):
        """returns the tuple, (true/false, array of coordinates)
        The first element is false if there is no changes and
        true otherwise.
        Follows an array with positions that have change
        as (x,y) coordinates. If there is no change
        an empty array is returned"""
        oldMatrix = np.copy(self.matrix)
        self.checkMatrix()
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

