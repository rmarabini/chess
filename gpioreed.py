import RPi.GPIO as GPIO
import numpy as np

class GPIOreed():
    """acess reed sdwitch using GPIO"""
    catMapper={}
    anoMapper = {}

    for k, v in zip ([1, 2, 3, 4, 5, 6, 7, 8],
                     [23, 24, 25, 12, 16, 20, 21, 26]):
        catMapper[k]=v

    for k, v in zip (['a','b', 'c','d','e','f','g','h'],
                     [ 4, 17, 27, 22,  5,  6, 13, 19]):
        anoMapper[k]=v

    def __init__(self, catodes, anodes, size=8):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for cat, ano in zip(catodes, anodes):
            GPIO.setup(cat, GPIO.OUT)
            GPIO.setup(ano, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.size = size
        self.matrix = np.zeros((size, size),dtype=int)

    def getGPIOMatrix(self):
        for row in range(self.size):
            GPIO.output(row, GPIO.LOW)  # cat
            for col in range(self.size):
                if GPIO.input(col):
                    self.matrix[row][col] = 1  # close
                else:
                    self.matrix[row][col] = 0
            GPIO.output(row, GPIO.LOW)

    def getMatrixChange(self):
        oldMatrix = np.copy(self.matrix)
        self.getGPIOMatrix()
        equal_arrays = np.array_equal(oldMatrix, self.matrix)

        if equal_arrays:
            return []
        else:
            differences = np.where(oldMatrix != self.matrix)
            cols = differences[0]
            rows = differences[1]
            pairs = []
            for col, row in zip(cols, rows):
                pairs.append(col, row)
            return pairs



