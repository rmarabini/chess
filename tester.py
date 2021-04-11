from matrixled import HT16K33, testMatrix, testMatrix2, testMatrix3
from gpioreed import CPIOreed, testUsingReeds, testUsingReeds2
from game import testLedReedCloseMatrix, testLedReedCloseSwitch
from game import Chess
import sys
import time

arg = sys.argv[1]

if arg == "led1":  # switch led one by one
    ledMatrix = HT16K33(size=8)
    testMatrix(ledMatrix, seconds = 0.25)
elif arg == "led2": # switch led comulatibily
    ledMatrix = HT16K33(size=8)
    testMatrix2(ledMatrix, seconds = 0.1)
elif arg == "led3":  # switch all leds
    ledMatrix = HT16K33(size=8)
    testMatrix3(ledMatrix)

elif arg == "reed1": # show squares with piece
    cpio = CPIOreed(address=0x21, size=8)
    cpio.reset2()
    testUsingReeds(cpio)
elif arg == "reed2": # detect modification of board
    cpio = CPIOreed(address=0x21, size=8)
    cpio.reset2()
    testUsingReeds2(cpio,seconds=0.5)
elif arg == "both1":
    testLedReedCloseMatrix(seconds=0.1)
elif arg == "both2":
    testLedReedCloseSwitch(seconds=1)
elif arg == 'chessw':  # initializacion
    epd='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - hmvc 0; fmvn 1;'
    #epd='r1bqkbnr/ppp1p1pp/2n2p2/3pP3/3P4/8/PPP2PPP/RNBQKBNR w KQkq - hmvc 0; fmvn 4;'
    counter = 0
    chess = Chess(level=0.05, firstPlayer='h', epd=epd, depth=2)
    chess.play_game(chess.humanPlayer, chess.computerPlayer, pause=0.05)
    #chess.engine.quit()
elif arg == 'chessb':  # initializacion
    counter = 0
    epd='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - hmvc 0; fmvn 1;'
    chess = Chess(level=0.05, firstPlayer='c', epd=epd, depth=2)
    chess.play_game(chess.computerPlayer, chess.humanPlayer, pause=0.05)
    #chess.engine.quit()
    # epd='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - hmvc 0; fmvn 1;'
print("END")
