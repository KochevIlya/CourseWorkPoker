import random
from Poker import *
from Poker.ranking_cards import *
class SimpleGeneticBot:
    


    def __init__(self, genome, stack=100, name="Bot", min_bet=10, place=0):
        
        self.name = str(name)
        self._holeCards = []
        self._bestHand = None
        self.place = 0
        self.active_folds = 0
        self.stack = stack
        self.in_hand = True
        self.desicion = ""
        self.genome = genome
        self.min_bet = min_bet
        self.bet = 0
        self.game_bet = 0
        self.num_folds = 0
        self.num_played = 0

    def __str__(self):
        if not self._bestHand:
            return self.name + ":" + str(self._holeCards)
        else:
            return self.name + ":" + str(self._bestHand) + "," + categorize_hand(self._bestHand)
        
    def __repr__(self):
        return str(self)

    def evaluate_hand_strength(self, hand, community_cards):
        
        return poker_strength(hand, community_cards, iters=1000 )

    def make_decision(self, hand, community_cards, min_call):
        hand_strength = self.evaluate_hand_strength(hand, community_cards)
        bluff_rand = random.random()
        
        score = self.genome[0] * hand_strength + self.genome[1] * bluff_rand - self.genome[2] * self.game_bet / (self.game_bet + self.stack)
     
        if score > 0.8:
            return 'raise'
        elif score > 0.4:
            return 'call'
        else:
            return 'fold'
        
    def reset_for_new_hand(self):
        self._holeCards = []
        self._bestHand = None
        self.place = 0
        self.active_folds = 0
        self.in_hand = True
        self.desicion = ""
        self.bet = 0
        self.game_bet = 0
        self.num_folds = 0
        self.num_played = 0


    def add_card(self, c):
        if len(self._holeCards) < 2:
            self._holeCards.append(c)
        else:
            raise ValueError("Player can only have two hole cards")
    
    def get_holecards_pokernotation(self):
        
        self._holeCards.sort(reverse=True)
        poker_notation = self._holeCards[0].value + self._holeCards[1].value
        if poker_notation[0] == poker_notation[1]:
            return poker_notation
        else:
            if self._holeCards[0].suite == self._holeCards[1].suite:
                poker_notation = poker_notation + "s"
            else:
                poker_notation = poker_notation + "o"
            return poker_notation
    def reset_player(self, stack = 100, min_bet=10):
        self._holeCards = []
        self._bestHand = None
        self.place = 0
        self.active_folds = 0
        self.stack = stack
        self.in_hand = True
        self.desicion = ""
        self.min_bet = min_bet
        self.bet = 0
        self.game_bet = 0
        self.num_folds = 0
        self.num_played = 0

        
    def update_best_hand(self, table):
        
        if len(table) < 3:
            raise ValueError("table has insufficient community cards")
        if len(table) >= 3:
            lst_hands = [list(combo) for combo in combinations(self._holeCards + table, 5)]
            self._bestHand = best_hand(lst_hands)
            self._bestHand.sort(reverse=True)
            return self._bestHand    


    def get_holecards(self):
        return self._holeCards

    def get_best_hand(self):
        if not self._bestHand:
            raise ValueError("Best hand undetermiend. Call update_best_hand")
        return self._bestHand

    def get_desicion(self):
        return self.desicion