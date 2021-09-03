from __future__ import annotations

import dataclasses
import typing
from typing import (Dict, Generic, Iterable, Iterator, List, Optional, Tuple,
                    TypeVar)

Color = bool
COLORS = [RED, BLACK] = [True, False]
COLOR_NAMES = ["black", "red"]


PieceType = int
PIECE_TYPES = [PAWN, CANNON, ROOK, KNIGHT, BISHOP, ADVISOR, KING] = range(1, 8)
PIECE_SYMBOLS = [None, "p", "c", "r", "n", "b", "a", "k"]
PIECES_NAMES = {
    "R": "车", "r": "俥",
    "N": "马", "n": "傌",
    "B": "相", "b": "象",
    "A": "仕", "a": "士",
    "K": "帅", "k": "将",
    "P": "兵", "p": "卒",
    "C": "炮", "c": "砲",
}

ACTION_NAMES = {".": "平", "+": "进", "-": "退"}
POSITION_NAMES = {".": "中", "+": "前", "-": "后", "a": "一", "b": "二", "c": "三", "d": "四", "e": "五"}


def piece_symbol(piece_type: PieceType) -> str:
    return typing.cast(str, PIECE_SYMBOLS[piece_type])


FILE_NAMES = [None, None, None, "a", "b", "c", "d", "e", "f", "g", "h", "i", None, None, None, None]
CHINESE_NUMBERS = [None, "一", "二", "三", "四", "五", "六", "七", "八", "九"]
RANK_NAMES = [None, None, None, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", None, None, None]

STARTING_FEN = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
STARTING_BOARD_FEN = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR"

Square = int
SQUARES = [
    __, __, __, __, __, __, __, __, __, __, __, __, __, __, __, __,
    __, __, __, __, __, __, __, __, __, __, __, __, __, __, __, __,
    __, __, __, __, __, __, __, __, __, __, __, __, __, __, __, __,
    __, __, __, A0, B0, C0, D0, E0, F0, G0, H0, I0, __, __, __, __,
    __, __, __, A1, B1, C1, D1, E1, F1, G1, H1, I1, __, __, __, __,
    __, __, __, A2, B2, C2, D2, E2, F2, G2, H2, I2, __, __, __, __,
    __, __, __, A3, B3, C3, D3, E3, F3, G3, H3, I3, __, __, __, __,
    __, __, __, A4, B4, C4, D4, E4, F4, G4, H4, I4, __, __, __, __,
    __, __, __, A5, B5, C5, D5, E5, F5, G5, H5, I5, __, __, __, __,
    __, __, __, A6, B6, C6, D6, E6, F6, G6, H6, I6, __, __, __, __,
    __, __, __, A7, B7, C7, D7, E7, F7, G7, H7, I7, __, __, __, __,
    __, __, __, A8, B8, C8, D8, E8, F8, G8, H8, I8, __, __, __, __,
    __, __, __, A9, B9, C9, D9, E9, F9, G9, H9, I9, __, __, __, __,
    __, __, __, __, __, __, __, __, __, __, __, __, __, __, __, __,
    __, __, __, __, __, __, __, __, __, __, __, __, __, __, __, __,
    __, __, __, __, __, __, __, __, __, __, __, __, __, __, __, __,
] = range(256)

SQUARE_NAMES = [
    f + r if f and r else None for r in RANK_NAMES for f in FILE_NAMES]


def square_file(square: Square) -> int:
    return square & 0xf


def square_file_wxf(square: Square, color: Color) -> int:
    if color == BLACK:
        return square_file(square) - 2
    else:
        return 10 - (square_file(square) - 2)


def square_rank(square: Square) -> int:
    return square >> 4


def square_in_board(square: Square) -> bool:
    return bool(BB_SQUARES[square] & BB_IN_BOARD)


def square_distance(a: Square, b: Square) -> int:
    return max(abs(square_file(a) - square_file(b)), abs(square_rank(a) - square_rank(b)))


def square_mirror(square: Square) -> Square:
    return square ^ 0xf0


SQUARES_180 = [square_mirror(sq) for sq in SQUARES]


Bitboard = int
BB_EMPTY = 0
BB_ALL = 0xffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff
BB_IN_BOARD = 0x0000_0000_0000_0ff8_0ff8_0ff8_0ff8_0ff8_0ff8_0ff8_0ff8_0ff8_0ff8_0000_0000_0000
BB_RED_SIDE = 0x0000_0000_0000_0000_0000_0000_0000_0000_ffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff
BB_BLACK_SIDE = 0xffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff_0000_0000_0000_0000_0000_0000_0000_0000


def print_bitboard(bb: Bitboard) -> None:
    bb = bb & (2**256 - 1)
    s = format(bb, '0256b').replace("1", "@").replace("0", ".")
    for i in range(3, 13):
        print(f"{12-i} " + " ".join(s[i * 16 + 16 - 1 - 3:i * 16 - 1 + 4:-1]))
    print("  a b c d e f g h i")


BB_SQUARES = [
    _, _, _, _____, _____, _____, _____, _____, _____, _____, _____, _____, _, _, _, _,
    _, _, _, _____, _____, _____, _____, _____, _____, _____, _____, _____, _, _, _, _,
    _, _, _, _____, _____, _____, _____, _____, _____, _____, _____, _____, _, _, _, _,
    _, _, _, BB_A0, BB_B0, BB_C0, BB_D0, BB_E0, BB_F0, BB_G0, BB_H0, BB_I0, _, _, _, _,
    _, _, _, BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1, BB_I1, _, _, _, _,
    _, _, _, BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2, BB_I2, _, _, _, _,
    _, _, _, BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3, BB_I3, _, _, _, _,
    _, _, _, BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4, BB_I4, _, _, _, _,
    _, _, _, BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5, BB_I5, _, _, _, _,
    _, _, _, BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6, BB_I6, _, _, _, _,
    _, _, _, BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7, BB_I7, _, _, _, _,
    _, _, _, BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8, BB_I8, _, _, _, _,
    _, _, _, BB_A9, BB_B9, BB_C9, BB_D9, BB_E9, BB_F9, BB_G9, BB_H9, BB_I9, _, _, _, _,
    _, _, _, _____, _____, _____, _____, _____, _____, _____, _____, _____, _, _, _, _,
    _, _, _, _____, _____, _____, _____, _____, _____, _____, _____, _____, _, _, _, _,
    _, _, _, _____, _____, _____, _____, _____, _____, _____, _____, _____, _, _, _, _,
] = [1 << sq for sq in SQUARES]

BB_CORNERS = BB_A0 | BB_I0 | BB_A9 | BB_I9
BB_RED_PAWNS = BB_A3 | BB_C3 | BB_E3 | BB_G3 | BB_I3
BB_BLACK_PAWNS = BB_A6 | BB_C6 | BB_E6 | BB_G6 | BB_I6

BB_IN_PALACE = (BB_D0 | BB_E0 | BB_F0 | BB_D1 | BB_E1 | BB_F1 | BB_D2 | BB_E2 | BB_F2 |
                BB_D7 | BB_E7 | BB_F7 | BB_D8 | BB_E8 | BB_F8 | BB_D9 | BB_E9 | BB_F9)

SQUARES_IN_BOARD = [sq for sq in SQUARES if BB_SQUARES[sq] & BB_IN_BOARD]

BB_FILES = [
    _, _, _,
    BB_FILE_A,
    BB_FILE_B,
    BB_FILE_C,
    BB_FILE_D,
    BB_FILE_E,
    BB_FILE_F,
    BB_FILE_G,
    BB_FILE_H,
    BB_FILE_I,
    _, _, _, _,
] = [0x0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001 << i for i in range(16)]

BB_RANKS = [
    _, _, _,
    BB_RANK_0,
    BB_RANK_1,
    BB_RANK_2,
    BB_RANK_3,
    BB_RANK_4,
    BB_RANK_5,
    BB_RANK_6,
    BB_RANK_7,
    BB_RANK_8,
    BB_RANK_9,
    _, _, _,
] = [0xffff << (16 * i) for i in range(16)]

BB_SQUARES_BISHOP = BB_C0 | BB_G0 | BB_A2 | BB_E2 | BB_I2 | BB_C4 | BB_G4 | BB_C5 | BB_G5 | BB_A7 | BB_E7 | BB_I7 | BB_C9 | BB_G9
BB_SQUARES_ADVISOR = BB_D0 | BB_F0 | BB_E1 | BB_D2 | BB_F2 | BB_D7 | BB_F7 | BB_E8 | BB_D9 | BB_F9


def msb(bb: Bitboard) -> int:
    return bb.bit_length() - 1


def scan_reversed(bb: Bitboard) -> Iterator[Square]:
    while bb:
        r = bb.bit_length() - 1
        yield r
        bb ^= BB_SQUARES[r]


def count_ones(bb: Bitboard):
    s = 0
    t = {'0': 0, '1': 1, '2': 1, '3': 2, '4': 1, '5': 2, '6': 2, '7': 3}
    for c in oct(bb)[2:]:
        s += t[c]
    return s


def between(a: Square, b: Square) -> Bitboard:
    file_a, file_b = square_file(a), square_file(b)
    rank_a, rank_b = square_rank(a), square_rank(b)
    if file_a == file_b:
        bb = BB_FILES[file_a] & ((BB_ALL << a) ^ (BB_ALL << b))
    elif rank_a == rank_b:
        bb = BB_RANKS[rank_a] & ((BB_ALL << a) ^ (BB_ALL << b))
    else:
        bb = BB_EMPTY
    return bb & (bb - 1)


def line(a: Square, b: Square) -> Bitboard:
    file_a, file_b = square_file(a), square_file(b)
    rank_a, rank_b = square_rank(a), square_rank(b)
    if file_a == file_b:
        return BB_FILES[file_a]
    elif rank_a == rank_b:
        return BB_RANKS[rank_a]
    else:
        return BB_EMPTY


def _sliding_attacks(square: Square, occupied: Bitboard, deltas: Iterable[int]) -> Bitboard:
    attacks = BB_EMPTY

    for delta in deltas:
        sq = square
        while True:
            sq += delta
            if not (0 <= sq < 256) or square_distance(sq, sq - delta) > 2:
                break

            attacks |= BB_SQUARES[sq]

            if occupied & BB_SQUARES[sq]:
                break

    return attacks


def _rook_attacks(square: Square, occupied: Bitboard):
    return _sliding_attacks(square, occupied, [16, -16, -1, 1])


def _cannon_attacks(square: Square, occupied: Bitboard) -> Bitboard:
    attacks = BB_EMPTY
    deltas = [16, -16, -1, 1]
    for delta in deltas:
        hops = 0
        sq = square
        while True:
            sq += delta
            if not (0 <= sq < 256) or square_distance(sq, sq - delta) > 2:
                break

            if occupied & BB_SQUARES[sq]:
                if hops == 1:
                    attacks |= BB_SQUARES[sq]
                    break
                else:
                    hops += 1

    return attacks


def _step_attacks(square: Square, deltas: Iterable[int]) -> Bitboard:
    return _sliding_attacks(square, BB_ALL, deltas)


def _pawn_attacks(reverse=False) -> List[List[Bitboard]]:
    attacks = [[], []]
    direction = -1 if reverse else 1
    for sq in SQUARES:
        # 红兵
        if sq > I4:
            # 过河兵
            attacks[RED].append(_step_attacks(sq, [-1, 16 * direction, 1]))
        else:
            attacks[RED].append(_step_attacks(sq, [16 * direction]))
    for sq in SQUARES:
        # 黑卒
        if sq < A5:
            # 过河兵
            attacks[BLACK].append(_step_attacks(sq, [-1, -16 * direction, 1]))
        else:
            attacks[BLACK].append(_step_attacks(sq, [-16 * direction]))
    return attacks


def _knight_attacks(reverse=False) -> Tuple[List[Bitboard], List[Dict[Bitboard, Bitboard]]]:
    mask_table = []
    attack_table = []
    knight_deltas = [33, 31, -14, 18, -33, -31, -18, 14] if not reverse else [14, 31, 33, 18, -14, -31, -18, -33]
    directions = [16, 1, -16, -1] if not reverse else [15, 17, -15, -17]
    for square in SQUARES:
        if not square_in_board(square):
            attack_table.append({BB_EMPTY: BB_EMPTY})
            mask_table.append(BB_EMPTY)
            continue
        attacks = {}
        mask = BB_EMPTY
        for d in directions:
            mask |= BB_SQUARES[square + d]

        for i in range(0xf):
            # 马脚位置
            subset = BB_EMPTY
            deltas = []
            for j in range(4):
                if i >> j & 1:
                    # 别马脚
                    subset |= BB_SQUARES[square + directions[j]]
                else:
                    deltas.append(knight_deltas[2 * j])
                    deltas.append(knight_deltas[2 * j + 1])
            attacks[subset] = _step_attacks(square, deltas)

        attack_table.append(attacks)
        mask_table.append(mask)
    return mask_table, attack_table


def _bishop_attacks() -> List[Bitboard]:
    mask_table = []
    attack_table = []
    directions = [15, 17, -15, -17]
    for square in SQUARES:
        square_side = BB_RED_SIDE if BB_SQUARES[square] & BB_RED_SIDE else BB_BLACK_SIDE
        if not (BB_SQUARES[square] & BB_SQUARES_BISHOP):
            attack_table.append({BB_EMPTY: BB_EMPTY})
            mask_table.append(BB_EMPTY)
            continue
        attacks = {}
        mask = BB_EMPTY
        for d in directions:
            mask |= BB_SQUARES[square + d]
        for i in range(0xf):
            # 象眼位置
            subset = BB_EMPTY
            deltas = []
            for j in range(4):
                if i >> j & 1:
                    # 塞象眼
                    subset |= BB_SQUARES[square + directions[j]]
                else:
                    deltas.append(2 * directions[j])
            attacks[subset] = _step_attacks(square, deltas) & square_side
        attack_table.append(attacks)
        mask_table.append(mask)
    return mask_table, attack_table


def _king_attacks() -> List[Bitboard]:
    attacks = []
    for square in SQUARES:
        if not(BB_SQUARES[square] & BB_IN_PALACE):
            attacks.append(BB_EMPTY)
            continue
        attacks.append(_step_attacks(square, [-16, 16, 1, -1]) & BB_IN_PALACE)
    return attacks


def _advisor_attacks() -> List[Bitboard]:
    attacks = []
    for square in SQUARES:
        if not(BB_SQUARES[square] & BB_SQUARES_ADVISOR):
            attacks.append(BB_EMPTY)
            continue
        attacks.append(_step_attacks(square, [15, 17, -15, -17]) & BB_IN_PALACE)
    return attacks


def _knight_blocker(king: Square, knight: Square) -> Bitboard:
    masks = [BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king + 15],
             BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king + 17],
             BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king - 15],
             BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king - 17],
             ]
    for mask in masks:
        if BB_KNIGHT_REVERSED_ATTACKS[king][mask] & BB_SQUARES[knight]:
            return BB_KNIGHT_REVERSED_MASKS[king] & ~mask
    return BB_EMPTY


