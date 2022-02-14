import os
import json
import sys

from engine import Engine
import chess
from utils import *
from colorama import init, Fore
from chess import Move

init(autoreset=True)

weights = []

board = chess.Board()
engine = Engine("stockfish", "./weights/weights_norm.json")
uci_conf = json.load(open('./settings/uci_config.json', 'r'))
uci_conf2 = json.load(open('./settings/conf.json', 'r'))

def show_intro():
	intro = Fore.GREEN + f""" _______ _______               __              
|   |   |    ___|.-----.-----.|__|.-----.-----.
|       |    ___||     |  _  ||  ||     |  -__|
|__|_|__|_______||__|__|___  ||__||__|__|_____|
                       |_____|      
-----------------------------------------------
{Fore.MAGENTA} MarcoEngine by Mark Kim. {Fore.LIGHTRED_EX} Neural chess network.  
                       """



	print(intro)

def finding_weights():
	for f in os.listdir("./weights"):
		if f.endswith(".json"):
			weights.append(json.load(open(f'./weights/{f}', 'r')))

def uci_commander(command):

		if command.startswith('go'):
			if len(command.split()) == 1:
				engine.go()
				print_l('[+] Complete!')

			else:
				print_l('[-] Cannot parse command... ')

		elif command.startswith('uciok') or command == 'uci':
			for key in list(uci_conf2.keys()):
				print_l(f"id {str(key)}  {uci_conf2[key]}")

			for key in list(uci_conf.keys()):
				print_l(f"option name {str(key)} type WIP default {uci_conf[key]}")

			print('uciok', flush=True)

		elif command.startswith('ucinewgame'):
			new_board(old_board=board)

		elif command.startswith('position fen'):
			new_board(command.split()[2])

		elif command.startswith('position startpos'):
			command.replace('position startpos moves')
			c = command.split()

			for move in c:
				board.push(move)

		elif command.startswith('isready'):
			print_l('[+] Ready')

		elif command.startswith('quit'):
			sys.exit(1)

		else:
			print_l(f'[?] Unkown command: {command}')

def uci_sys_comander(sys_argv, command, other):

		if command.startswith('go'):
			if len(command.split()) == 1:
				engine.go()
				print_l('[+] Complete!')

			else:
				print_l('[-] Cannot parse command... ')

		elif command.startswith('uciok') or command == 'uci':
			for key in list(uci_conf2.keys()):
				print_l(f"id {str(key)}  {uci_conf2[key]}")

			for key in list(uci_conf.keys()):
				print_l(f"option name {str(key)} type WIP default {uci_conf[key]}")

			print('uciok', flush=True)

		elif command.startswith('ucinewgame'):
			new_board(old_board=board)

		elif command.startswith('position') and other == 'fen':
			new_board(sys_argv[2])

		elif 'position' in sys_argv and 'startpos' in sys_argv and \
        'moves' in sys_argv:
		    sys__argv = sys_argv
		    uc = " ".join(str(x) for x in sys__argv)
		    uc = uc.replace('position startpos moves', '')
		    uc_ = uc.split()

		    for move in uc_:
		        board.push(Move.from_uci(move))

		elif command.startswith('isready'):
			print_l('[+] Ready')

		elif command.startswith('quit'):
			sys.exit()

		else:
			print_l(f'[?] Unkown command: {command}')


if sys.argv == ['uci.py'] or sys.argv == ['./uci.bin'] or sys.argv == ['./marcoengine.bon']:
	show_intro()

	while True:
		com = input()
		uci_commander(com)

else:
	show_intro()

	sys_argv = sys.argv[1:]

	try:
		func = sys.argv[1]

	except:
		pass

	try:
		show_intro()

		other = sys.argv[2]
		uci_sys_comander(command=func, other=other, sys_argv=sys_argv)

	except:
		show_intro()

		uci_sys_comander(command=func, other=None, sys_argv=sys_argv)
