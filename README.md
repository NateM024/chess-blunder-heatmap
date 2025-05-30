# ♟️ Lichess Blunder Heatmap Visualizer

A Python tool to analyze your chess games for blunders using the Stockfish engine and visualize blunder frequencies on a chessboard heatmap.

---

## Features

- **Downloads your games** from Lichess via the API (PGN format).  
- **Analyze blunders automatically** using Stockfish (local engine).  
- **Generate a heatmap visualization** showing which squares have the highest blunder frequency.  
- Simple, clean GUI output with adjustable figure size and a bottom-positioned colorbar.  

---

## Getting Started

### Prerequisites

- Python 3.7+  
- [Stockfish](https://stockfishchess.org/download/) engine executable  
- Required Python packages (install via pip): pip install chess matplotlib requests


### Set Up
1. Download your games:
   Run download-chess-games.py to fetch your Lichess games. Make sure to use the correct username

2. Analyze blunders:
   Run analyze_blunders.py to process your downloaded games with Stockfish and generate blunder data. Make sure to use the correct username.

3. Visualize heatmap:
   Run draw_heatmap.py to display the blunder frequency heatmap.

#### Stockfish Set Up
- Update the STOCKFISH_PATH in analyze_blunders.py to match where it is on your computer

---

## Trouble Shooting
- Ensure Stockfish path is correct and executable has proper permissions.

- Use raw string literals for Windows paths (r"C:\Tools\stockfish.exe").

- If visualization is too large or small, adjust figsize in draw_heatmap.py.

---

## Future Improvements
- Filter blunders by piece type or game phase.

- Export heatmap images.

- Include heatmaps for mistakes, best moves, etc.

- Overall GUI improvements