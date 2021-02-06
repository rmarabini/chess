from matrixled import HT16K33

ledMatrix = HT16K33(size=3)
ledMatrix.testMatrix(printOn=True, seconds=0.5)
#ledMatrix.testMatrix2(printOn=True, seconds=0.5)

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

