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
    def __init__(self, address=0x70, busnum=1):
        """Create display instance on default I2C address (0x70) and bus number.
           check using I2cdetect -y 1  to make sure the address is 70,
           if not pass the right address and busnum """

        self.display = Matrix8x8.Matrix8x8(address=address, busnum=busnum)
        # Initialize the display. Must be called once before using the display.
        self.display.begin()

    def setPixels(self, xList, yList, clear = True):
        """ x and y are arrays. light all the pixels in the array"""
        for x, y in zip(xList, yList):
            if clear:
                self.display.clear()
            # anodes numbers starts 1
            # cathodes number start 0
            self.display.set_pixel(x+1, y, 1)
            self.display.write_display()

    def testMatrix(self, size=8, printOn=True, seconds=1):
        """test function. LEDS light one by one in the order 1 to size*size"""
        while True:
            for led in range(size*size):   # anodes numbers starts 1
                x = led // 3 + 1    # anodes numbers starts 1
                y = led % 3   # cathodes number start 0
                self.setPixels([x], [y], clear = True)
                if printOn:
                    print("led %d %d ON" % (x, y))
                time.sleep(seconds)
