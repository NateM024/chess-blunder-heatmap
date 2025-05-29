# ♟️ Lichess Blunder Heatmap Visualizer

Visualize your chess blunders with interactive heatmaps based on your actual games from Lichess!

---

## 🔍 Project Overview

This project provides a set of Python scripts to:

1. **Download your public chess games** from Lichess in PGN format.
2. **Analyze moves and identify blunders** using engine evaluations or Lichess annotations.
3. **Create heatmap visualizations** highlighting the squares on the chessboard where you make the most mistakes.

The goal is to help chess players understand their weak points on the board and improve more efficiently.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- [Lichess account](https://lichess.org)
- Basic Python knowledge

### Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/yourusername/lichess-blunder-heatmap.git
    cd lichess-blunder-heatmap
    ```

2. (Optional) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Usage

### Step 1: Download games

Edit `download_lichess_games.py` and set your Lichess username. Then run:

```bash
python download_lichess_games.py