BB_KNIGHT_MASKS, BB_KNIGHT_ATTACKS = _knight_attacks()
BB_KNIGHT_REVERSED_MASKS, BB_KNIGHT_REVERSED_ATTACKS = _knight_attacks(reverse=True)
BB_BISHOP_MASKS, BB_BISHOP_ATTACKS = _bishop_attacks()
BB_PAWN_ATTACKS = _pawn_attacks()
BB_PAWN_REVERSED_ATTACKS = _pawn_attacks(reverse=True)
BB_KING_ATTACKS = _king_attacks()
BB_ADVISOR_ATTACKS = _advisor_attacks()


@dataclasses.dataclass
class Piece:

    piece_type: PieceType

    color: Color

    def symbol(self) -> str:
        symbol = piece_symbol(self.piece_type)
        return symbol.upper() if self.color else symbol

    def chinese(self) -> str:
        symbol = piece_symbol(self.piece_type)
        name = PIECES_NAMES[symbol.upper() if self.color else symbol]
        return name

    def __hash__(self) -> int:
        return self.piece_type + (-1 if self.color else 6)

    def __repr__(self) -> str:
        return f"Piece.from_symbol({self.symbol()!r})"

    def __str__(self) -> str:
        return self.symbol()

    @classmethod
    def from_symbol(cls, symbol: str) -> Piece:
        return cls(PIECE_SYMBOLS.index(symbol.lower()), symbol.isupper())


