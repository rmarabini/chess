from matrixled import HT16K33
from gpioreed import CPIOreed
from constants import ERROR, OK, Mapper
import chess
import chess.engine
import chess.pgn
import time
import numpy as np
from datetime import datetime
class BoardError(Exception):
    pass

class Chess():
    """ Main class for chess game. pip3 install chess required"""
    def __init__(self, size=8, address=0x21, level=0.1, # second for stockfish
                 firstPlayer='h', stockfishBin="/usr/games/stockfish", depth =2,
                 fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 keyboard = -1,  # introduce move through keyboard
                                 # after "keyboard" moves the game starts
                 training=False # moves introduced using the board,
                                  # game starts if move a1a1 is introduced
                 ):
        self.training = training
        self.cpio = CPIOreed(address=address, size=size)
        self.ledMatrix = HT16K33(size=size)
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfishBin)
        self.board = chess.Board()
        self.board.set_fen(fen)
        self.time = level
        self.depth = depth
        self.keyboard = keyboard # number of have moves

        if firstPlayer == 'h': # h = human, c = computer, b= both computer
            self.player1 = self.humanPlayer
            self.player2 = self.computerPlayer
            self.computerColor = chess.BLACK
            self.humanColor = chess.WHITE
        elif firstPlayer == 'c':
            self.player1 = self.computerPlayer
            self.player2 = self.humanPlayer
            self.computerColor = chess.WHITE
            self.humanColor = chess.BLACK
        else:
            self.player1 = self.computerPlayer
            self.player2 = self.computerPlayer
        # switch on all led (1 sec)
        print("Checking leds: switch on all for a second")
        self.ledMatrix.switchOnAllLeds()
        time.sleep(1)
        # switch on led with pieces
        print("Checking reeds: switch leds with pieces for a second")
        self.switchLedWithPieces()
        time.sleep(1)
        self.ledMatrix.clear()
        # switch off all
        
	    
    def checkforBoardPieces(self, counter=0):
        self.cpio.checkMatrix()
        # reed switch matrix
        cpioMatrix = self.cpio.getMatrix()
        # chess board matrix
        chessMatrix = np.zeros_like(cpioMatrix)
        # get dictionary with piece position
        piece_map = self.board.piece_map()
        # update chessMatrix
        for square, piece in piece_map.items():
            chessMatrix[square] = 1
        # compare matrices, if they are not equal complain
        equal_arrays = np.array_equal(cpioMatrix, chessMatrix)
        if not equal_arrays:
            squaresdifferent = np.where(cpioMatrix != chessMatrix)[0]
            for square in squaresdifferent:
                print("square", Mapper[square], "is differente")
            print(self.cpio.printM(counter))
            print(self.board.unicode(invert_color=True))
            print("BOARDERROR: square %s, %s is wrong" % 
                                          (Mapper[square]), counter)
            print(self.board.fen())
            if counter==0:
                self.switchLedWithPieces()
                time.sleep(.25)
                self.ledMatrix.clear()
            return False
                
        return True

    def loopUntillPiecesAreInTheRightPlace(self, counter=1):
        while True:
            if self.checkforBoardPieces(counter):
                break
            print("Pieces NO OK.\n"
                   " Please place them as in the diagram")
            time.sleep(2)

    def getMove(self, prompt):
        uci = input(prompt)
        if uci and uci[0] == "q":
            raise KeyboardInterrupt()
        try:
            chess.Move.from_uci(uci)
        except:
            uci = None
        return uci

    def getMoveFromBoard(self, prompt, myColor):
        print(prompt)
        first = True
        uci=""
        while True:
            skip = False
            result, squaresPlus, squaresMinus = self.cpio.getMatrixChange()
            if result:
                for square in squaresMinus:
                    if self.board.color_at(square) != myColor:
                         skip = True
                         break
                if skip: 
                    continue
                if first:
                    squares = squaresMinus
                else:
                    squares = squaresPlus
                for square in squares:
                    uci += Mapper[square][0]+str(Mapper[square][1])
                    print("uci", uci)
		            # switch on led
                    self.ledMatrix.setPixelsOn([square])
                    if first == False:
                         print("return uci", uci)
                         time.sleep(.25)  # wait so we can see the led of the final pposition
                         return uci
                first = False
            time.sleep(.01)

    def moveLoop(self, mycolor):
        uci = self.getMoveFromBoard("%s's move> " %
                                    self.who(self.board.turn),
                                    mycolor)
        legal_uci_moves = [move.uci() for move in self.board.legal_moves]
        counter = 0
        while uci not in legal_uci_moves:
            # so far always promote to queen
            promotion = uci + "q"
            if promotion in legal_uci_moves:
                uci += "q"
                break
            if self.training and uci[:2] == uci[-2:]:
                self.training = False
                if self.computerColor == mycolor:
                    return False
            print(self.cpio.printM(counter))
            print(self.board.unicode(invert_color=True))
            print("sent move = ", uci, "training = ", self.training)
            print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
            print("reset board")
            time.sleep(0.1)
            # input("reset board and press enter to continue\n")
            self.cpio.getMatrixChange()  # update matrix

            uci = self.getMoveFromBoard("%s's move[q to quit]> " % self.who(
                self.board.turn), self.humanColor)
            counter += 1
            # check if castling
        try:
            self.board.push_uci(uci)
        except ValueError:
            print(ValueError)
        return uci         	    

	
    def humanPlayer(self, keyboard = False):
        if keyboard or len(self.board.move_stack) < self.keyboard:
            # TODO: origin led on 0.1 seg, target on till next move
            uci = self.getMove("%s's move [q to quit]> " %
                               self.who(self.board.turn))
            legal_uci_moves = [move.uci() for move in self.board.legal_moves]
            while uci not in legal_uci_moves:
                print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
                uci = self.getMove("%s's move[q to quit]> " % self.who(
                    self.board.turn))
            self.board.push_uci(uci)
            return uci
        else:
            return self.moveLoop(self.humanColor)

    def computerPlayer(self, keyboard=False):
        if keyboard or len(self.board.move_stack) < self.keyboard:
            # TODO: origin led on 0.1 seg, target on till next move
            uci = self.getMove("%s's move [q to quit]> " %
                               self.who(self.board.turn))
            legal_uci_moves = [move.uci() for move in self.board.legal_moves]
            while uci not in legal_uci_moves:
                print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
                uci = self.getMove("%s's move[q to quit]> " % self.who(
                    self.board.turn))
            self.board.push_uci(uci)
            return uci

        if self.training:
            uci = self.moveLoop(self.computerColor)
            if uci:
                return uci
        
        result = self.engine.play(self.board,
                                  chess.engine.Limit(time=self.time, depth=self.depth))
        self.ledMatrix.clear(write=True)
        source = result.move.from_square
        target = result.move.to_square
        self.ledMatrix.setPixelsOn([source, target])
        # check result
        try:
            # TODO: no uci needed just self.board.push(result.move)
            self.board.push_uci(result.move.uci())
        except ValueError:
            print(ValueError)
        return result.move.uci()

    def who(self, player):
                return "White" if player == chess.WHITE else "Black"

    def png(self, board):
        game = chess.pgn.Game.from_board(board)
        game.headers['Date'] = datetime.today().strftime('%Y-%m-%d')
        if self.computerColor == chess.BLACK:
            game.headers['White'] = 'human'
            game.headers['Black'] = 'computer'
        else:
            game.headers['Black'] = 'human'
            game.headers['White'] = 'computer'
        print("game:\n", game, "\n")

    def play_game(self, player1, player2, visual="svg", pause=0.01):
        """
peek() -> last move
is_castling -> Checks if the given pseudo-legal move is a castling move.
        """
        counter=0
        try:
            while not self.board.is_game_over(claim_draw=True):
                # loop until reed switch and board
                # are in agreement
                self.loopUntillPiecesAreInTheRightPlace(counter=counter)
                self.ledMatrix.clear(write=True)
                print(self.cpio.printM(-1))
                print(self.board.unicode(invert_color=True))
                if self.board.turn == chess.WHITE:
                    uci = player1()
                else:
                    uci = player2()
                if self.board.is_check():
                     print("CHECK: ", self.who(self.board.turn))
                     kingSquare = self.board.pieces(chess.KING, self.board.turn)
                     self.ledMatrix.blink(kingSquare,.5)
                     
                print("---------")
                print(self.board.unicode(invert_color=True))
                counter += 1
                time.sleep(pause)
        except KeyboardInterrupt:
            msg = "Game interrupted!"
            # print game if ctrl-C is pressed
            self.png(self.board)
            return
        result = None
        if self.board.is_checkmate():
            msg = "checkmate: " + self.who(not self.board.turn) + " wins!"
            result = not self.board.turn
        elif self.board.is_stalemate():
            msg = "draw: stalemate"
        elif self.board.is_fivefold_repetition():
            msg = "draw: 5-fold repetition"
        elif self.board.is_insufficient_material():
            msg = "draw: insufficient material"
        elif self.board.can_claim_draw():
            msg = "draw: claim"
        print(msg)
        self.png(self.board)

        try:
            self.engine.quit()
        except:
            print("bye")
    
    def switchLedWithPieces(self):
        """switch on led where there is a close reed switch"""
        self.cpio.reset2()
        self.cpio.checkMatrix()
        self.ledMatrix.setPixelsMatrixOn(self.cpio.matrix)


##########################
def testLedReedCloseMatrix(seconds=0.1):
    """switch on led where there is a close reed switch"""
    ledMatrix = HT16K33(size=8)
    cpio = CPIOreed(address=0x21, size=8)
    cpio.reset2()
    while True:
        cpio.checkMatrix()
        ledMatrix.setPixelsMatrixOn(cpio.matrix)
        time.sleep(seconds)

def testLedReedCloseSwitch(seconds=1):
    """switch on led when siation changes"""
    ledMatrix = HT16K33(size=8)
    cpio = CPIOreed(address=0x21, size=8)
    cpio.reset2()
    while True:
        change, squaresPlus, squaresMinus = cpio.getMatrixChange()
        print(change, squaresPlus, squaresMinus)
        ledMatrix.display.clear()
        ledMatrix.matrix.fill(0)
        ledMatrix.display.write_display()
        if change:
            for square in squaresPlus:
                print("ON")
                ledMatrix.setPixelsOn([square], clear=True)
            for square in squaresMinus:
                print("OFF")
                ledMatrix.setPixelsOn([square], clear=True)
        time.sleep(seconds)
