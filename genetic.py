import random
import copy
from Poker import *

def crossover(g1, g2):
   
    return [(a + b) / 2 for a, b in zip(g1, g2)]

def mutate(genome, mutation_rate, mutation_strength):
    
    return [
        max(0, min(1, g + (random.uniform(-mutation_strength, mutation_strength) if random.random() < mutation_rate else 0)))
        for g in genome
    ]

def fitnes(tuple):
    
    bot = tuple[0]
    total_rate = tuple[3]
    fold_rate = bot.num_folds / bot.num_played
    if fold_rate > 0.9:
        total_rate *= 0.5
    return total_rate

def run_game_tournament(candidate_bots, reference_bots, num_games=5, stack=100, num_sims=50):
   


    for bot in candidate_bots + reference_bots:
        bot.stack = stack
        bot._holeCards = []
        bot._bestHand = None
        bot.in_hand = True
    ref_one = random.sample(reference_bots, 1)
    bots = candidate_bots + [copy.deepcopy(b) for b in ref_one]
       
    sorted_results = run_full_poker_game(bots, sims=num_sims)
    results = []
    
    i = 0
    for bot in sorted_results:
        if bot in candidate_bots:
            results.append( (bot, bot.stack, False, i) )
            i += 1
    for bot in sorted_results:
        if bot not in candidate_bots:
            results.append( (bot, bot.stack, True, i) )
            i += 1
    return results

def evoluate(
        num_generations, mutation_rate, mutation_strength, reference_genomes, sims=50, 
        places_dict={
    0 : 10,
    1 : 10,
    2 : 9,
    3 : 9,
    4 : 7,
    5 : 7,
    6 : 5,
    7 : 5,
    8 : None
    }
             ):
    """
    :param num_generations: число поколений
    :param mutation_rate: вероятность мутации каждого гена
    :param mutation_strength: сила мутации (максимальное изменение)
    :param reference_genomes: список геномов эталонных ботов (длина 6)
    :return: список из 6 лучших ботов последней популяции
    """
    reference_bots = [SimpleGeneticBot(g, name=f"Ref_{i}", place=8) for i, g in enumerate(reference_genomes)]
    population = [SimpleGeneticBot([random.random(), random.random(), random.random()], name=f"Gen_{i}", place=places_dict[i]) for i in range(7)]

    for gen in range(num_generations):
        
        results = run_game_tournament(population, reference_bots, num_sims=sims)
        
        candidates = [item for item in results if not item[2]]
        candidates.sort(key=lambda x: fitnes(x))


       
        if len(candidates) < 4:
            raise Exception("Too few candidates left for selection/crossover!")
        
        with open(f"genetic_bots.txt", 'w', newline='') as f:
            f.write(f'generation{gen}\n')
            for bot in results:
                f.write(f'[ ')
                for i in bot[0].genome:
                    f.write(f'{i}, ')
                f.write(f"]'\n'")

        
        bot1, bot2, bot3, bot4, bot5, bot6, bot7 = [c[0] for c in candidates[:7]]
        
        next_gen = [
            copy.deepcopy(bot1),
            copy.deepcopy(bot2),
            SimpleGeneticBot(mutate(crossover(bot1.genome, bot2.genome), mutation_rate, mutation_strength), name="Child_1"),
            SimpleGeneticBot(mutate(crossover(bot2.genome, bot3.genome), mutation_rate, mutation_strength), name="Child_2"),
            SimpleGeneticBot(mutate(crossover(bot3.genome, bot4.genome), mutation_rate, mutation_strength), name="Child_3"),
            SimpleGeneticBot([random.random(), random.random(), random.random()], name=f"Random_{1}"),
            SimpleGeneticBot(mutate(bot1.genome, mutation_rate, mutation_strength), name="Mutant_1"),
        ]
        for i in range(len(next_gen)):
            next_gen[i].place = places_dict[i]
        population = next_gen
        print(f"Поколение {gen+1}: лучший стек (из кандидатов) = {candidates[0][1]:.1f}, геном: {candidates[0][0].genome}")
    
    return population

def run_full_poker_game(players, stack=100, min_bet=10, sims=50):
    num_players = 8
    blind = 0
    bet = min_bet
    #player_indx = 3
    game = 0
    losers = list()
    sim = 0 
    
    while(len(players) > 1 and sim <= sims):
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

        # for p in players:
        #     p_hand = p.get_holecards_pokernotation()
        #     starting_hands_stats[p_hand]['played'] += 1

        # print_cards(players)
        bet_blind(players, bet, blind)
        pot = bet
        table = []

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")

        play_deck.dealcard() 
        flop_cards = [play_deck.dealcard() for _ in range(3)]
        # print("Flop:", flop_cards)
        # print(players)
        table = flop_cards
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")

        play_deck.dealcard()
        turn_card = [play_deck.dealcard()]
        # print("Turn:", turn_card)

        table += turn_card
        print("Table: ", table)

        pot, actions = betting_round(players, bet, pot, table,  blind + 1)
        print(*actions, sep="\n")

        play_deck.dealcard() 
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
            #p_hand = p.get_holecards_pokernotation()
            # starting_hands_stats[p_hand]['won'] += 1
        
        

        # with open(f"simulation_{n}.csv", 'w', newline='') as f:
        #     cols = ['hand','won','played']
        #     w = csv.DictWriter(f, cols)
        #     w.writeheader()
        #     for hand, stat in starting_hands_stats.items():
        #         row = {"hand": hand}
        #         row.update(stat)
        #         w.writerow(row)
        for p in players:
            if p.stack == 0:
                losers.append(p)  
        players = [player for player in players if player.stack >= 10]
        post_game(players)
        sim+= 1
    players.sort(key= lambda x: x.stack)
    results = losers + players
    return results