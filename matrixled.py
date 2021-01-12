"""Class that controls an Adafruit HT16K33 16×8 LED Matrix Driver
 requires Adafruit_Python_LED_Backpack (see https://github.com/adafruit/Adafruit_Python_LED_Backpack)
  The command
     i2cdetect -y
  should detect your dvice.

 """

import time
from Adafruit_LED_Backpack import Matrix8x8
"""Class that controls an Adafruit HT16K33 16×8 LED Matrix Driver."""

class HT16K33():
    xMapper={}
    yMapper = {}
    for k, v in zip ([1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7]):
        yMapper[k]=v
    for k, v in zip (['a','b', 'c','d','e','f','g','h'],
                     [0, 1, 2, 3, 4, 5, 6, 7]):
        xMapper[k]=v

    def __init__(self, address=0x70, busnum=1):
        """Create display instance on default I2C address (0x70) and bus number.
           check using I2cdetect -y 1  to make sure the address is 70,
           if not pass the right address and busnum """

        self.display = Matrix8x8.Matrix8x8(address=address, busnum=busnum)
        # Initialize the display. Must be called once before using the display.
        self.display.begin()

    def setPixelsOn(self, xList, yList, clear = True,
                    chessMapperOn=False):
        """ x and y are arrays. light all the pixels in the array.
        If chessMapper is True then the input uses chess notation"""
        if chessMapperOn:
            for n, x in enumerate(xList):
                xList[n] = self.xMapper[x.lower()]
            for n, y in enumerate(yList):
                yList[n] = self.yMapper[y]

        for x, y in zip(xList, yList):
            if clear:
                self.display.clear()
            # anodes numbers starts 1
            # cathodes number start 0
            self.display.set_pixel(x+1, y, 1)
            self.display.write_display()

    def setPixelsOff(self, xList, yList, clear = True,
                     chessMapperOn=False):
        """ x and y are arrays. light all the pixels in the array
            If chessMapper is True then the input uses chess notation"""
        if chessMapperOn:
            for n, x in enumerate(xList):
                xList[n] = self.xMapper[x.lower()]
            for n, y in enumerate(yList):
                yList[n] = self.yMapper[y]

        for x, y in zip(xList, yList):
            if clear:
                self.display.clear()
            # anodes numbers starts 1
            # cathodes number start 0
            self.display.set_pixel(x+1, y, 0)
            self.display.write_display()

    def testMatrix(self, size=8, printOn=True, seconds=1):
        """test function. LEDS light one by one in the order 1 to size*size"""
        while True:
            for led in range(size*size):
                x = led // 3
                y = led % 3   # cathodes number start 0
                self.setPixelsOn([x], [y], clear = True)
                if printOn:
                    print("led %d %d ON" % (x, y))
                time.sleep(seconds)

    def testMatrix2(self, size=8, printOn=True, seconds=1):
        """test function. switch on all leds one after the other.
        Then switch then off"""
        while True:
            for led in range(size*size):
                x = led // 3
                y = led % 3
                self.setPixelsOn([x], [y], clear = False)
                if printOn:
                    print("led %d %d ON" % (x, y))
                time.sleep(seconds)
            for led in range(size*size):
                x = led // 3
                y = led % 3
                self.setPixelsOff([x], [y], clear = False)
                if printOn:
                    print("led %d %d OFF" % (x, y))
                time.sleep(seconds)

    def testMatrix3(self, size=8, printOn=True, seconds=1):
        """test function. LEDS light one by one in the order 1 to size*size"""
        yy=[1,2,3,4,5,6,7,8]
        xx=['a','b','c','d','e','f','g','h']
        while True:
            for led in range(size*size):
                x = xx[led // 3]
                y = yy[led % 3]
                self.setPixelsOn([x], [y], clear = False, chessMapperOn=True)
                if printOn:
                    print("led %s %d ON" % (x, y))
                time.sleep(seconds)
            for led in range(size*size):
                x = xx[led // 3]
                y = yy[led % 3]
                self.setPixelsOff([x], [y], clear = False, chessMapperOn=True)
                if printOn:
                    print("led %s %d OFF" % (x, y))
                time.sleep(seconds)
