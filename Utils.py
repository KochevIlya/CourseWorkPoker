from Poker import *
def print_stats(players):
    for player in players:
        print(f"{player.name} has: {player.stack} tips")

def print_cards(players):
    for player in players:
        print(f"{player._holeCards}")