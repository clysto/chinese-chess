#!/usr/bin/env python3

import sys
import threading
import tkinter as tk
from os.path import abspath
from tkinter import messagebox
from typing import Callable, Dict

from PIL import Image, ImageTk

import chess

FEN = chess.STARTING_FEN
SELF_PLAY, COMPUTER_PLAY = 1, 2
THINK_TIME = 1

sys.path.append(abspath('searcher'))

from elephantfish import Searcher

from searcher.tools import parseFEN, search


class ThinkThread(threading.Thread):
    def __init__(self, board: chess.Board, think_time: int, on_finish: Callable):
        threading.Thread.__init__(self)
        self.board = board
        self.think_time = think_time
        self.on_finish = on_finish

    def run(self):
        pos = parseFEN(self.board.fen())
        move, _, _ = search(Searcher(), pos, THINK_TIME)
        from_square, to_square = move
        from_square = chess.SQUARES_180[from_square]
        to_square = chess.SQUARES_180[to_square]
        if self.board.turn == chess.BLACK:
            from_square = 255 - from_square - 1
            to_square = 255 - to_square - 1
        move = chess.Move(from_square, to_square)
        if self.on_finish:
            self.on_finish(move)

    def stop(self):
        self.on_finish = None


class PhotoImage(ImageTk.PhotoImage):
    @classmethod
    def open(cls, fp):
        return cls(Image.open(fp))

    @classmethod
    def open_and_crop(cls, fp, x, y, w, h):
        im = Image.open(fp)
        im = im.crop((x, y, x + w, y + h))
        return cls(im)


class Application(tk.Frame):

    resources: Dict[str, PhotoImage]
    style = {"start_x": 15, "start_y": 45, "space_x": 60, "space_y": 60}
    select_square: chess.Square = None
    board: chess.Board
    rotate = False
    mode = SELF_PLAY

    def __init__(self) -> None:
        self.master = tk.Tk()
        super().__init__(self.master)
        self.load_resources()
        self.master.title("中国象棋")
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()
        self.reset()

    def load_resources(self) -> None:
        self.resources = {}
        self.resources["bg"] = PhotoImage.open("./assets/board.png")
        self.resources["bg_r"] = PhotoImage.open("./assets/board_rotate.png")
        all_pieces = ["R", "N", "B", "A", "K", "C", "P", "r", "n", "b", "a", "k", "c", "p", "red_box", "blue_box"]
        for offset, piece in enumerate(all_pieces):
            self.resources[piece] = PhotoImage.open_and_crop("./assets/pieces.png", 0, offset * 60, 60, 60)
        self.resources["checkmate"] = PhotoImage.open("./assets/checkmate.png")
        self.resources["check"] = PhotoImage.open("./assets/check.png")

    def create_widgets(self) -> None:
        self.canvas = tk.Canvas(self, bg="white", height=690, width=570, highlightthickness=0)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.button0 = tk.Button(self, text="翻转棋盘", command=self.rotate_board)
        self.button1 = tk.Button(self, text="悔棋", command=self.pop)
        self.button2 = tk.Button(self, text="自我对战", command=self.confirm_reset)
        self.button3 = tk.Button(self, text="人机对战", command=self.show_options)
        self.canvas.pack()
        self.button0.pack(side="left", pady=10)
        self.button1.pack(side="left", pady=10)
        self.button2.pack(side="left", pady=10)
        self.button3.pack(side="left", pady=10)

    def show_options(self) -> None:
        self.options_frame = tk.Toplevel(self, borderwidth=20)
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.options_frame.geometry("+%d+%d" % (x + 200, y + 200))
        self.options_frame.resizable(False, False)
        self.computer_side = tk.BooleanVar(self)
        label = tk.Label(self.options_frame, text="电脑")
        label.grid(row=0, column=0)
        red_button = tk.Radiobutton(self.options_frame, text="红", variable=self.computer_side, value=chess.RED)
        red_button.grid(row=0, column=1)
        black_button = tk.Radiobutton(self.options_frame, text="黑", variable=self.computer_side, value=chess.BLACK)
        black_button.select()
        black_button.grid(row=0, column=2)
        start_button = tk.Button(self.options_frame, text="开始挑战", command=self.start_game)
        start_button.grid(row=1, column=0, columnspan=3)
        self.options_frame.update()

    def start_game(self) -> None:
        self.options_frame.destroy()
        self.mode = COMPUTER_PLAY
        self.reset()
        if self.computer_side.get() == chess.RED:
            self.rotate = True
            self.update_canvas()
            self.computer_move()

    def rotate_board(self) -> None:
        self.rotate = not self.rotate
        self.update_canvas()

    def confirm_reset(self) -> None:
        is_reset = messagebox.askokcancel(message="是否重新开始？")
        if not is_reset:
            return
        self.mode = SELF_PLAY
        self.reset()

    def reset(self) -> None:
        self.board = chess.Board(FEN)
        self.select_square = None
        self.update_canvas()

    def pop(self) -> None:
        if self.board.is_checkmate():
            return
        if self.mode == COMPUTER_PLAY and self.board.turn == self.computer_side.get():
            # 电脑思考时不能悔棋
            return
        if self.mode == COMPUTER_PLAY:
            self.board.pop()
        self.board.pop()
        self.select_square = None
        self.update_canvas()

    def computer_move(self) -> None:
        def on_finish(move):
            self.push(move)
        ThinkThread(self.board, 1, on_finish).start()

    def handle_click(self, event: tk.Event) -> None:
        if self.board.is_checkmate():
            return
        square = self.get_click_square(event.x, event.y)
        piece = self.board.piece_at(square)

        if self.mode == SELF_PLAY:
            my_color = self.board.turn
        else:
            my_color = not self.computer_side.get()

        if piece and self.board.color_at(square) == my_color and my_color == self.board.turn:
            self.select_square = square
            self.update_canvas()
        elif self.select_square:
            move = chess.Move(self.select_square, square)
            if move in self.board.legal_moves:
                self.push(move)
                if self.mode == COMPUTER_PLAY:
                    self.computer_move()

    def push(self, move: chess.Move):
        print(self.board.chinese_move(move, full_width=True))
        self.board.push(move)
        self.select_square = None
        self.update_canvas()
        if self.board.is_checkmate():
            self.update_canvas()
        elif self.board.is_check():
            self.update_canvas()
            check_image = self.canvas.create_image(0, 30, image=self.resources["check"], anchor="nw")

            def delete_check_image():
                self.canvas.delete(check_image)

            self.canvas.after(500, delete_check_image)

    def rotate_square(self, square: chess.Square) -> chess.Square:
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
        self.canvas.create_image(x, y, image=self.resources[piece.symbol()], anchor="nw")

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
        self.canvas.create_image(x, y, image=self.resources[box], anchor="nw")

    def get_click_square(self, x: int, y: int) -> chess.Square:
        file = (x - self.style["start_x"]) // self.style["space_x"] + 3
        rank = (y - self.style["start_y"]) // self.style["space_y"] + 3
        square = chess.msb(chess.BB_FILES[file] & chess.BB_RANKS[rank])
        if self.rotate:
            return self.rotate_square(chess.SQUARES_180[square])
        return chess.SQUARES_180[square]

    def update_canvas(self) -> None:
        self.canvas.delete("all")
        if self.rotate:
            self.canvas.create_image(0, 0, image=self.resources["bg_r"], anchor="nw")
        else:
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
            self.canvas.create_image(0, 30, image=self.resources["checkmate"], anchor="nw")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
