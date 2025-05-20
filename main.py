from Poker import *
from Player import *
from simple_bot import *
from Utils import *
from genetic import *
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
for j in range(num_simulations):
    
    num_players = 8
    blind = 0
    bet = 10
    player_indx = 3
    game = 0
    players = [
        SimpleGeneticBot([1.0, 0.0, 0.5], name="Bot_A"),
        SimpleGeneticBot([0.8, 0.8, 0.3], name="Bot_B"),
        SimpleGeneticBot([0.6, 0.5, 0.2], name="Bot_C"),
        SimpleGeneticBot([0.8, 0.1, 0,5], name="Bot_D"),
        SimpleGeneticBot([0.4, 0.5, 0,1], name="Bot_E"),
        SimpleGeneticBot([0.9, 0.1, 0,5], name="Bot_F"),
        SimpleGeneticBot([0.6, 0.7, 0.2], name="Bot_G"),
    ]
    reference_genomes = [
        [1.0, 0.0, 0.5],
        [0.8, 0.8, 0.3],
        [0.6, 0.5, 0.2],
        [0.8, 0.1, 0,5],
        [0.4, 0.5, 0,1],
        [0.9, 0.1, 0,5],
    ]

    winers = []
    losers = list()
    sim = 0 
    evoluate(10, 0.1, 0.1, reference_genomes, sims=20)
    while(len(players) > 1 and sim <= 50):
        blind = (blind + 1) % len(players)
        print(f'game{game}')
        print_stats(players)
        game += 1
        # define a deck of cards
        play_deck = Deck()
        play_deck.shuffle()
        assert len(play_deck) == 52

        # set players
        
        # deal cards
        for _ in range(2):
            for p in players:
                p.add_card(play_deck.dealcard())

        for p in players:
            p_hand = p.get_holecards_pokernotation()
            starting_hands_stats[p_hand]['played'] += 1

        # print_cards(players)
        bet_blind(players, bet, blind)
        pot = bet
        table = []

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")

        play_deck.dealcard() # burn before flop
        flop_cards = [play_deck.dealcard() for _ in range(3)]
        # print("Flop:", flop_cards)
        # print(players)
        table = flop_cards
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")

        play_deck.dealcard() # burn before flop
        turn_card = [play_deck.dealcard()]
        # print("Turn:", turn_card)

        table += turn_card
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")

        play_deck.dealcard() # burn before flop
        river_card = [play_deck.dealcard()]
        # print("River:", river_card)
        table += river_card
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")
        print("Table: ", table)

        for p in players:
            bh = p.update_best_hand(table)
            print(p.get_holecards(), end= " ")
            print(poker_rules.categorize_hand(bh), bh)
        

        for p in winning_player(players):
            print (f'Выигрывает: {p.name}')
            p.stack += pot
            p_hand = p.get_holecards_pokernotation()
            starting_hands_stats[p_hand]['won'] += 1
        
        

        # with open(f"simulation_{n}.csv", 'w', newline='') as f:
        #     cols = ['hand','won','played']
        #     w = csv.DictWriter(f, cols)
        #     w.writeheader()
        #     for hand, stat in starting_hands_stats.items():
        #         row = {"hand": hand}
        #         row.update(stat)
        #         w.writerow(row)

        losers.append(l for l in players if l.stack == 0)
        players = [player for player in players if player.stack >= 10]
        post_game(players)
        sim+= 1
    
winers = [p for p in players if p.stack > 0]
maxim = max(pl.stack for pl in winers)
winer = ""
for p in winers:
    if p.stack == maxim:
        winer = p.name


print(f'Победитель: {winer}')