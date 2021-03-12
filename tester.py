from matrixled import HT16K33, testMatrix, testMatrix2, testMatrix3
from gpioreed import CPIOreed, testUsingReeds, testUsingReeds2
from reedled import testLedReedCloseMatrix, testLedReedCloseSwitch
import sys
import time

arg = sys.argv[1]

if arg == "led1":
    ledMatrix = HT16K33(size=8)
    testMatrix(ledMatrix, seconds = 0.25)
elif arg == "led2":
    ledMatrix = HT16K33(size=8)
    testMatrix2(ledMatrix, seconds = 0.1)
elif arg == "led3":
    ledMatrix = HT16K33(size=8)
    testMatrix3(ledMatrix)
elif arg == "reed1":
    cpio = CPIOreed(address=0x21, size=8)
    cpio.reset2()
    testUsingReeds(cpio)
elif arg == "reed2":
    cpio = CPIOreed(address=0x21, size=8)
    cpio.reset2()
    testUsingReeds2(cpio,seconds=0.5)
elif arg == "both1":
    testLedReedCloseMatrix(seconds=0.1)
elif arg == "both2":
    testLedReedCloseSwitch(seconds=1)
    

exit(1)
"""
>>> cpio.GPIOB[0].direction = Direction.OUTPUT
>>> cpio.GPIOA[0].direction = Direction.INPUT
>>> cpio.GPIOA[0].pull = Pull.UP
>>> cpio.GPIOA[0].value; cpio.GPIOB[0].value
True
False
>>> cpio.GPIOA[0].value; cpio.GPIOB[0].value
True
False
>>> cpio.GPIOA[0].value = True
>>> cpio.GPIOA[0].value; cpio.GPIOB[0].value
True
False
>>> cpio.GPIOA[B].value = True
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'B' is not defined
>>> cpio.GPIOB[0].value = True
>>> cpio.GPIOA[0].value; cpio.GPIOB[0].value
True
True
>>> cpio.GPIOA[0].value; cpio.GPIOB[0].value
True
True
>>> cpio.GPIOA[0].value; cpio.GPIOB[0].value
True
True
>>> cpio.GPIOB[0].value = False
>>> cpio.GPIOA[0].value; cpio.GPIO



ledMatrix = HT16K33(size=3)
#testMatrix(ledMatrix,printOn=True, seconds=0.5)
#testMatrix2(ledMatrix,printOn=True, seconds=0.5)
cpio = CPIOreed(address=0x21, size=3)
cpio.testUsingLeds()


from matrixled import HT16K33, testMatrix, testMatrix2, testMatrix3
ledMatrix = HT16K33(size=8)
testMatrix3(ledMatrix)
#testMatrix2(ledMatrix, True, .25)


##########
#>>> from gpioreed import GPIOreed
#>>> g = GPIOreed(size=1)
#>>> g.print()
# 1 [0 ]
#    a
#>>> g.getGPIOMatrix()
#>>> g.print()
#######
#>>> from gpioreed import GPIOreed; g = GPIOreed(size=3)
#>>> g.getGPIOMatrix(); g.print()
#>>> from matrixled import HT16K33
#>>> ledMatrix = HT16K33(size=3)
#>>> g.getGPIOMatrix(ledMatrix); g.print()

"""