@dataclasses.dataclass(unsafe_hash=True)
class Move:

    from_square: Square

    to_square: Square

    def iccs(self) -> str:
        if self:
            return SQUARE_NAMES[self.from_square] + SQUARE_NAMES[self.to_square]
        else:
            return "0000"

    def __bool__(self) -> bool:
        return bool(self.from_square or self.to_square)

    def __repr__(self) -> str:
        return f"Move.from_uci({self.iccs()!r})"

    def __str__(self) -> str:
        return self.iccs()

    @classmethod
    def from_iccs(cls, iccs: str) -> Move:
        if iccs == "0000":
            return cls.null()
        elif len(iccs) == 4:
            from_square = SQUARE_NAMES.index(iccs[:2])
            to_square = SQUARE_NAMES.index(iccs[2:])
            return cls(from_square, to_square)
        else:
            raise ValueError(f"expected iccs string to be of length 4: {iccs!r}")

    @classmethod
    def null(cls) -> Move:
        return cls(0, 0)


BoardT = TypeVar("BoardT", bound="Board")


class _BoardState(Generic[BoardT]):

    def __init__(self, board: BoardT) -> None:
        self.pawns = board.pawns
        self.knights = board.knights
        self.bishops = board.bishops
        self.rooks = board.rooks
        self.cannons = board.cannons
        self.advisors = board.advisors
        self.kings = board.kings

        self.occupied_r = board.occupied_co[RED]
        self.occupied_b = board.occupied_co[BLACK]
        self.occupied = board.occupied

        self.turn = board.turn
        self.fullmove_number = board.fullmove_number

    def restore(self, board: BoardT) -> None:
        board.pawns = self.pawns
        board.knights = self.knights
        board.bishops = self.bishops
        board.rooks = self.rooks
        board.cannons = self.cannons
        board.advisors = self.advisors
        board.kings = self.kings

        board.occupied_co[RED] = self.occupied_r
        board.occupied_co[BLACK] = self.occupied_b
        board.occupied = self.occupied

        board.turn = self.turn
        board.fullmove_number = self.fullmove_number


