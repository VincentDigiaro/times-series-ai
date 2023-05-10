import os
import sys
import subprocess
from sgfmill import sgf, sgf_moves

KATAGO_PATH = "C:\\Users\\Digiaro\\Desktop\\KATAGO\\katago.exe"
CONFIG_PATH = "C:\\Users\\Digiaro\\Desktop\\KATAGO\\default_gtp.cfg"
SGF_PATH = "C:\\Users\\Digiaro\\Desktop\\KATAGO\\mecSolid.sgf"
MOVE_NUMBER = 5



# Load SGF file
with open(SGF_PATH, "rb") as f:
    sgf_data = f.read()

# Parse SGF file
game = sgf.Sgf_game.from_bytes(sgf_data)
board, plays = sgf_moves.get_setup_and_moves(game)

# Set up a GTP pipe to KataGo
katago = subprocess.Popen([KATAGO_PATH, "gtp", "-config", CONFIG_PATH],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, universal_newlines=True)

# Send GTP commands to load moves
for color, move in plays[:MOVE_NUMBER]:
    katago.stdin.write(f"play {color} {move}\n")
    katago.stdin.flush()
    response = katago.stdout.readline().strip()

# Request analysis for the current move
katago.stdin.write(f"kata-analyze {plays[MOVE_NUMBER-1][0]} 10\n")
katago.stdin.flush()

# Read and parse KataGo's response
while True:
    response = katago.stdout.readline().strip()
    if response.startswith("="):
        break
    elif response.startswith("info"):
        _, move, _, winrate, _, score, *_ = response.split()
        if move == plays[MOVE_NUMBER-1][1]:
            points_lost = float(score) - float(plays[MOVE_NUMBER-1][2])
            print(f"Points lost by move {MOVE_NUMBER}: {points_lost:.2f}")
            break
