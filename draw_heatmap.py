import json
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
import chess

BOARD_SIZE = 8
SQUARES = [chess.square_name(sq) for sq in chess.SQUARES]

def load_blunder_data(json_file="blunder_heatmap_data.json", heatmap_type="from"):
    with open(json_file, "r") as f:
        data = json.load(f)
    
    if heatmap_type == "from":
        return data.get("from_squares", "{}")
    elif heatmap_type == "to":
        return data.get("to_squares", "{}")
    elif heatmap_type == "both":
        from_blunders = data.get("from_squares", {})
        to_blunders = data.get("to_squares", {})
        combined = {}

        # Sum counts for squares appearing in either dict
        all_squares = set(from_blunders) | set(to_blunders)
        for sq in all_squares:
            combined[sq] = from_blunders.get(sq, 0) + to_blunders.get(sq, 0)
        return combined
    else:
        return ValueError("Heatmap must be 'from' or 'to'")

def create_heatmap_matrix(blunder_data):
    matrix = np.zeros((BOARD_SIZE, BOARD_SIZE))

    for square, count in blunder_data.items():
        file = chess.FILE_NAMES.index(square[0])
        rank = int(square[1]) - 1
        matrix[rank][file] = count  # Flip vertically to match board layout

    return matrix

def draw_chessboard_heatmap(heatmap_matrix, title="Blunder Heatmap"):
    fig, ax = plt.subplots(figsize=(8, 8))
    cmap = plt.cm.Reds

    cax = ax.imshow(heatmap_matrix, cmap=cmap, interpolation="nearest")

    # Draw squares with text
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            ax.text(j, i, f"{int(heatmap_matrix[i][j])}", ha="center", va="center", color="black", fontsize=9)

    # Set ticks for files (columns)
    ax.set_xticks(np.arange(BOARD_SIZE))
    ax.set_xticklabels("abcdefgh")

    # Set ticks for ranks (rows) but remove the bottom label
    y_labels = list(range(1, 9))
    ax.set_yticks(np.arange(BOARD_SIZE))
    ax.set_yticklabels(y_labels)

    # Set titles for heatmap
    ax.set_title(title)
    ax.set_xlabel("File")
    ax.set_ylabel("Rank")

    plt.gca().invert_yaxis()

    # Move colorbar to bottom
    cbar = fig.colorbar(cax, ax=ax, orientation='horizontal', fraction=0.05, pad=0.07)
    cbar.set_label("Blunder Frequency")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = load_blunder_data("blunder_heatmap_data.json", heatmap_type="both")
    matrix = create_heatmap_matrix(data)
    draw_chessboard_heatmap(matrix)
