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
from constants import Mapper, X, Y


class HT16K33():
    """Class that controls an Adafruit HT16K33 16x8 LED Matrix Driver."""

    def __init__(self, address=0x70, busnum=1, size=8):
        """Create display instance on default I2C address (0x70) and bus number.
           check using I2cdetect -y 1  to make sure the address is 70,
           if not pass the right address and busnum """

        self.size = size
        self.matrix = np.zeros((size * size),dtype=int)
        #self.display = Matrix8x8.Matrix8x8(address=address, busnum=busnum)
        self.display = Matrix8x16.Matrix8x16(address=address, busnum=busnum)
        # Initialize the display. Must be called once before using the display.
        self.display.begin()
        self.clear(write=True)

    def clear(self, write=False):
        self.display.clear()
        self.matrix.fill(0)
        if write:
            self.display.write_display()
    
    def setPixelsOn(self, squares, clear = True):
        """ x and y are arrays. light all the pixels in the array.
        If chessMapper is True then the input uses chess notation"""

        if clear:
            self.clear()

        for square in squares:
            self.display.set_pixel(square // self.size, 
	                           square % self.size, 1)
            self.matrix[square]=1
            self.display.write_display()

    def setPixelsMatrixOn(self, matrix):
        """ set all coords equal to 1 in matrix on.
        switch off others"""
        self.clear()
        for square, square_value in enumerate(matrix):
            if square_value == 1:
                self.display.set_pixel(square // self.size, 
		                       square % self.size, 1)
                self.matrix[square] = 1
        self.display.write_display()

    def setPixelsOff(self, squares, clear = True,
                     chessMapperOn=False):
        """ light all the pixels in the array
            If chessMapper is True then the input uses chess notation"""

        if clear:
            self.clear()

        for square in squares:
            self.display.set_pixel(square // self.size, 
	                           square % self.size, 0)
            self.matrix[square]=0
            self.display.write_display()

    def printM(self):
        """Print self.matrix as a 2D array"""
        # (0,0 in matrix should be bottom left
        # in board
        for y in range(self.size -1, -1, -1):
            print(" %d [" % Y[y], end="")
            for x in range(self.size):
                print("%d " % self.matrix[x + y * self.size], end="")
            print("]")
        print("   ", end="")
        for item in X[:self.size]:
            print(" %s" % item, end="")
        print("")

    def getSize(self):
        return self.size

def testMatrix(ledMatrix, printOn=True, seconds=1):
    """test function. LEDS light one by one in the order 1 to size*size"""
    while True:
        for k, v in Mapper.items():
            ledMatrix.setPixelsOn([k], clear = True)
            if printOn:
                print("led ", v, " ON")
                ledMatrix.printM()
            time.sleep(seconds)
				
def testMatrix2(ledMatrix, printOn=True, seconds=1):
    """test function. switch on all leds one after the other.
    Then switch then off one by one"""
    while True:
        for k, v in Mapper.items():
            ledMatrix.setPixelsOn([k], clear = False)
            if printOn:
                print("led ", v, " ON")
                ledMatrix.printM()
            time.sleep(seconds)
        for k, v in Mapper.items():
            ledMatrix.setPixelsOff([k], clear = False)
            if printOn:
                print("led ", v, " OFF")
                ledMatrix.printM()
            time.sleep(seconds)



def testMatrix3(ledMatrix, printOn=True):
    """ switch on all led at the same time"""
    matrix = np.ones(64,dtype=int)
    ledMatrix.setPixelsMatrixOn(matrix)
    if printOn:
        ledMatrix.printM()

