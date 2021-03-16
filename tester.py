from matrixled import HT16K33, testMatrix, testMatrix2, testMatrix3
from gpioreed import CPIOreed, testUsingReeds, testUsingReeds2
from game import testLedReedCloseMatrix, testLedReedCloseSwitch
from game import Chess
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
elif arg == 'chess1':  # initializacion
    counter = 0
    chess = Chess()
    chess.play_game(chess.humanPlayer, chess.computerPlayer)
    #while True:
    #    try:
    #        chess.checkforBoardPieces()
    #    except  Exception as e:
    #        print("BOARD ERROR: initial position is wrong")
    #        print(e)
    #    time.sleep(1)
    #    counter += 1
    #    print("counter %d" % counter)
    # chess.checkforBoardPieces()
    chess.engine.quit()
print("END")