class BaseBoard:

    def __init__(self, board_fen: Optional[str] = STARTING_BOARD_FEN) -> None:
        self.occupied_co = [BB_EMPTY, BB_EMPTY]
        if board_fen is None:
            self._clear_board()
        elif board_fen == STARTING_BOARD_FEN:
            self._reset_board()
        else:
            self._set_board_fen(board_fen)

    def _reset_board(self) -> None:
        self.pawns = BB_RED_PAWNS | BB_BLACK_PAWNS
        self.knights = BB_B0 | BB_H0 | BB_B9 | BB_H9
        self.bishops = BB_C0 | BB_G0 | BB_C9 | BB_G9
        self.rooks = BB_CORNERS
        self.cannons = BB_B2 | BB_H2 | BB_B7 | BB_H7
        self.advisors = BB_D0 | BB_F0 | BB_D9 | BB_F9
        self.kings = BB_E0 | BB_E9

        self.occupied_co[RED] = BB_RANK_0 | BB_B2 | BB_H2 | BB_RED_PAWNS
        self.occupied_co[BLACK] = BB_RANK_9 | BB_B7 | BB_H7 | BB_BLACK_PAWNS
        self.occupied = self.occupied_co[RED] | self.occupied_co[BLACK]

    def reset_board(self) -> None:
        self._reset_board()

    def _clear_board(self) -> None:
        self.pawns = BB_EMPTY
        self.knights = BB_EMPTY
        self.bishops = BB_EMPTY
        self.rooks = BB_EMPTY
        self.cannons = BB_EMPTY
        self.advisors = BB_EMPTY
        self.kings = BB_EMPTY

        self.occupied_co[RED] = BB_EMPTY
        self.occupied_co[BLACK] = BB_EMPTY
        self.occupied = BB_EMPTY

    def clear_board(self) -> None:
        self._clear_board()

    def _set_board_fen(self, fen: str) -> None:
        fen = fen.strip()
        if " " in fen:
            raise ValueError(f"expected position part of fen, got multiple parts: {fen!r}")

        rows = fen.split("/")
        if len(rows) != 10:
            raise ValueError(f"expected 9 rows in position part of fen: {fen!r}")

        for row in rows:
            field_sum = 0
            previous_was_digit = False

            for c in row:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if previous_was_digit:
                        raise ValueError(f"two subsequent digits in position part of fen: {fen!r}")
                    field_sum += int(c)
                    previous_was_digit = True
                elif c.lower() in PIECE_SYMBOLS:
                    field_sum += 1
                    previous_was_digit = False
                else:
                    raise ValueError(f"invalid character in position part of fen: {fen!r}")

            if field_sum != 9:
                raise ValueError(f"expected 9 columns per row in position part of fen: {fen!r}")

        self._clear_board()
        square_index = A0
        for c in fen:
            if c in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                square_index += int(c)
            elif c.lower() in PIECE_SYMBOLS:
                piece = Piece.from_symbol(c)
                self._set_piece_at(SQUARES_180[square_index], piece.piece_type, piece.color)
                square_index += 1
            else:
                square_index += 7

    def set_board_fen(self, fen: str) -> None:
        self._set_board_fen(fen)

    def board_fen(self) -> str:
        builder = []
        empty = 0

        for square in SQUARES_180:
            if not square_in_board(square):
                continue

            piece = self.piece_at(square)

            if not piece:
                empty += 1
            else:
                if empty:
                    builder.append(str(empty))
                    empty = 0
                builder.append(piece.symbol())

            if BB_SQUARES[square] & BB_FILE_I:
                if empty:
                    builder.append(str(empty))
                    empty = 0

                if square != I0:
                    builder.append("/")

        return "".join(builder)

    def _remove_piece_at(self, square: Square) -> Optional[PieceType]:
        piece_type = self.piece_type_at(square)
        mask = BB_SQUARES[square]

        if piece_type == PAWN:
            self.pawns ^= mask
        elif piece_type == KNIGHT:
            self.knights ^= mask
        elif piece_type == BISHOP:
            self.bishops ^= mask
        elif piece_type == ROOK:
            self.rooks ^= mask
        elif piece_type == CANNON:
            self.cannons ^= mask
        elif piece_type == KING:
            self.kings ^= mask
        elif piece_type == ADVISOR:
            self.advisors ^= mask
        else:
            return None

        self.occupied ^= mask
        self.occupied_co[RED] &= ~mask
        self.occupied_co[BLACK] &= ~mask

        return piece_type

    def remove_piece_at(self, square: Square) -> Optional[Piece]:
        color = bool(self.occupied_co[RED] & BB_SQUARES[square])
        piece_type = self._remove_piece_at(square)
        return Piece(piece_type, color) if piece_type else None

    def _set_piece_at(self, square: Square, piece_type: PieceType, color: Color) -> None:
        self._remove_piece_at(square)

        mask = BB_SQUARES[square]

        if piece_type == PAWN:
            self.pawns |= mask
        elif piece_type == KNIGHT:
            self.knights |= mask
        elif piece_type == BISHOP:
            self.bishops |= mask
        elif piece_type == ROOK:
            self.rooks |= mask
        elif piece_type == CANNON:
            self.cannons |= mask
        elif piece_type == KING:
            self.kings |= mask
        elif piece_type == ADVISOR:
            self.advisors |= mask
        else:
            return

        self.occupied ^= mask
        self.occupied_co[color] ^= mask

    def set_piece_at(self, square: Square, piece: Optional[Piece]) -> None:
        if piece is None:
            self._remove_piece_at(square)
        else:
            self._set_piece_at(square, piece.piece_type, piece.color)

    def pieces_mask(self, piece_type: PieceType, color: Color) -> Bitboard:
        if piece_type == PAWN:
            bb = self.pawns
        elif piece_type == KNIGHT:
            bb = self.knights
        elif piece_type == BISHOP:
            bb = self.bishops
        elif piece_type == ROOK:
            bb = self.rooks
        elif piece_type == CANNON:
            bb = self.cannons
        elif piece_type == ADVISOR:
            bb = self.advisors
        elif piece_type == KING:
            bb = self.kings
        else:
            assert False, f"expected PieceType, got {piece_type!r}"

        return bb & self.occupied_co[color]

    def piece_at(self, square: Square) -> Optional[Piece]:
        piece_type = self.piece_type_at(square)
        if piece_type:
            mask = BB_SQUARES[square]
            color = bool(self.occupied_co[RED] & mask)
            return Piece(piece_type, color)
        else:
            return None

    def piece_type_at(self, square: Square) -> Optional[PieceType]:
        mask = BB_SQUARES[square]

        if not self.occupied & mask:
            return None
        elif self.pawns & mask:
            return PAWN
        elif self.knights & mask:
            return KNIGHT
        elif self.bishops & mask:
            return BISHOP
        elif self.rooks & mask:
            return ROOK
        elif self.cannons & mask:
            return CANNON
        elif self.advisors & mask:
            return ADVISOR
        else:
            return KING

    def color_at(self, square: Square) -> Optional[Color]:
        mask = BB_SQUARES[square]
        if self.occupied_co[RED] & mask:
            return RED
        elif self.occupied_co[BLACK] & mask:
            return BLACK
        else:
            return None

    def king(self, color: Color) -> Optional[Square]:
        king_mask = self.occupied_co[color] & self.kings
        return msb(king_mask) if king_mask else None

    def attacks_mask(self, square: Square) -> Bitboard:
        bb_square = BB_SQUARES[square]

        if bb_square & self.pawns:
            color = bool(bb_square & self.occupied_co[RED])
            return BB_PAWN_ATTACKS[color][square]
        if bb_square & self.kings:
            # 老将对脸杀
            return BB_KING_ATTACKS[square] | (_rook_attacks(square, self.occupied) & self.kings)
        if bb_square & self.advisors:
            return BB_ADVISOR_ATTACKS[square]
        elif bb_square & self.knights:
            return BB_KNIGHT_ATTACKS[square][BB_KNIGHT_MASKS[square] & self.occupied]
        elif bb_square & self.bishops:
            return BB_BISHOP_ATTACKS[square][BB_BISHOP_MASKS[square] & self.occupied]
        elif bb_square & self.rooks:
            return _rook_attacks(square, self.occupied)
        elif bb_square & self.cannons:
            return (_cannon_attacks(square, self.occupied) |
                    (_rook_attacks(square, self.occupied) & ~self.occupied))
        else:
            return BB_EMPTY

    def _attackers_mask(self, color: Color, square: Square, occupied: Bitboard) -> Bitboard:
        cannon_attacks = _cannon_attacks(square, occupied)
        rook_attacks = _rook_attacks(square, occupied)
        attackers = (
            (cannon_attacks & self.cannons) |
            (rook_attacks & self.rooks) |
            (BB_KNIGHT_REVERSED_ATTACKS[square][occupied & BB_KNIGHT_REVERSED_MASKS[square]] & self.knights) |
            (BB_BISHOP_ATTACKS[square][occupied & BB_BISHOP_MASKS[square]] & self.bishops) |
            (BB_PAWN_REVERSED_ATTACKS[color][square] & self.pawns) |
            (BB_ADVISOR_ATTACKS[square] & self.advisors) |
            ((BB_KING_ATTACKS[square] | (rook_attacks & self.kings)) & self.kings)
        )
        return attackers & self.occupied_co[color]

    def attackers_mask(self, color: Color, square: Square) -> Bitboard:
        return self._attackers_mask(color, square, self.occupied)

    def is_attacked_by(self, color: Color, square: Square) -> bool:
        return bool(self.attackers_mask(color, square))

    def piece_map(self, *, mask: Bitboard = BB_IN_BOARD) -> Dict[Square, Piece]:
        result = {}
        for square in scan_reversed(self.occupied & mask):
            result[square] = typing.cast(Piece, self.piece_at(square))
        return result

    def __str__(self) -> str:
        builder = []

        for square in SQUARES_180:
            if not BB_SQUARES[square] & BB_IN_BOARD:
                continue

            piece = self.piece_at(square)

            if piece:
                builder.append(piece.symbol())
            else:
                builder.append(".")

            if BB_SQUARES[square] & BB_FILE_I:
                if square != I0:
                    builder.append("\n")
            else:
                builder.append(" ")

        return "".join(builder)

    def copy(self: BaseBoard) -> BaseBoard:
        board = type(self)(None)

        board.pawns = self.pawns
        board.knights = self.knights
        board.bishops = self.bishops
        board.rooks = self.rooks
        board.cannons = self.cannons
        board.advisors = self.advisors
        board.kings = self.kings

        board.occupied_co[RED] = self.occupied_co[RED]
        board.occupied_co[BLACK] = self.occupied_co[BLACK]
        board.occupied = self.occupied

        return board

    def chinese(self) -> str:
        builder = []

        for square in SQUARES_180:
            if not BB_SQUARES[square] & BB_IN_BOARD:
                continue

            piece = self.piece_at(square)

            if BB_SQUARES[square] & BB_FILE_A:
                builder.append(RANK_NAMES[square_rank(square)] + " ")

            if piece:
                builder.append(piece.chinese())
            else:
                builder.append("．")

            if BB_SQUARES[square] & BB_FILE_I:
                builder.append("\n")
        builder.append("  ａｂｃｄｅｆｇｈｉ")

        return "".join(builder)


