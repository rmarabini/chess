import RPi.GPIO as GPIO
import numpy as np

class GPIOreed():
    """access reed switch using GPIO.
    CLI pinout returns raspberry pinout
    CLI gpio readall returns the state of all ports"""
    catMapper = {}  # map actual GPIO numbers to columns // C
    anoMapper = {}  # map actual GPIO numbers to rows  // L

    for k, v in zip ([1, 2, 3, 4, 5, 6, 7, 8],
                     [23, 24, 25, 12, 16, 20, 21, 26]):
        anoMapper[k]=v

    for k, v in zip (['a','b', 'c','d','e','f','g','h'],
                     [ 4, 17, 27, 22,  5,  6, 13, 19]):
        catMapper[k]=v

    def __init__(self, catodes, anodes, size=8):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # PINs refer to the X in GPIOX label
        for cat, ano in zip(catodes, anodes):
            GPIO.setup(ano, GPIO.OUT)
            # in gpio need a pull down/up resistor
            # otherwise measurement will jump from high to low radomly
            GPIO.setup(cat, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.size = size
        self.matrix = np.zeros((size, size),dtype=int)

    def getGPIOMatrix(self):
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

    def print(self):
        """Print self.matrix as a 2D array"""
        print(*(' '.join(row) for row in self.matrix), sep='\n')


