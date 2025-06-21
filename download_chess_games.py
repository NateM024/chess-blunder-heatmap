import berserk

# Create an anonymous client (no token needed)
client = berserk.Client()

def download_lichess_games(username, max_games=20, output_file="games.pgn"):
    print(f"Downloading up to {max_games} games for user: {username}")
    with open(output_file, "w", encoding="utf-8") as f:
        for game in client.games.export_by_player(username, max=max_games, as_pgn=True):
            f.write(game + "\n\n")
    print(f"Saved games to {output_file}")

if __name__ == "__main__":
    download_lichess_games("NateChess24", max_games=10)
