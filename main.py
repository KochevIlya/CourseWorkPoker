from Poker import *
from Player import *
from simple_bot import *
from Utils import *
from genetic import *
import matplotlib.pyplot as plt
from collections import defaultdict

open(f"log.txt", "w")
starting_hands_stats = {}


hand_stats = {'won': 0, 'played': 0}
create_stats_dict(starting_hands_stats, hand_stats)
results_stack = defaultdict(int)
results_times = defaultdict(int)
num_simulations = 100
for j in range(num_simulations):
    
    num_players = 8
    blind = 0
    bet = 10
    player_indx = 3
    game = 0
    players = [
    SimpleGeneticBot([0.9, 0.1, 0.2], name="Aggressor"),
    SimpleGeneticBot([0.2, 0.1, 0.9], name="Tight"),
    SimpleGeneticBot([0.4, 0.9, 0.4], name="Bluff"),
    SimpleGeneticBot([0.5, 0.5, 0.5], name="Balanced"),
    SimpleGeneticBot([0.9, 0.9, 0.2], name="Maniac"),
    
    ]

    reference_genomes = [
        [0.9, 0.1, 0.2],
        # [0.8, 0.8, 0.3],
        # [0.6, 0.5, 0.2],
        # [0.8, 0.1, 0,5],
        # [0.4, 0.5, 0,1],
        # [0.9, 0.1, 0,5],
    ]

    winers = []
    losers = list()
    sim = 0 
    #best_players = evoluate(100, 0.1, 0.1, reference_genomes, sims=100)
                            
    # with open(f"results_bots.txt", 'a', newline='') as f:
            
    #         for bot in best_players:
    #             f.write(f'[ ')
    #             for i in bot[0].genome:
    #                 f.write(f'{i}, ')
    #             f.write(f"]'\n'")

    #players = best_players
    for i in players: 
        i.reset_player()
    while(len(players) > 1 and sim <= 50):
        blind = (blind + 1) % len(players)
        print(f'game{game}')
        lprint(f'game{game}\n')
        
        print_stats(players)
        game += 1
        
        play_deck = Deck()
        play_deck.shuffle()
        assert len(play_deck) == 52

      
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

        pot, actions = betting_round(players, bet, pot, table,  blind + 1, is_placeble=False)
        inp = "\n".join(actions)
        lprint(inp, sep="\n")
        print(*actions, sep="\n")


        play_deck.dealcard() 
        flop_cards = [play_deck.dealcard() for _ in range(3)]
        # print("Flop:", flop_cards)
        # print(players)
        table += flop_cards
        inp = "\n".join(actions)
        lprint(inp, sep="\n")
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1, is_placeble=False)
        inp = "\n".join(actions)
        lprint(inp, sep="\n")
        print(*actions, sep="\n")

        play_deck.dealcard()
        turn_card = [play_deck.dealcard()]
        # print("Turn:", turn_card)

        table += turn_card
        lprint("Table: ", table)
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1, is_placeble=False)
        inp = "\n".join(actions)
        lprint(inp, sep="\n")
        print(*actions, sep="\n")

        play_deck.dealcard()
        river_card = [play_deck.dealcard()]
        # print("River:", river_card)
        table += river_card
        lprint("Table: ", table)
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1, is_placeble=False)
        inp = "\n".join(actions)
        lprint(inp, sep="\n")
        print(*actions, sep="\n")
        lprint("Table: ", table)
        print("Table: ", table)

        for p in players:
            bh = p.update_best_hand(table)
            print(p.get_holecards(), end= " ")
            print(poker_rules.categorize_hand(bh), bh)
        

        for p in winning_player(players):
            lprint (f'Выигрывает: {p.name}\n')
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
        results_stack[p.name] += p.stack
        results_times[p.name] += 1

names = list(results_stack.keys())
stacks = list(results_stack.values())

plt.figure(figsize=(10, 5))
plt.bar(names, stacks, color='skyblue')
plt.xlabel('Боты')
plt.ylabel('Итоговый стек')
plt.title('Результаты стратегий ботов после симуляции')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("strategy_results.png")
plt.show()

names = list(results_times.keys())
times = list(results_times.values())

plt.figure(figsize=(10, 5))
plt.bar(names, times, color='red')
plt.xlabel('Боты')
plt.ylabel('Количество выигрышей')
plt.title('Результаты стратегий ботов по числу выигрышей')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("strategy_win_times.png")
plt.show()

lprint(f'Победитель: {winer}\n')
print(f'Победитель: {winer}')