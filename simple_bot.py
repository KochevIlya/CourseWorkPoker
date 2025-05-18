import random
from Poker import *

class SimpleGeneticBot:
    def __init__(self, genome, name="Bot"):
        # genome = [вес силы руки, вес блефа]
        self.genome = genome
        self.name = name
        self.in_hand = True
        self.bet = 0
        self.stack = 1000  # например, стартовый стэк

    def evaluate_hand_strength(self, hand, community_cards):
        # Monte Carlo или простая оценка
        return poker_strength(hand, community_cards, iters=1000 )

    def make_decision(self, hand, community_cards, min_call):
        hand_strength = self.evaluate_hand_strength(hand, community_cards)
        bluff_rand = random.random()
        # Векторное произведение (или сумма, если хочешь)
        score = self.genome[0] * hand_strength + self.genome[1] * bluff_rand
        # Пороговые значения на твой вкус (0.5, 0.7 и т.д.)
        if score > 0.8:
            return 'raise'
        elif score > 0.4:
            return 'call'
        else:
            return 'fold'