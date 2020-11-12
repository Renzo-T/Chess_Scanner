from stockfish import Stockfish
import os

cw_dir = os.path.dirname(__file__)
sf_path = "stockfish_20090216_x64_bmi2"
abs_path = os.path.join(cw_dir,sf_path)

stockfish = Stockfish(abs_path);
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(stockfish.get_board_visual())
print(stockfish.get_best_move())