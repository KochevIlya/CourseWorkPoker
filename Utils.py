from Poker import *
def print_stats(players):
    for player in players:
        lprint(f"{player.name} has: {player.stack} tips\n")
        print(f"{player.name} has: {player.stack} tips")

def print_cards(players):
    for player in players:
        lprint(f"{' '.join(player._holeCards)}\n")
        print(f"{player._holeCards}")



def lprint(string, sep="\n", end="\n"):
    with open(f"all_log.txt", 'a', newline='') as f:
        f.write(string)
    with open(f"log.txt", 'a', newline='') as f:
        f.write(string)