import json
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import chess

BOARD_SIZE = 8
SQUARES = [chess.square_name(sq) for sq in chess.SQUARES]

# for square filtering
SQUARE_STATES = ["to", "from"]
square_index = 0

# for color filtering
COLOR_STATES = ["both", "white", "black"]
color_index = 0

# Returns data from json  
def load_blunder_data(json_file="blunder_heatmap_data.json", square_state="to"):
    with open(json_file, "r") as f:
        data = json.load(f)
    
    # Load specific data from json file
    if square_state == "to":
        return data.get("to_squares", "{}")
    elif square_state == "from":
        return data.get("from_squares", "{}")
    else:
        return ValueError("Heatmap must be 'to' or 'from'")

# Returns an 8x8 array containing heatmap values 
def create_heatmap_matrix(blunder_data, color_state="both"):
    # Create matrix of 0's
    matrix = np.zeros((BOARD_SIZE, BOARD_SIZE))

    # Determine how the heatmap is filtered by color
    if color_state == "both":
        for position, colors in blunder_data.items():
            for color, count in colors.items():
                file = chess.FILE_NAMES.index(position[0])
                rank = int(position[1]) - 1
                matrix[rank][file] = count
    elif color_state == "white":
        for position, colors in data.items():
            if 'white' in colors:
                file = chess.FILE_NAMES.index(position[0])
                rank = int(position[1]) - 1
                matrix[rank][file] = colors['white']
    elif color_state == "black":
         for position, colors in data.items():
            if 'black' in colors:
                file = chess.FILE_NAMES.index(position[0])
                rank = int(position[1]) - 1
                matrix[rank][file] = colors['black']
    else:
        return ValueError("Color state must be 'both' 'white' or 'black")
    return matrix

# Shared references for update function
fig, ax, cax, cbar, heatmap_img, text_labels = None, None, None, None, None, []

# Updates the heatmap to display blunder frequency depending on the location of the blundered piece
def filter_blundered_squares(event):
    global square_index, heatmap_img, text_labels, ax, cbar

    square_index = (square_index + 1) % len(SQUARE_STATES)

    data = load_blunder_data("blunder_heatmap_data.json", square_state=SQUARE_STATES[square_index])
    new_matrix = create_heatmap_matrix(data, color_state=COLOR_STATES[color_index])

    # Update image data
    heatmap_img.set_data(new_matrix)

    # Update title
    ax.set_title(f"Blunder Heatmap ({COLOR_STATES[color_index].capitalize()}, {SQUARE_STATES[square_index].capitalize()})")

    # Remove old text labels from the plot
    for text in text_labels:
        text.remove()
    text_labels.clear()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            val = int(new_matrix[i][j])
            label = ax.text(j, i, str(val), ha='center', va='center', color='black', fontsize=9)
            text_labels.append(label)

    # Update color scale
    heatmap_img.set_clim(vmin=0, vmax=np.max(new_matrix))
    cbar.update_normal(heatmap_img)

    plt.draw()

# Updates heatmap to show blunder frequency off of the player's color
def filter_color(event):
    global square_index, color_index, text_labels, ax, cbar
    
    color_index = (color_index + 1) % len(COLOR_STATES)

    data = load_blunder_data("blunder_heatmap_data.json", square_state=SQUARE_STATES[square_index])
    new_matrix = create_heatmap_matrix(data, color_state=COLOR_STATES[color_index])

    # Update image data
    heatmap_img.set_data(new_matrix)

    # Update title
    ax.set_title(f"Blunder Heatmap ({COLOR_STATES[color_index].capitalize()}, {SQUARE_STATES[square_index].capitalize()})")

    # Remove old text labels from the plot
    for text in text_labels:
        text.remove()
    text_labels.clear()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            val = int(new_matrix[i][j])
            label = ax.text(j, i, str(val), ha='center', va='center', color='black', fontsize=9)
            text_labels.append(label)

    # Update color scale
    heatmap_img.set_clim(vmin=0, vmax=np.max(new_matrix))
    cbar.update_normal(heatmap_img)

    plt.draw()


# Adds components to GUI
def draw_chessboard_heatmap(heatmap_matrix, title="Blunder Heatmap"):
    global fig, ax, cax, cbar, heatmap_img, text_labels

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(right=0.85, bottom=0.15, left=0.1, top=0.9)

    cmap = plt.cm.Reds

    heatmap_img = ax.imshow(heatmap_matrix, cmap=cmap, interpolation="nearest")

    # Draw squares with text
    text_labels = []  # Initialize global label list
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            val = int(heatmap_matrix[i][j])
            label = ax.text(j, i, str(val), ha="center", va="center", color="black", fontsize=9)
            text_labels.append(label)

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

    # Add colorbar to bottom
    cbar = fig.colorbar(heatmap_img, ax=ax, orientation='horizontal', fraction=0.05, pad=0.07)
    cbar.set_label("Blunder Frequency")

    # Add button to right side for to-from squares
    button_ax = fig.add_axes([0.87, 0.65, 0.1, 0.1])  # x, y, width, height in figure coords
    square_button = Button(button_ax, "Toggle\nBlundered\nPiece\nSquare")
    square_button.on_clicked(filter_blundered_squares)

    # Add button to right side for color filtering
    button_ax = fig.add_axes([0.87, 0.45, 0.1, 0.1])
    color_button = Button(button_ax, "Filter\nBy\nPlaying\nColor")
    color_button.on_clicked(filter_color)

    plt.show()

if __name__ == "__main__":
    data = load_blunder_data("blunder_heatmap_data.json")
    matrix = create_heatmap_matrix(data)
    draw_chessboard_heatmap(matrix)

#Features to add:
# piece insights
# time control insights
# toggle between for, to, and both - use radio buttons?
# display: 
    # total blunders
    # best/worst rows/cols
    # worst cell(s)
    # Insights based on above info