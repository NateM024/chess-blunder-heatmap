import chess.pgn
import chess.engine
import json
from collections import defaultdict, Counter

STOCKFISH_PATH = "C:/Tools/stockfish-windows-x86-64-avx2.exe" # <-- Change as needed
USERNAME = "NateChess24" # <-- Change as needed
BLUNDER_THRESHOLD = 2  # Eval drop in pawns considered a blunder

def analyze_blunders_with_stockfish(pgn_file="games.pgn", max_depth=15):
    from_square_blunders = defaultdict(Counter)
    to_square_blunders = defaultdict(Counter)

    with open(pgn_file) as f:
        count_games = 1
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
        
            # Figure out what color the user played as
            player_color = chess.WHITE
            if game.headers.get("Black", "") == USERNAME:
                player_color = chess.BLACK

            # Load the game
            board = game.board()
            evaluations = []

            with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
                node = game

                # Go through each move
                while node.variations:
                    next_node = node.variation(0)
                    move = next_node.move

                    # Only evaluate player's moves
                    if board.turn == player_color:
                        info = engine.analyse(board, chess.engine.Limit(depth=max_depth))
                        score = info["score"].white().score(mate_score=10000)
                        evaluations.append(score if score is not None else 0)

                    board.push(move)
                    node = next_node

                color = "white"
                if player_color == False:
                    color = "black"

                # Compare evals to find blunders
                for i in range(1, len(evaluations)):
                    delta = evaluations[i] - evaluations[i - 1]  
                    if color == "black" and delta > BLUNDER_THRESHOLD * 100 or color == "white" and delta < -BLUNDER_THRESHOLD * 100: # Determines if a blunder occured
                        move = list(game.mainline_moves())[i - 1]
                        #print(f"Blunder in game {count_games}, player color: {player_color}")
                        from_square_blunders[move.from_square][color] += 1
                        to_square_blunders[move.to_square][color] += 1

                print(f"Game {count_games} analyzed")
                count_games += 1

    # Convert to algebraic notation
    
    from_result = {chess.square_name(sq): dict(colors) for sq, colors in from_square_blunders.items()}
    to_result = {chess.square_name(sq): dict(colors) for sq, colors in to_square_blunders.items()}

    heatmap_data = {
        "from_squares": from_result,
        "to_squares": to_result
    }

    # Save to json file
    with open("blunder_heatmap_data.json", "w") as out_file:
        json.dump(heatmap_data, out_file, indent=2)

    print("Analysis complete. Saved to blunder_heatmap_data.json.")

if __name__ == "__main__":
    analyze_blunders_with_stockfish()

# {
#   "from squares": {
#       "a1": {
#           "white" : 1
#           "black" : 1 
#           ?"both" : 2
#       }
#       "a2"{
#       
#       }
#       "a3"
#       "a4"
#   }
#
#
#
#
#
#
#
#}
