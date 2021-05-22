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
    #fen='rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
    fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    counter = -1 # number of have moves
    chess = Chess(level=0.05, firstPlayer='h', fen=fen, depth=2, keyboard=counter)
    chess.play_game(chess.humanPlayer, chess.computerPlayer, pause=0.05)
    #chess.engine.quit()
elif arg == 'chessb':  # initializacion
    counter = -1
    epd='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - hmvc 0; fmvn 1;'
    chess = Chess(level=0.05, firstPlayer='c', epd=epd, depth=3)
    chess.play_game(chess.computerPlayer, chess.humanPlayer, pause=0.05)
    #chess.engine.quit()
    # epd='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - hmvc 0; fmvn 1;'
elif arg == 'chesswt':  # initializacion
    #fen='rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
    fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    counter = -1 # number of half moves
    chess = Chess(level=0.05, firstPlayer='h', fen=fen, depth=2, keyboard=counter,
    training = True)
    chess.play_game(chess.humanPlayer, chess.computerPlayer, pause=0.05)
    #chess.engine.quit()
print("END")
