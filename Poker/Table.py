from Player import Player
from simple_bot import SimpleGeneticBot
from .poker_rules import best_hand

def winning_player(players):
    """
    given a list of players, return the winners who have the best poker hand
    
    :param players: list of [Player] objects
    :return: list of players that won
    :rtype: list[Player]
    """
    active_players = [p for p in players if p.in_hand]
    player_best_hands = [p.get_best_hand() for p in active_players]
    winning_hand = best_hand(player_best_hands)
    winners = [p for p in active_players if p.get_best_hand() == winning_hand]
    return winners