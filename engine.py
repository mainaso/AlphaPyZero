import json

import chess.engine

from train import analyze, best_move
from utils import *

logger = logging.getLogger("MarcoEngineTraining")  
board = chess.Board()

# engine
class Engine:
	def __init__(self, engine_path, weights_filename):
		self.engine = chess.engine.SimpleEngine.popen_uci(str(engine_path))
		self.weights = json.load(open(weights_filename, 'r'))

	def go(self, depth: int = None):
		if depth is None:
			for deep in range(0, 101):
				info = analyze(self.engine, board, deep)
				result = best_move(self.engine, board, deep)

				if str(board.fen()) in list(self.weights.values()):
					result = get_key(self.weights, str(result))

					print(f'Uses weight from fen: {board.fen()}')
					print(str(info) + f' {deep} depth')
					print(str(result))
					print('\n'*3)

				else:
					print(str(board.fen()) + ' not in weights! Analyzing without weights...')
					print(str(info) + f' {deep} depth')
					print(str(result))
					print('\n'*3)

				return result.move


		elif not depth is None:
			print(str(list(self.weights.values())) + ' weights loaded!')

			for deep in range(0, depth + 1):
				info = analyze(self.engine, board, deep)
				result = best_move(self.engine, board, deep)

				if str(board.fen()) in list(self.weights.values()):
					result = get_key(self.weights, str(result))

					print(f'Uses weight from fen: {board.fen()}')
					print(str(info) + f' {deep} depth')
					print(str(result))
					print('\n'*3)

				else:
					print(str(board.fen()) + ' not in weights! Analyzing without weights...')
					print(str(info) + f' {deep} depth')
					print(str(result))
					print('\n'*3)

				return result.move


			self.engine.quit()
			return

if __name__ == '__main__':
	engin = Engine("stockfish", "./weights/weights_norm.json")
	engin.go(depth=20)
