import chess.pgn
import chess.engine
import json
from collections import Counter

STOCKFISH_PATH = "C:/Tools/stockfish-windows-x86-64-avx2.exe"
BLUNDER_THRESHOLD = 1.5  # Eval drop in pawns considered a blunder

def analyze_blunders_with_stockfish(pgn_file="games.pgn", max_depth=15):
    blunder_squares = Counter()

    with open(pgn_file) as f:
        print('opened pgn')
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break

            board = game.board()
            evaluations = []

            with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
                node = game
                while node.variations:
                    next_node = node.variation(0)
                    move = next_node.move

                    # Evaluate current position
                    info = engine.analyse(board, chess.engine.Limit(depth=max_depth))
                    score = info["score"].white().score(mate_score=10000)
                    evaluations.append(score if score is not None else 0)

                    board.push(move)
                    node = next_node

                # Compare evals to find blunders
                for i in range(1, len(evaluations)):
                    delta = evaluations[i] - evaluations[i - 1]
                    if delta < -BLUNDER_THRESHOLD * 100:  # Stockfish scores in centipawns
                        move = list(game.mainline_moves())[i - 1]
                        blunder_squares[move.from_square] += 1
                        blunder_squares[move.to_square] += 1

    # Convert square indices to algebraic notation
    result = {chess.square_name(sq): count for sq, count in blunder_squares.items()}

    with open("blunder_heatmap_data.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Analysis complete. Saved to blunder_heatmap_data.json.")

if __name__ == "__main__":
    analyze_blunders_with_stockfish()
