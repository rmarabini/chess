from matrixled import HT16K33, testMatrix, testMatrix2
from gpioreed import CPIOreed
cpio = CPIOreed(address=0x21, size=3)
cpio.reset2()
cpio.testUsingReeds()

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


from matrixled import HT16K33, testMatrix, testMatrix2
ledMatrix = HT16K33(size=9)
testMatrix2(ledMatrix, True, .5)


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
