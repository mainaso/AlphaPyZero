import logging
import random

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

def calculate_time(wtime, btime, depth):
    if wtime <= 1000 and btime >= 1000:
        return "0.{}".format(int(depth // 4))
        
    elif wtime <= 1000 and btime <= 1000:
        return "0.".format(int(depth // random.randint(3, 5)))
    
    else:
        return "0.".format(int(depth // random.randint(5, 9)))
