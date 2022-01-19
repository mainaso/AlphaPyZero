#import marcoengine_selfstudy2 as me
from chess.engine import SimpleEngine

import self_study_weights as ssw
import chess
from chess import Move
import chess.engine
from colorama import Fore, Style

import time # for sleeping & timers
import sys
import re

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(r'stockfish')
g = 0
wtime = 100
btime = 100
dobavka = 0
pv = 1

uci_s = {'name': 'MarcoEngine 4.2', 'author': 'Mark Kim', 'hash': 256, 'MultiPV': 1} # uci protocol

# max rating is 4132

print(f'''{Fore.LIGHTYELLOW_EX}
                   ______            
        |\    /|   |       |\   |    ______   ---|---  |\  |  |----
{Fore.LIGHTGREEN_EX}        | \  / |   |---    | \  |    |           |     | \ |  |--
{Fore.LIGHTYELLOW_EX}        |  \/  |   |_____  |  \_|    |   __   ---|---  |  \|  |----
{Fore.LIGHTGREEN_EX}                                     |____|      

{Style.RESET_ALL}MarcoEngine 4.2 by Mark Kim.

{Fore.LIGHTRED_EX}Neural network chess engine based on Stockfish 14 by T. Romstad, M. Costalba, J. Kiiski, G. Linscott.
{Style.RESET_ALL}
''')

if sys.argv == ['main.py']:

    while True:
        userCommand = input()

        if userCommand == 'train':
            print('Starting training..', flush=True)
            # start training

            # create weights
            if not g >= 2:
                ssw.configure_weights(engine=engine, board=board)

            del board
            board = chess.Board()  # new board

            # self playing
            while not board.is_game_over():
                ssw.self_study_with_weights(engine=engine, board=board,
                                                          rating=1000,
                                                          results_f=open('./weights_results.txt', 'a'))

            g += 1

            # print results
            print('Done!', flush=True)
            print('Results:', flush=True)
            print('Result of game ' + str(board.result()), flush=True)
            print('Played games {}'.format(g), flush=True)
            print('\n' * 7)

            del board
            board = chess.Board()  # new board

        elif userCommand == 'go':
            # if engine trained
            if not g >= 3:
                print('First train engine!', flush=True)

            else:
                if board.turn:

                    rs = ssw.bestmove(engine=engine, board=board, wtime=wtime, btime=btime, dobavka=dobavka,
                                      multipv=pv, move='W')
                    print('bestmove ' + str(rs[0]), flush=True)

                    wtime = rs[1]
                    wtime += dobavka

                else:
                    rs = ssw.bestmove(engine=engine, board=board, wtime=wtime, btime=btime, dobavka=dobavka,
                                      multipv=pv, move='B')
                    print('bestmove ' + str(rs[0]), flush=True)



                    btime = rs[1]
                    btime += dobavka

        elif userCommand == 'setposition':
            del board
            fen_ = input()
            board = chess.Board(fen_)

        elif userCommand.startswith('setoption name'):
             uc = userCommand.split()

             if uc[2] == 'Hash':
                engine.hash = re.sub('\D', '', str(uc))
                uci_s['Hash'] = int(uc[4])

             elif uc[2] == 'MultiPV':
                uci_s['MultiPV'] = int(uc[4])

        elif userCommand.startswith('position fen'):
             uc = userCommand.split()

             del board
             board = chess.Board(uc[2])

        elif userCommand.startswith('position startpvpos'):
            userCommand.replace('position startpos moves')
            uc = userCommand.split()

            for move in uc:
                board.push(move)

        elif userCommand == 'ucinewgame':
            del board
            board = chess.Board()

        elif userCommand == "uci":
            print("id name MarcoEngine", flush=True)
            print("id author Mark Kim", flush=True)
            print(f'id Hash {uci_s["hash"]}', flush=True)
            print(f'id MultiPV {uci_s["MultiPV"]}', flush=True)
            time.sleep(1)
            print('uciok', flush=True)

        elif userCommand == 'wtime':
            print(wtime, flush=True)

        elif userCommand == 'btime':
            print(btime, flush=True)

        elif userCommand == 'winc':
            print(dobavka, flush=True)

        elif userCommand == 'binc':
            print(dobavka, flush=True)

        elif userCommand == 'isready':
            print('Yeah! Ready!', flush=True)

        elif userCommand == 'quit':
            print('Bye! ', flush=True)
            sys.exit()

        else:
            print('Unkown command', flush=True)

func = sys.argv[1]
try:
    other = sys.argv[2]
except:
    pass

sys_argv = sys.argv[1:]


if func == 'train':
    print('Starting training..', flush=True)
    # start training

    # create weights
    if not g >= 2:
        ssw.configure_weights(engine=engine, board=board)

    del board
    board = chess.Board()  # new board

    # self playing
    while not board.is_game_over():
        ssw.self_study_with_weights(engine=engine, board=board,
                                    rating=1000,
                                    results_f=open('./results_weights.txt', 'a'))

    g += 1

    # print results
    print('Done!', flush=True)
    print('Results:', flush=True)
    print('Result of game ' + str(board.result()), flush=True)
    print('Played games {}'.format(g), flush=True)
    print('\n' * 7)

    del board
    board = chess.Board()  # new board

elif func == 'go':
    # if engine trained
    if not g >= 3:
        print('First train engine!', flush=True)

    else:
        if board.turn:

            rs = ssw.bestmove(engine=engine, board=board, wtime=wtime, btime=btime, dobavka=dobavka, move='W')
            print('bestmove ' + str(rs[0]), flush=True)

            wtime = rs[1]
            wtime += dobavka

        else:
            rs = ssw.bestmove(engine=engine, board=board, wtime=wtime, btime=btime, dobavka=dobavka, move='B')
            print('bestmove ' + str(rs[0]), flush=True)

            btime = rs[1]
            btime += dobavka

elif func == 'setposition':
    del board
    board = chess.Board(other)

elif func.startswith('setoption name'):
    uc = func.split()

    if uc[2] == 'Hash':
        engine.hash = int(uc[4])

    elif uc[2] == 'MultiPV':
        pv = int(uc[4])

elif func.startswith('position fen'):
    uc = func.split()

    del board
    board = chess.Board(uc[2])


elif 'position' in sys_argv and 'startpos' in sys_argv and \
        'moves' in sys_argv:
    sys__argv = sys_argv
    uc = " ".join(str(x) for x in sys__argv)
    uc = uc.replace('position startpos moves', '')
    uc_ = uc.split()

    for move in uc_:
        board.push(Move.from_uci(move))

elif func == 'ucinewgame':
    del board
    board = chess.Board()

elif func == "uci":
    print("id name MarcoEngine", flush=True)
    print("id author Mark Kim", flush=True)
    print(f'id Hash {uci_s["hash"]}', flush=True)
    print(f'id MultiPV {uci_s["MultiPV"]}', flush=True)
    time.sleep(1)
    print('uciok', flush=True)

elif func == 'wtime':
    print(wtime, flush=True)

elif func == 'btime':
    print(btime, flush=True)

elif func == 'winc':
    print(dobavka, flush=True)

elif func == 'binc':
    print(dobavka, flush=True)

elif func == 'isready':
    print('Yeah! Ready!', flush=True)

elif func == 'quit':
    print('Bye! ')
    sys.exit()

else:
    print('Unkown command', flush=True)
    sys.exit()