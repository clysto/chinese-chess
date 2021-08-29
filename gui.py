#!/usr/bin/env python3

import chess
import tkinter as tk
from tkinter import messagebox
import threading
from typing import Callable, Dict, List, Optional
from elephantfish import best_move
from PIL import Image, ImageTk

THINK_TIME = 5
# FEN = chess.STARTING_FEN
FEN = "5k3/9/5N3/9/9/8C/9/9/9/3K5 w - - 0 1"


class PhotoImage(ImageTk.PhotoImage):
    @classmethod
    def open(cls, fp):
        return cls(Image.open(fp))

    @classmethod
    def open_and_crop(cls, fp, x, y, w, h):
        im = Image.open(fp)
        im = im.crop((x, y, x + w, y + h))
        return cls(im)


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
    style = {"start_x": 15, "start_y": 15, "space_x": 60, "space_y": 60}
    boxs = []
    select_square: Optional[chess.Square] = None
    board: chess.Board
    rotate = False

    def __init__(self) -> None:
        self.master = tk.Tk()
        super().__init__(self.master)
        self.load_resources()
        self.master.title("中国象棋")
        self.master.resizable(False, False)
        self.pack()
        self.board = chess.Board(FEN)
        self.create_widgets()
        self.update_canvas()

    def load_resources(self) -> None:
        self.resources = {}
        self.resources["bg"] = PhotoImage.open("./assets/board.jpg")
        all_pieces = ["R", "N", "B", "A", "K", "C", "P", "r", "n", "b", "a", "k", "c", "p", "red_box", "blue_box"]
        for offset, piece in enumerate(all_pieces):
            self.resources[piece] = PhotoImage.open_and_crop("./assets/pieces.png", 0, offset * 60, 60, 60)
        self.resources["checkmate"] = PhotoImage.open("./assets/checkmate.png")

    def create_widgets(self) -> None:
        self.canvas = tk.Canvas(
            self, bg="white", height=630, width=570, highlightthickness=0
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
        self.board = chess.Board()
        self.boxs.clear()
        self.select_square = None
        self.update_canvas()

    def pop(self):
        if self.board.is_checkmate():
            return
        self.board.pop()
        self.update_canvas()

    def handle_click(self, event: tk.Event):
        if self.board.is_checkmate():
            return
        square = self.get_click_square(event.x, event.y)
        piece = self.board.piece_at(square)
        if piece and self.board.color_at(square) == self.board.turn:
            self.select_square = square
            self.update_canvas()
        else:
            if self.select_square:
                move = chess.Move(self.select_square, square)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.select_square = None
                    self.update_canvas()
                    if self.board.is_checkmate():
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
        box = "blue_box" if color == "blue" else "red_box"
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
                self.create_piece(piece, square)
        last_move = self.board.peek()

        if self.select_square:
            self.create_box(self.select_square, color="red")
            for move in filter(lambda x: x.from_square == self.select_square, self.board.legal_moves):
                self.create_box(move.to_square)

        elif last_move:
            self.create_box(last_move.from_square)
            self.create_box(last_move.to_square)

        if self.board.is_checkmate():
            self.canvas.create_image(0, 0, image=self.resources["checkmate"], anchor="nw")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
