from .Card import Card
from itertools import combinations

def create_stats_dict(starting_hands_stats, stats_dict):
    """
    updated input dictionary with 169 keys representing the unique starting hands in poker
    each key maps to a nested statistics dictionary
    
    :param starting_hands_stats: empty dict
    :return: None
    """    
    pocket_pairs = [c*2 for c in Card.static_cardvalues]
    combos = list(combinations(Card.static_cardvalues, 2))  # 13C2 = 78 two card combinations
    suited_hands = [b+a+'s' for a,b in combos]  # 78 suited two card combinations
    offsuite_hands = [b+a+'o' for a,b in combos]  # any two offsuite cards
    starting_hands_stats.update({k: stats_dict.copy() for k in pocket_pairs + suited_hands + offsuite_hands})

