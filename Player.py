from Poker.poker_rules import *
from itertools import combinations
from Utils import *


class Player:
    def __init__(self, name="Player", stack=100, min_bet=10, place = 0):
        self.min_bet = min_bet
        self.name = str(name)
        self._holeCards = []
        self.place = place
        self.active_folds = 0
        self._bestHand = None
        self.stack = stack
        self.in_hand = True
        self.bet = 0
        self.desicion = ""
        self.acted_this_round = False
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

    def ask_player(self):
        lprint(f'Ваши карты: {self._holeCards}, вы поставили {self.game_bet}')
        print(f'Ваши карты: {self._holeCards}, вы поставили {self.game_bet}')
        desicion = int(input())
        self.make_decision(desicion)

    def reset_for_new_hand(self):
        self._holeCards = []
        self.active_folds = 0
        self._bestHand = None
        self.in_hand = True
        self.bet = 0
        self.desicion = ""
        self.acted_this_round = False
        self.game_bet = 0
        self.num_folds = 0
        self.num_played = 0

    def add_card(self, c):
        if len(self._holeCards) < 2:
            self._holeCards.append(c)
        else:
            raise ValueError("Player can only have two hole cards")

    def make_decision(self, desicion):
        desicions = {
            1 : "fold",
            2 : "call",
            3 : "raise"
        }
        self.desicion = desicions[desicion]


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