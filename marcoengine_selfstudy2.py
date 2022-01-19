# weights self study
import chess
import chess.engine

from timeit import default_timer as timer
from datetime import timedelta
import random
import sys



def self_study(engine, board):
    is_game_over = False
    bb = 0
    rating = 1000

    while not is_game_over:
        info = engine.analyse(board, chess.engine.Limit(depth=10))
        result = engine.play(board, chess.engine.Limit(depth=10))
        print(result.move)

        if board.is_game_over():
            is_game_over = True

        info_score = list(str(info['score']))
        if info_score[12] == '+':
            normal_score = [int(info_score[13])]
            try:
                normal_score.append(int(info_score[14]))
                score_real = int(str(info_score[13]) + str(info_score[14]))
                if score_real <= -50:
                    result_ = engine.play(board, chess.engine.Limit(depth=15))
                    board.push(result_.move)
                    bb += 1
                    if bb == 106:
                        is_game_over = True
                    print(board.unicode() + '\t ' + str(result1.move) + '(new result)')
                    print(''.join(str(e) for e in normal_score) + ' | WHITE MOVE number {}'.format(bb // 2))
                    print('GAME {}'.format(b))

                else:

                    board.push(result.move)
                    bb += 1
                    if bb == 106:
                        is_game_over = True
                    print(board.unicode() + '\t ' + str(result.move))
                    print(''.join(str(e) for e in normal_score) + ' | WHITE MOVE number {}'.format(bb // 2))
                    print('GAME {}'.format(b))

                del normal_score, score_real
            except:
                del normal_score

        elif info_score[12] == '-':
            normal_score = [int(info_score[13])]
            try:
                normal_score.append(int(info_score[14]))
                score_real = int(str(info_score[13]) + str(info_score[14]))
                if score_real >= 100:
                    result1 = engine.play(board, chess.engine.Limit(depth=15))
                    board.push(result1.move)
                    bb += 1
                    if bb == 106:
                        is_game_over = True
                    print(board.unicode() + '\t ' + str(result1.move) + '(new result)')
                    print(''.join(str(e) for e in normal_score) + ' | BLACK MOVE number {}'.format(bb // 2))
                    print('GAME {}'.format(b))

                else:
                    board.push(result.move)
                    bb += 1
                    if bb == 106:
                        is_game_over = True
                    print(board.unicode() + '\t ' + str(result.move))
                    print(''.join(str(e) for e in normal_score) + ' | BLACK MOVE number {}'.format(bb // 2))
                    print('GAME {}'.format(b))

                del normal_score, score_real
            except:
                del normal_score

        del info, result


    if str(board.result()) == '1-0' or str(board.result()) == '0-1':
        rating += random.randrange(70, 120)

    elif str(board.result()) == '1/2-1/2' or bb == 106:
        rating += random.randrange(10, 50)

    del bb

    return rating - 1000

