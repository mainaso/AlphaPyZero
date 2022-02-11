import logging

import chess

logger = logging.getLogger("MarcoEngineUtils")

def print_l(msg):
    print(msg)
    logger.info(msg)


def new_board(old_board, fen: str = None):
    del old_board

    if not fen is None:
        n_board = chess.Board(fen)

        return n_board

    else:
        n_board = chess.Board()

        return n_board


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

