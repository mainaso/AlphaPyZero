import chess
import chess.engine
from colorama import init, Fore

from rich.console import Console
from rich.table import Table

import logging
import json
import re
import random
import time
import datetime

from engine import *
from utils import *

init(autoreset=True)



logger = logging.getLogger("MarcoEngineTraining")
board = chess.Board()

uci_conf = json.load(open('./settings/uci_config.json', 'r'))
train_conf = json.load(open('./settings/train_conf.json', 'r'))
conf = json.load(open("./settings/conf.json", "r"))
results_dictionary = json.load(open("./games/results.json", "r"))
games_count = train_conf['Games count']
games_count_for_train = conf["Games Train Count"]

# engine utils
def analyze(engine, board, depth: int = None, limit: int = None):
    if depth is None and limit is None:
        # print_l('You want input depth or limit!')

        return

    elif depth is not None and limit is None:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))

        info['Hash'] = uci_conf['Hash']
        info['MultiPV'] = uci_conf['MultiPV']

        # print_l(str(info['score']))

        return info['score']

    elif depth is None and limit is not None:
        info = engine.analyse(board, chess.engine.Limit(time=limit))

        info['Hash'] = uci_conf['Hash']
        info['MultiPV'] = uci_conf['MultiPV']

        # print_l(str(info['score']))

        return info['score']


def analyze_without_score(engine, board, depth: int = None, limit: int = None):
    if depth is None and limit is None:
        print_l('You want input depth or limit!')

        return

    elif depth is not None and limit is None:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))

        info['Hash'] = uci_conf['Hash']
        info['MultiPV'] = uci_conf['MultiPV']

        # print_l(str(info['score']))

        return info['score']

    elif depth is None and limit is not None:
        info = engine.analyse(board, chess.engine.Limit(time=limit))

        info['Hash'] = uci_conf['Hash']
        info['MultiPV'] = uci_conf['MultiPV']

        # print_l(str(info['score']))

        return info


def best_move(engine, board, depth: int = None, limit: int = None):
    weights_json = json.load(open("./weights/weights_norm.json", 'r'))

    if depth is None and limit is None:
        print_l('You want input depth or limit!')

        return

    elif depth is not None and limit is None:
        result = engine.play(board, chess.engine.Limit(depth=depth))

        if not str(board.fen()) in weights_json.values():

            return result.move

        else:

            return result.move

    elif depth is None and limit is not None:
        result = engine.play(board, chess.engine.Limit(time=limit))

        if not str(board.fen()) in weights_json.values():

            return result.move

        else:
            engin = Engine("stockfish", "./weights/weights_norm.json")
            move = engin.go(calculate_time(depth=20))

            return move

        return result.move


# engine
def create_new_move(filename):
    if filename.endswith('.json'):
        dict_errors = json.load(open(filename, 'r'))
        dict_norm = json.load(open(filename, 'r'))


    else:

        dict_errors = json.load(open(filename + '.json', 'r'))
        dict_norm = json.load(open(filename + '.json', 'r'))

    start_time = time.perf_counter()

    error_keys = dict_errors.keys()

    fens = []
    dict_moves = []
    dict_keys = []

    for key in error_keys:
        board = chess.Board(dict_errors[key])
        score = analyze(engine=engine, board=board, depth=20)
        real_score = re.sub('\D', '', str(score))

        if '-' in str(score) and int(str('-') + str(real_score)) <= -40:
            # generating new move
            move = best_move(engine=engine, board=board, depth=20)

            fens.append(str(board.fen()))
            dict_moves.append(str(move))
            dict_keys.append(str(key))

        if '+' in str(score) and int(real_score) >= 40:
            # generating new move
            move = best_move(engine=engine, board=board, depth=20)

            board.push(move)

            fens.append(str(board.fen()))
            dict_moves.append(str(move))
            dict_keys.append(str(key))

    for _move in dict_moves:
        dict_norm[str(move)] = fens[dict_moves.index(_move)]

    with open('./weights/weights_norm.json', 'w') as weights_file:
        json.dump(dict_norm, weights_file)

    end_time = time.perf_counter()

    return end_time - start_time


def train(engine, board):
    dictionary = {}  # or dict()
    board = new_board(old_board=board)

    start_time = time.perf_counter()

    while not board.is_game_over():
        move = best_move(engine=engine, board=board, depth=random.randrange(10, 15))
        try:
            board.push(move)

            dictionary[str(move)] = board.fen()

        except:
            end_time = time.perf_counter()
            return board, dictionary, end_time - start_time

    end_time = time.perf_counter()

    train_conf['Games count'] = train_conf['Games count'] + 1
    json.dump(train_conf, open('./settings/train_conf.json', 'w'))

    return board, dictionary, end_time - start_time

def results_print(results_dict):
    draws = 0
    wins_w = 0
    wins_b = 0

    for result in list(results_dict.keys()):
        if "1/2-1/2" in result:
            draws += 1

        elif  "1-0" in result:
            wins_w += 1

        elif "0-1" in result:
            wins_b += 1

    print('\n'*2)

    table = Table(title="Train results")

    table.add_column("Played games", justify="right", style="cyan", no_wrap=True)
    table.add_column("Wins white", style="magenta")
    table.add_column("Loses white", style="magenta")
    table.add_column("Draws", style="magenta")

    table.add_row(str(len(results_dict.keys())), str(wins_w), str(wins_b), str(draws))



    console = Console()
    console.print(table)

def start(engine):
    now = datetime.datetime.now()
    path = "./games/game" + str(random.randint(0, 1000000)) + '.json'
    b, _dictionary, elapsed = train(engine=engine, board=board)

    if not str(b.result()) == '*':
        print_l(
            f'{Fore.GREEN} [+ {now.strftime("%d-%m-%Y %H:%M")}] Game completed, result: {b.result()}. Time elapsed: {elapsed}')

    with open(path, "w") as write_file:
        json.dump(_dictionary, write_file)

    elapsed_new_move = create_new_move(filename=path)

    now = datetime.datetime.now()

    print_l(f'{Fore.GREEN} [+ {now.strftime("%d-%m-%Y %H:%M")}] Weights created. Time elapsed: {elapsed_new_move}')

    return b.result()


if __name__ == '__main__':
    count_g = 0

    while not count_g >= games_count_for_train:
        count_g += 1
        engine = chess.engine.SimpleEngine.popen_uci('stockfish')
        resul = start(engine=engine)
        engine.quit()

        results_dictionary[str(count_g) + " " + str(resul)] = " "

        with open('./games/results.json', "w") as results_diictionary:
            json.dump(results_dictionary, results_diictionary)

    results_print(results_dict=results_dictionary)


