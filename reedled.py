from matrixled import HT16K33, testMatrix, testMatrix2
from gpioreed import CPIOreed
import chess
import chess.engine
import time

class Chess():
    """ Main class for chess game"""
    def __init__(self, size=8, address=0x21, time=0.1,
                 firstPlayer='h', stockfishBin="/usr/games/stockfish"):
        self.cpio = CPIOreed(address=address, size=size)
        self.ledMatrix = HT16K33(size=size)
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfishBin)
        self.board = chess.Board()
        self.time = time

        if firstPlayer == 'h': # h = human, c = computer, b= both computer
            self.player1 = self.humanPlayer
            self.player2 = self.computerPlayer
        elif firstPlayer == 'c':
            self.player1 = self.computerPlayer
            self.player2 = self.humanPlayer
        else:
            self.player1 = self.computerPlayer
            self.player2 = self.computerPlayer

    def getMove(self, prompt):
        uci = input(prompt)
        if uci and uci[0] == "q":
            raise KeyboardInterrupt()
        try:
            chess.Move.from_uci(uci)
        except:
            uci = None
        return uci

    def humanPlayer(self, keyboard = True):
        if keyboard:
            # TODO: origin led on 0.1 seg, target on till next move
            uci = self.getMove("%s's move [q to quit]> " %
                               self.who(self.board.turn))
            legal_uci_moves = [move.uci() for move in self.board.legal_moves]
            while uci not in legal_uci_moves:
                print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
                uci = self.getMove("%s's move[q to quit]> " % self.who(
                    self.board.turn))
            return uci
        else:
            pass

    def computerPlayer(self):
        result = self.engine.play(self.board,
                                  chess.engine.Limit(time=self.time))
        #TODO: orgin, target led ON till next movement
        return result.move.uci()

    def who(self, player):
        return "White" if player == chess.WHITE else "Black"

    def play_game(self, player1, player2, visual="svg", pause=0.1):
        """
peek() -> last move
is_castling -> Checks if the given pseudo-legal move is a castling move.
        """
        try:
            while not self.board.is_game_over(claim_draw=True):
                if self.board.turn == chess.WHITE:
                    uci = player1()
                else:
                    uci = player2()
                try:
                    self.board.push_uci(uci)
                except ValueError:
                    print(ValueError)

                print("---------")
                print(self.board)
                time.sleep(pause)
        except KeyboardInterrupt:
            msg = "Game interrupted!"
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
        self.engine.quit()
