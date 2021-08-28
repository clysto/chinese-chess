import chess
import tkinter as tk
from tkinter import messagebox
import threading
from typing import Callable, Dict, List, Optional
from elephantfish import best_move
from PIL import Image, ImageTk

THINK_TIME = 5
FEN = "3k5/4a4/9/4c4/4N4/9/9/4K3c/9/9 w - - 0 1"


class PhotoImage(ImageTk.PhotoImage):
    @classmethod
    def open(cls, fp):
        return cls(Image.open(fp))


class ThinkThread(threading.Thread):
    def __init__(self, board: chess.Board, on_finish: Callable):
        threading.Thread.__init__(self)
        self.board = board
        self.on_finish = on_finish

    def run(self):
        move = best_move(self.board, think_time=THINK_TIME)
        print("computer move:" + str(move))
        if self.on_finish:
            self.on_finish(move)

    def stop(self):
        self.on_finish = None


class Application(tk.Frame):

    resources: Dict[str, PhotoImage]
    style = {"start_x": 10, "start_y": 10, "space_x": 40, "space_y": 40}
    boxs = []
    pieces = []
    select_square: Optional[chess.Square] = None
    moves: List[chess.Move] = []
    board: chess.Board
    checkmate: bool = False
    think_thread: ThinkThread = None
    rotate = False

    def __init__(self, master: tk.Tk = None) -> None:
        super().__init__(master)
        self.load_resources()
        self.master = master
        self.master.title("中国象棋")
        self.master.resizable(False, False)
        self.pack()
        self.board = chess.Board(FEN)
        self.create_widgets()
        self.update_canvas()

    def load_resources(self) -> None:
        self.resources = {}
        self.resources["bg"] = PhotoImage.open("./assets/board.jpg")
        self.resources["A"] = PhotoImage.open("./assets/ra.png")
        self.resources["B"] = PhotoImage.open("./assets/rb.png")
        self.resources["K"] = PhotoImage.open("./assets/rk.png")
        self.resources["N"] = PhotoImage.open("./assets/rn.png")
        self.resources["C"] = PhotoImage.open("./assets/rc.png")
        self.resources["P"] = PhotoImage.open("./assets/rp.png")
        self.resources["R"] = PhotoImage.open("./assets/rr.png")
        self.resources["a"] = PhotoImage.open("./assets/ba.png")
        self.resources["b"] = PhotoImage.open("./assets/bb.png")
        self.resources["k"] = PhotoImage.open("./assets/bk.png")
        self.resources["n"] = PhotoImage.open("./assets/bn.png")
        self.resources["c"] = PhotoImage.open("./assets/bc.png")
        self.resources["p"] = PhotoImage.open("./assets/bp.png")
        self.resources["r"] = PhotoImage.open("./assets/br.png")
        self.resources["box"] = PhotoImage.open("./assets/ns.png")
        self.resources["red_box"] = PhotoImage.open("./assets/nr.png")
        self.resources["checkmate"] = PhotoImage.open("./assets/checkmate.png")

    def create_widgets(self) -> None:
        self.canvas = tk.Canvas(
            self, bg="white", height=420, width=380, highlightthickness=0
        )
        self.canvas.bind("<Button-1>", self.handle_click)
        self.button0 = tk.Button(self, text="翻转棋盘", command=self.rotate_board)
        self.button1 = tk.Button(self, text="悔棋", command=self.pop)
        self.button2 = tk.Button(self, text="重新开始", command=self.reset)
        self.canvas.pack()
        self.button0.pack(side="left", pady=10)
        self.button1.pack(side="left", pady=10)
        self.button2.pack(side="left", pady=10)

    def rotate_board(self):
        self.rotate = not self.rotate
        self.update_canvas()

    def reset(self):
        is_reset = messagebox.askokcancel(message="是否重新开始？")
        if not is_reset:
            return
        if self.think_thread:
            self.think_thread.stop()
        self.board = chess.Board()
        self.boxs.clear()
        self.moves.clear()
        self.pieces.clear()
        self.select_square = None
        self.checkmate = False
        self.update_canvas()

    def pop(self):
        if self.checkmate:
            return
        if self.think_thread:
            self.think_thread.stop()
        self.board.pop()
        if self.board.turn == chess.BLACK:
            self.board.pop()
        self.update_canvas()

    def handle_click(self, event: tk.Event):
        square = self.get_click_square(event.x, event.y)
        piece = self.board.piece_at(square)
        if piece and self.board.color_at(square) == self.board.turn:
            for id in self.boxs:
                self.canvas.delete(id)
            self.moves.clear()
            self.select_square = square
            self.boxs.append(self.create_box(square, color="red"))
            for m in self.board.generate_legal_moves(chess.BB_SQUARES[square]):
                self.moves.append(m)
                self.boxs.append(self.create_box(m.to_square))
        else:
            if self.select_square:
                move = chess.Move(self.select_square, square)
                if move in self.moves:
                    self.board.push(move)
                    self.update_canvas()
                    if self.board.is_checkmate():
                        self.checkmate = True
                        self.update_canvas()

    def rotate_square(self, square: chess.Square):
        return 255 - square - 1

    def create_piece(self, piece: chess.Piece, square: chess.Square) -> None:
        if self.rotate:
            square = self.rotate_square(square)
        x = (
            self.style["start_x"]
            + (chess.square_file(chess.SQUARES_180[square]) - 3) * self.style["space_x"]
        )
        y = (
            self.style["start_y"]
            + (chess.square_rank(chess.SQUARES_180[square]) - 3) * self.style["space_y"]
        )
        return self.canvas.create_image(
            x, y, image=self.resources[piece.symbol()], anchor="nw"
        )

    def create_box(self, square: chess.Square, color="blue"):
        box = "box" if color == "blue" else "red_box"
        if self.rotate:
            square = self.rotate_square(square)
        x = (
            self.style["start_x"]
            + (chess.square_file(chess.SQUARES_180[square]) - 3) * self.style["space_x"]
        )
        y = (
            self.style["start_y"]
            + (chess.square_rank(chess.SQUARES_180[square]) - 3) * self.style["space_y"]
        )
        return self.canvas.create_image(x, y, image=self.resources[box], anchor="nw")

    def get_click_square(self, x: int, y: int) -> chess.Square:
        file = (x - self.style["start_x"]) // self.style["space_x"] + 3
        rank = (y - self.style["start_y"]) // self.style["space_y"] + 3
        square = chess.msb(chess.BB_FILES[file] & chess.BB_RANKS[rank])
        if self.rotate:
            return self.rotate_square(chess.SQUARES_180[square])
        return chess.SQUARES_180[square]

    def update_canvas(self) -> None:
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.resources["bg"], anchor="nw")
        for square in chess.SQUARES_IN_BOARD:
            piece = self.board.piece_at(square)
            if piece:
                self.pieces.append(self.create_piece(piece, square))
        last_move = self.board.peek()
        if last_move:
            self.boxs.append(self.create_box(last_move.from_square))
            self.boxs.append(self.create_box(last_move.to_square))

        if self.checkmate:
            self.canvas.create_image(0, 0, image=self.resources["checkmate"], anchor="nw")
        self.canvas.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
