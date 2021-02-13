"""Class that controls an Adafruit HT16K33 16x8 LED Matrix Driver
 requires Adafruit_Python_LED_Backpack (see https://github.com/adafruit/Adafruit_Python_LED_Backpack)
  The command
     i2cdetect -y
  should detect your dvice.

 """

import time

#from Adafruit_LED_Backpack import Matrix8x8
from Adafruit_LED_Backpack import Matrix8x16
import numpy as np
from constants import xMapper, yMapper, yMapperT


class HT16K33():
    """Class that controls an Adafruit HT16K33 16x8 LED Matrix Driver."""

    def __init__(self, address=0x70, busnum=1, size=8):
        """Create display instance on default I2C address (0x70) and bus number.
           check using I2cdetect -y 1  to make sure the address is 70,
           if not pass the right address and busnum """

        self.size = size
        self.matrix = np.zeros((size, size),dtype=int)
        #self.display = Matrix8x8.Matrix8x8(address=address, busnum=busnum)
        self.display = Matrix8x16.Matrix8x16(address=address, busnum=busnum)
        # Initialize the display. Must be called once before using the display.
        self.display.begin()

    def setPixelsOn(self, xList, yList, clear = True,
                    chessMapperOn=False):
        """ x and y are arrays. light all the pixels in the array.
        If chessMapper is True then the input uses chess notation"""
        if chessMapperOn:
            for n, x in enumerate(xList):
                xList[n] = xMapper[x.lower()]
            for n, y in enumerate(yList):
                yList[n] = yMapper[y]

        for x, y in zip(xList, yList):
            if clear:
                self.display.clear()
                self.matrix.fill(0)
            # anodes numbers starts 1
            # cathodes number start 0
            if y==7:
                self.display.set_pixel(x+1, y+1, 1)
            else:
                self.display.set_pixel(x+1, y, 1)
            self.matrix[x][y]=1
            self.display.write_display()

    def setPixelsMatrixOn(self, matrix):
        """ set all coords equal to 1 in matrix on.
        switch off others"""
        self.display.clear()
        self.matrix.fill(0)
        for x in range(0, self.size):
            for y in range(0, self.size):
                if matrix[x][y] == 1:
                    self.display.set_pixel(x+1, y, 1)
                    self.matrix[x][y]=1
        self.display.write_display()

    def setPixelsOff(self, xList, yList, clear = True,
                     chessMapperOn=False):
        """ x and y are arrays. light all the pixels in the array
            If chessMapper is True then the input uses chess notation"""
        if chessMapperOn:
            for n, x in enumerate(xList):
                xList[n] = xMapper[x.lower()]
            for n, y in enumerate(yList):
                yList[n] = yMapper[y]

        for x, y in zip(xList, yList):
            if clear:
                self.display.clear()
                self.matrix.fill(0)
                return
            # anodes numbers starts 1
            # cathodes number start 0
            self.display.set_pixel(x+1, y, 0)
            self.matrix[x][y]=0
        self.display.write_display()

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

    def getSize(self):
        return self.size

def testMatrix(ledMatrix, printOn=True, seconds=1):
    """test function. LEDS light one by one in the order 1 to size*size"""
    while True:
        for x in list(xMapper.keys())[:ledMatrix.getSize()]:
            for y in list(yMapper.keys())[:ledMatrix.getSize()]:
                ledMatrix.setPixelsOn([x], [y], chessMapperOn=True, clear = True)
                if printOn:
                    print("led %s %d ON" %
                      (x, y))
                    ledMatrix.printM()
                time.sleep(seconds)

def testMatrix2(ledMatrix, printOn=True, seconds=1):
    """test function. switch on all leds one after the other.
    Then switch then off"""
    while True:
        for x in list(xMapper.keys())[:ledMatrix.getSize()]:
            for y in list(yMapper.keys())[:ledMatrix.getSize()]:
                ledMatrix.setPixelsOn([x], [y], chessMapperOn=True, clear = False)
                if printOn:
                    print("led %s %d ON" %
                      (x, y))
                    ledMatrix.printM()
                time.sleep(seconds)
        for x in list(xMapper.keys())[:ledMatrix.getSize()]:
            for y in list(yMapper.keys())[:ledMatrix.getSize()]:
                ledMatrix.setPixelsOff([x], [y], chessMapperOn=True, clear = False)
                if printOn:
                    print("led %s %d OFF" %
                      (x, y))
                    ledMatrix.printM()
                time.sleep(seconds)
