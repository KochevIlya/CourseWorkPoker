from Poker import *
from Player import *

# card1 = Card("Heart", "A")
# card2 = Card("Spade", "A")
# card3 = Card("Heart", "Q")
# card4 = Card("Heart", "J")
# card5 = Card("Heart", "T")

# _card1 = Card("Heart", "A")
# _card2 = Card("Spade", "A")
# _card3 = Card("Heart", "Q")
# _card4 = Card("Spade", "J")
# _card5 = Card("Spade", "T")

# _card6 = Card("Diamond", "2")
# _card7 = Card("Club", "T")

# hand = [card1, card2, card3, card4, card5]
# hand2 = [_card1, _card2, _card3, _card4, _card5]
# hands = [hand, hand2]

# player = Player("Ilya")
# player.add_card(_card6)
# player.add_card(_card7)

# player.update_best_hand(hand2)

# print(player.get_best_hand())
# print(player.get_holecards_pokernotation())


import csv 


starting_hands_stats = {}

# dict to track win/loss stats
hand_stats = {'won': 0, 'played': 0}
create_stats_dict(starting_hands_stats, hand_stats)

num_simulations = 1
num_players = 8
n = num_players
blind = 0
bet = 10
player_indx = 3

for i in range(num_simulations):
    if i % 100 == 0:
        print(f"game{i}")
    # define a deck of cards
    play_deck = Deck()
    play_deck.shuffle()
    assert len(play_deck) == 52

    # set players
    players = [Player(f"Player{p}", 100) for p in range(n)]
    for i in players:
        i.make_decision(2)
    # deal cards
    for _ in range(2):
        for p in players:
            p.add_card(play_deck.dealcard())

    for p in players:
        p_hand = p.get_holecards_pokernotation()
        starting_hands_stats[p_hand]['played'] += 1

    bet_blind(players, bet, blind)
    pot = bet
    

    pot, actions = betting_round(players, bet, pot, blind + 1)
    print(*actions, sep="\n")

    play_deck.dealcard() # burn before flop
    flop_cards = [play_deck.dealcard() for _ in range(3)]
    print("Flop:", flop_cards)
    # print(players)
    table = flop_cards
    print("Table: ", table)

    pot, actions = betting_round(players, bet, pot, blind + 1)
    print(*actions, sep="\n")

    play_deck.dealcard() # burn before flop
    turn_card = [play_deck.dealcard()]
    print("Turn:", turn_card)

    table += turn_card
    print("Table: ", table)

    pot, actions = betting_round(players, bet, pot, blind + 1)
    print(*actions, sep="\n")

    play_deck.dealcard() # burn before flop
    river_card = [play_deck.dealcard()]
    print("River:", river_card)
    table += river_card
    print("Table: ", table)

    pot, actions = betting_round(players, bet, pot, blind + 1)
    print(*actions, sep="\n")
    print("Table: ", table)

    for p in players:
        bh = p.update_best_hand(table)
        print(p.get_holecards(), end= " ")
        print(poker_rules.categorize_hand(bh), bh)
    

    for p in winning_player(players):
        print (f'Выигрывает: {p.name}')
        p_hand = p.get_holecards_pokernotation()
        starting_hands_stats[p_hand]['won'] += 1
    
    

    with open(f"simulation_{n}.csv", 'w', newline='') as f:
        cols = ['hand','won','played']
        w = csv.DictWriter(f, cols)
        w.writeheader()
        for hand, stat in starting_hands_stats.items():
            row = {"hand": hand}
            row.update(stat)
            w.writerow(row)