class Board(BaseBoard):

    turn: Color

    fullmove_number: int

    move_stack: List[Move]

    def __init__(self: Board, fen: Optional[str] = STARTING_FEN) -> None:
        BaseBoard.__init__(self, None)
        self.move_stack = []
        self._stack: List[_BoardState[Board]] = []

        if fen is None:
            self.clear()
        elif fen == STARTING_FEN:
            self.reset()
        else:
            self.set_fen(fen)

    @property
    def legal_moves(self) -> LegalMoveGenerator:
        return LegalMoveGenerator(self)

    @property
    def pseudo_legal_moves(self) -> PseudoLegalMoveGenerator:
        return PseudoLegalMoveGenerator(self)

    def clear(self) -> None:
        self.turn = RED
        self.fullmove_number = 1
        self.clear_board()

    def reset(self) -> None:
        self.turn = RED
        self.fullmove_number = 1
        self.reset_board()

    def set_fen(self, fen: str) -> None:
        parts = fen.split()

        try:
            board_part = parts.pop(0)
        except IndexError:
            raise ValueError("empty fen")

        try:
            turn_part = parts.pop(0)
        except IndexError:
            turn = RED
        else:
            if turn_part == "w":
                turn = RED
            elif turn_part == "b":
                turn = BLACK
            else:
                raise ValueError(f"expected 'w' or 'b' for turn part of fen: {fen!r}")

        parts.pop(0)
        parts.pop(0)
        parts.pop(0)

        try:
            fullmove_part = parts.pop(0)
        except IndexError:
            fullmove_number = 1
        else:
            try:
                fullmove_number = int(fullmove_part)
            except ValueError:
                raise ValueError(f"invalid fullmove number in fen: {fen!r}")

            if fullmove_number < 0:
                raise ValueError(f"fullmove number cannot be negative: {fen!r}")

            fullmove_number = max(fullmove_number, 1)

        if parts:
            raise ValueError(f"fen string has more parts than expected: {fen!r}")

        self._set_board_fen(board_part)
        self.turn = turn
        self.fullmove_number = fullmove_number

    def checkers_mask(self) -> Bitboard:
        king = self.king(self.turn)
        return BB_EMPTY if king is None else self.attackers_mask(not self.turn, king)

    def is_check(self) -> bool:
        return bool(self.checkers_mask())

    def is_checkmate(self) -> bool:
        return not any(self.generate_legal_moves())

    def _is_safe(self, king: Square, slider_blockers: List[Tuple[Bitboard, Bitboard]],
                 knight_blockers: List[Tuple(Bitboard, Bitboard)], move: Move) -> bool:

        if move.from_square == king:
            # 把将去掉
            return not bool(self._attackers_mask(not self.turn, move.to_square, self.occupied & ~BB_SQUARES[king]))

        bb_from = BB_SQUARES[move.from_square]
        bb_to = BB_SQUARES[move.to_square]

        for blocker, to in knight_blockers:
            # 如果正在移动马腿棋子
            if blocker & bb_from and (not bb_to & to):
                return False

        for mask, sniper, limit in slider_blockers:
            # 如果正在移动阻挡棋子
            if mask & bb_from or mask & bb_to:
                if not (sniper & bb_to) and count_ones(self.occupied & mask & ~bb_from | bb_to & mask) == limit:
                    return False

        return True

    def is_pseudo_legal(self, move: Move) -> bool:
        if not move:
            return False
        # 必须有棋子
        piece = self.piece_type_at(move.from_square)
        if not piece:
            return False

        from_mask = BB_SQUARES[move.from_square]
        to_mask = BB_SQUARES[move.to_square]

        # 是否是自己的棋子
        if not self.occupied_co[self.turn] & from_mask:
            return False

        # 目标格子不能有自己的棋子
        if self.occupied_co[self.turn] & to_mask:
            return False

        return bool(self.attacks_mask(move.from_square) & to_mask)

    def is_legal(self, move: Move) -> bool:
        return self.is_pseudo_legal(move) and not self.is_into_check(move)

    def is_into_check(self, move: Move) -> bool:
        king = self.king(self.turn)
        if king is None:
            return False

        checkers = self.attackers_mask(not self.turn, king)
        if checkers and move not in self._generate_evasions(king, checkers, BB_SQUARES[move.from_square], BB_SQUARES[move.to_square]):
            return True

        return not self._is_safe(king, self._slider_blockers(king), self._knight_blockers(king), move)

    def _slider_blockers(self, king: Square) -> List[Tuple[Bitboard, Bitboard, int]]:
        rays = _rook_attacks(king, BB_EMPTY)
        cannons = rays & self.cannons & self.occupied_co[not self.turn]
        rooks_and_kings = rays & (self.kings | self.rooks) & self.occupied_co[not self.turn]

        blockers = []

        for sniper in scan_reversed(cannons):
            mask = between(king, sniper)
            b = mask & self.occupied
            # 如果路线上只有两个棋子
            if count_ones(b) == 2:
                blockers.append((mask, BB_SQUARES[sniper], 1))
            # 空头炮
            elif count_ones(b) == 0:
                blockers.append((mask, BB_SQUARES[sniper], 1))

        for sniper in scan_reversed(rooks_and_kings):
            mask = between(king, sniper)
            b = mask & self.occupied
            # 如果路线上只有一个棋子则是一个 blocker
            if b and count_ones(b) == 1:
                blockers.append((mask, BB_SQUARES[sniper], 0))

        return blockers

    def _knight_blockers(self, king: Square) -> List[Tuple(Bitboard, Bitboard)]:
        # 生成正在别马脚的棋子
        knights = self.knights & self.occupied_co[not self.turn]
        blockers = BB_EMPTY
        blockers_detail = []
        occupied = BB_KNIGHT_REVERSED_MASKS[king] & self.occupied_co[self.turn]
        masks = [BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king + 15],
                 BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king + 17],
                 BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king - 15],
                 BB_KNIGHT_REVERSED_MASKS[king] & ~BB_SQUARES[king - 17],
                 ]
        for mask in masks:
            attack_knights = BB_KNIGHT_REVERSED_ATTACKS[king][mask] & knights
            if attack_knights and (occupied & ~mask):
                blockers |= (occupied & ~mask)
                if count_ones(attack_knights) == 1:
                    blockers_detail.append((occupied & ~mask, attack_knights))
                else:
                    blockers_detail.append((occupied & ~mask, BB_EMPTY))

        return blockers_detail

    def _generate_evasions(self, king: Square, checkers: Bitboard,
                           from_mask: Bitboard = BB_IN_BOARD, to_mask: Bitboard = BB_IN_BOARD) -> Iterator[Move]:

        attacked = BB_EMPTY
        for checker in scan_reversed(checkers & self.rooks):
            attacked |= line(king, checker) & ~BB_SQUARES[checker]

        for checker in scan_reversed(checkers & self.cannons):
            middle = between(king, checker) & self.occupied
            l = between(middle, checker) | middle | checker
            attacked |= line(king, checker) & ~l & ~BB_SQUARES[checker]

        if BB_SQUARES[king] & from_mask:
            for to_square in scan_reversed(BB_KING_ATTACKS[king] & ~self.occupied_co[self.turn] & ~attacked & to_mask):
                yield Move(king, to_square)

        if count_ones(checkers) == 1:
            # 只有一个子将
            checker = msb(checkers)
            if checkers & (self.rooks | self.kings):
                target = between(king, checker) | checkers
                yield from self.generate_pseudo_legal_moves(~self.kings & from_mask, target & to_mask)
            elif checkers & self.cannons:
                target = between(king, checker) & ~self.occupied | checkers
                yield from self.generate_pseudo_legal_moves(~self.kings & from_mask & ~target, target & to_mask)
                # 拆炮架
                yield from self.generate_pseudo_legal_moves(~self.kings & from_mask & target, ~target & to_mask)
            elif checkers & self.knights:
                # 别马腿
                yield from self.generate_pseudo_legal_moves(~self.kings & from_mask, _knight_blocker(king, checker) & to_mask)

        elif count_ones(checkers) == 2:
            # 车炮双将
            cannon_checker = msb(checkers & self.cannons)
            rook_checker = msb(checkers & self.rooks)
            if line(cannon_checker, rook_checker) & BB_SQUARES[king] and not (between(cannon_checker, rook_checker) & BB_SQUARES[king]):
                yield from self.generate_pseudo_legal_moves(~self.kings & from_mask, between(king, rook_checker) & to_mask)

    def generate_pseudo_legal_moves(self, from_mask: Bitboard = BB_IN_BOARD, to_mask: Bitboard = BB_IN_BOARD) -> Iterator[Move]:
        our_pieces = self.occupied_co[self.turn]

        from_squares = our_pieces & from_mask
        for from_square in scan_reversed(from_squares):
            moves = self.attacks_mask(from_square) & ~our_pieces & to_mask
            for to_square in scan_reversed(moves):
                yield Move(from_square, to_square)

    def generate_legal_moves(self, from_mask: Bitboard = BB_IN_BOARD, to_mask: Bitboard = BB_IN_BOARD) -> Iterator[Move]:
        king_mask = self.kings & self.occupied_co[self.turn]
        if king_mask:
            king = msb(king_mask)
            slider_blockers = self._slider_blockers(king)
            knight_blockers = self._knight_blockers(king)
            checkers = self.attackers_mask(not self.turn, king)
            if checkers:
                for move in self._generate_evasions(king, checkers, from_mask, to_mask):
                    if self._is_safe(king, slider_blockers, knight_blockers, move):
                        yield move
            else:
                for move in self.generate_pseudo_legal_moves(from_mask, to_mask):
                    if self._is_safe(king, slider_blockers, knight_blockers, move):
                        yield move
        else:
            yield from self.generate_pseudo_legal_moves(from_mask, to_mask)

    def _board_state(self: Board) -> _BoardState[Board]:
        return _BoardState(self)

    def push(self, move: Move) -> None:
        board_state = self._board_state()

        self.move_stack.append(move)
        self._stack.append(board_state)

        if self.turn == BLACK:
            self.fullmove_number += 1

        if not move:
            self.turn = not self.turn
            return

        piece_type = self._remove_piece_at(move.from_square)
        assert piece_type is not None, f"push() expects move to be pseudo-legal, but got {move} in {self.board_fen()}"

        self._set_piece_at(move.to_square, piece_type, self.turn)
        self.turn = not self.turn

    def fen(self) -> str:
        return " ".join([
            self.board_fen(),
            "w" if self.turn == RED else "b",
            "-",
            "-",
            str(0),
            str(self.fullmove_number)
        ])

    def pop(self) -> Move:
        if not len(self.move_stack):
            return None
        move = self.move_stack.pop()
        self._stack.pop().restore(self)
        return move

    def peek(self) -> Move:
        if len(self.move_stack):
            return self.move_stack[-1]
        else:
            return None

    def push_iccs(self, iccs: str):
        # TODO:检查合法
        move = Move.from_iccs(iccs)
        if move in self.generate_legal_moves():
            self.push(move)

    def chinese_move(self, move: Move, full_width=False) -> str:
        build = []
        wxf_move = self.wxf(move)
        piece_type = wxf_move[0]
        if self.turn == RED:
            piece_type = piece_type.upper()
        build.append(PIECES_NAMES[piece_type])

        if wxf_move[1] in "+-abced":
            pos = POSITION_NAMES[wxf_move[1]]
            build.insert(0, pos)
        else:
            if self.turn == RED:
                build.append(CHINESE_NUMBERS[int(wxf_move[1])])
            else:
                build.append(wxf_move[1])

        build.append(ACTION_NAMES[wxf_move[2]])

        if self.turn == RED:
            build.append(CHINESE_NUMBERS[int(wxf_move[3])])
        else:
            build.append(wxf_move[3])

        if full_width:
            chars = "１２３４５６７８９"
            for i, c in enumerate(build):
                if c in "123456789":
                    build[i] = chars[int(c) - 1]

        return "".join(build)

    def wxf(self, move: Move) -> str:
        from_square = move.from_square
        to_square = move.to_square
        from_square_file = square_file(from_square)
        from_file_wxf = square_file_wxf(from_square, self.turn)
        to_file_wxf = square_file_wxf(to_square, self.turn)
        piece = self.piece_type_at(from_square)
        result = ""
        plus_symbol = "+" if self.turn == RED else "-"
        minus_symbol = "-" if self.turn == RED else "+"
        chars = ["a", "b", "c", "d", "e"]

        # 相象仕士
        if piece == ADVISOR or piece == BISHOP:
            result += PIECE_SYMBOLS[piece] + str(from_file_wxf)

        # 兵卒
        elif (piece == PAWN):
            other = self.pieces_mask(piece, self.turn) & BB_FILES[from_square_file] & ~BB_SQUARES[from_square]
            if not other:
                result += PIECE_SYMBOLS[piece] + str(from_file_wxf)
            else:
                pawns = []
                for bb_file in BB_FILES[::-1]:
                    file_pawns = []
                    for p in scan_reversed(bb_file & self.pawns & self.occupied_co[self.turn]):
                        file_pawns.append(p)
                    if len(file_pawns) > 1:
                        pawns += file_pawns
                if len(pawns) == 2:
                    result = PIECE_SYMBOLS[piece] + [plus_symbol, minus_symbol][pawns.index(from_square)]
                elif len(pawns) == 3:
                    result = PIECE_SYMBOLS[piece] + [plus_symbol, ".", minus_symbol][pawns.index(from_square)]
                else:
                    if self.turn == RED:
                        result = PIECE_SYMBOLS[piece] + chars[pawns.index(from_square)]
                    else:
                        result = PIECE_SYMBOLS[piece] + chars[pawns[::-1].index(from_square)]

        # 车马帅将炮
        else:
            other = self.pieces_mask(piece, self.turn) & BB_FILES[from_square_file] & ~BB_SQUARES[from_square]
            if other:
                result += PIECE_SYMBOLS[piece] + (plus_symbol if msb(other) < from_square else minus_symbol)
            else:
                result += PIECE_SYMBOLS[piece] + str(from_file_wxf)

        # 马相象仕士
        if piece == KNIGHT or piece == BISHOP or piece == ADVISOR:
            result += (plus_symbol if from_square < to_square else minus_symbol) + str(to_file_wxf)

        # 车帅将炮兵卒
        else:
            offset = count_ones(between(from_square, to_square)) + 1
            if abs(from_square - to_square) > 15:
                result += (minus_symbol if from_square > to_square else plus_symbol) + str(offset)
            else:
                result += "." + str(to_file_wxf)

        return result


class PseudoLegalMoveGenerator:

    def __init__(self, board: Board) -> None:
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_pseudo_legal_moves())

    def count(self) -> int:
        return len(list(self))

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_pseudo_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_pseudo_legal(move)

    def __repr__(self) -> str:
        builder = []

        for move in self:
            if self.board.is_legal(move):
                builder.append(self.board.wxf(move))
            else:
                builder.append(move.iccs())

        sans = ", ".join(builder)
        return f"<PseudoLegalMoveGenerator at {id(self):#x} ({sans})>"


class LegalMoveGenerator:

    def __init__(self, board: Board) -> None:
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_legal_moves())

    def count(self) -> int:
        return len(list(self))

    def chinese(self) -> str:
        s = ", ".join(self.board.chinese_move(move) for move in self)
        return s

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_legal(move)

    def __repr__(self) -> str:
        sans = ", ".join(self.board.wxf(move) for move in self)
        return f"<LegalMoveGenerator at {id(self):#x} ({sans})>"
