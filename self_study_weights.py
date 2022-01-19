import random
import re
from time import perf_counter

import chess
import chess.engine

def calculate_depth(wtime, btime, dobavka, mode):
    if mode == 'classic':
        return ((wtime + btime) + dobavka) // 5

    elif mode == 'bullet':
        return ((wtime + btime) + dobavka) // 11


def configure_weights(engine, board):
    weights = open('./weights.txt', 'a')
    weights_f = open('./weights_fen.txt', 'a')

    weights_f.write(str(board.fen()) + '\n')

    while not board.is_game_over():
        info = engine.analyse(board, chess.engine.Limit(depth=10))
        result = engine.play(board, chess.engine.Limit(depth=10))


        score_real1 = re.sub('\D', '', str(info['score']))
        if int(score_real1) >= 100 and not board.turn:
            weights.write(str(result.move) + '\n')
            result_ = engine.play(board, chess.engine.Limit(depth=20))

            board.push(result_.move)
            weights_f.write(str(board.fen()) + '\n')


            print(board.unicode())
            print('\n'*2)

        else:

            info = engine.analyse(board, chess.engine.Limit(depth=10))
            result = engine.play(board, chess.engine.Limit(depth=10))

            board.push(result.move)
            weights_f.write(str(board.fen()) + '\n')


            print(board.unicode())
            print('\n'*3)

        if int(score_real1) <= -50 and board.turn:
            weights.write(str(result.move) + '\n')

            result_ = engine.play(board, chess.engine.Limit(depth=20))

            board.push(result_.move)
            weights_f.write(str(board.fen()) + '\n')

            print(board.unicode())
            print('\n'*2)

        else:

            info = engine.analyse(board, chess.engine.Limit(depth=10))
            result = engine.play(board, chess.engine.Limit(depth=10))

            board.push(result.move)
            weights_f.write(str(board.fen()) + '\n')

            print(board.unicode())
            print('\n'*3)

            print('Weight configed!')


def self_study_with_weights(engine, board,
                            rating,
                            results_f):
    bb = 1
    rating = 1000
    depth = 10

    # parse weights
    weights_ = open('./weights.txt', 'r')
    weights_ = weights_.readlines()
    weights_f_ = open('./weights_fen.txt', 'r')
    weights_f_ = weights_f_.readlines()
    weights_f_ = [line.rstrip('\n') for line in weights_f_]


    for weight in weights_:
        new_weight = weight.replace('\n', '')
        weights_.remove(weight) # removing old weight
        weights_.append(new_weight)

    # self-move
    if True:
        info = engine.analyse(board, chess.engine.Limit(depth=15))
        result = engine.play(board, chess.engine.Limit(depth=15))


        if result.move in weights_ and \
                weights_f_[bb-1] == \
                str(board.fen()):
            print('STOP')

            if True:
                result_ = engine.play(board, chess.engine.Limit(depth=10))
                if result_.move in weights_:
                    if depth >= 100:
                        score_real1 = re.sub('\D', '', str(info['score']))
                        board.push(result_.move)
                        print(board.unicode())
                        if board.turn:
                            print(score_real1 + ' | WHITE MOVE')
                        else:
                            print(score_real1 + ' | BLACK MOVE')
                        #break

                    depth += 5
                    print(f'DEPTH NOW IS {depth}')
                    result_ = engine.play(board, chess.engine.Limit(depth=depth))
                    score_real1 = re.sub('\D', '', str(info['score']))
                    bb += 1
                    if bb == 106:
                        is_game_over = True
                    print(board.unicode())
                    if board.turn:
                        print(score_real1 + ' | WHITE MOVE')
                    else:
                        print(score_real1 + ' | BLACK MOVE')

                else:
                    board.push(result_.move)
                    bb += 1
                    print(board.unicode())

                    score_real1 = re.sub('\D', '', str(info['score']))

                    if board.turn:
                        print(score_real1 + ' | WHITE MOVE')
                    else:
                        print(score_real1 + ' | BLACK MOVE')
                    #break

        else:
            info = engine.analyse(board, chess.engine.Limit(depth=10))
            result = engine.play(board, chess.engine.Limit(depth=10))

            board.push(result.move)
            bb += 1
            print(board.unicode())
            if board.turn:
                score_real1 = re.sub('\D', '', str(info['score']))
                print(score_real1 + ' | WHITE MOVE')
            else:
                score_real1 = re.sub('\D', '', str(info['score']))
                print(score_real1 + ' | BLACK MOVE')

        if str(board.result()) == '1-0' or str(board.result()) == '0-1':
            rating += random.randrange(70, 120)
            results_f.write(str(board.result()) + '\n')

        elif str(board.result()) == '1/2-1/2' or bb == 106:
            rating += random.randrange(10, 50)
            results_f.write(str(board.result()) + '\n')

        return rating-1000

def bestmove(engine, board, wtime, btime, dobavka, multipv, move):
    # calculating depth
    depth = calculate_depth(wtime=wtime, btime=btime, dobavka=dobavka, mode='bullet')
    print(depth)

    start_time = perf_counter()

    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    result = engine.play(board, chess.engine.Limit(depth=depth))

    info['multipv'] = multipv

    d = 0

    weights_ = open('./weights.txt', 'r')
    weights_ = weights_.readlines()

    for weight in weights_:
        new_weight = weight.replace('\n', '')
        weights_.remove(weight)  # removing old weight
        weights_.append(new_weight)

    if result.move in weights_:
        d += 5
        info = engine.analyse(board, chess.engine.Limit(depth=depth + d))
        result = engine.play(board, chess.engine.Limit(depth=depth + d))

        end = perf_counter()

        if move == 'W':
            wtime -= (end - start_time)

            return [result.move, wtime]

        elif move == 'B':
            btime -= (end - start_time)

            return [result.move, btime]

    else:

        end = perf_counter()

        if move == 'W':
            wtime -= (end - start_time)

            return [result.move, wtime]

        elif move == 'B':
            btime -= (end - start_time)

            return [result.move, btime]

