from itertools import pairwise


hand_categories = ("RoyalFlush",
                   "StraightFlush",
                   "FourofaKind",
                   "FullHouse",
                   "Flush",
                   "Straight",
                   "ThreeofaKind",
                   "TwoPair",
                   "Pair",
                   "HighCard")


def is_royal_flush(hand):
    """
    check if hand contains royal flush
    :return: status, True for royal flush and sorted hand
    :rtype: tuple(True, hand) or tuple(False, None)
    """
    hand.sort(reverse=True)
    b_royal = is_straight_flush(hand)[0] \
              and hand[0].value == "A" \
              and hand[-1].value == "T"
    if b_royal:
        return True, hand
    else:
        return False, None


def is_straight_flush(hand):
    """
    check if hand contains straight flush
    :return: status, True for straight flush and sorted hand
    :rtype: tuple(True, hand) or tuple(False, None)
    """
    hand.sort(reverse=True)
    b_st_flush = is_flush(hand)[0] and is_straight(hand)[0]
    if b_st_flush:
        return True, hand
    else:
        return False, None


def is_fourkind(hand):
    """
    check if hand contains four of a kind
    :return: status, True for four of a kind and sorted hand
    :rtype: tuple(True, hand) or tuple(False, None)
    """
    hand.sort(reverse=True)
    b_foundKind = hand.count(hand[0]) == 4 or hand.count(hand[-1]) == 4
    if b_foundKind:
        return True, hand
    else:
        return False, None


def is_fullhouse(hand):
    """
    check if hand contains full house
    :return: status, True for full house and sorted hand
    :rtype: tuple(True, hand) or tuple(False, None)
    """
    b_isFullHouse, tres = is_threekind(hand)
    if b_isFullHouse:
        other_two = [c for c in hand if c not in tres]
        duo = is_pair(other_two)
        b_isFullHouse = b_isFullHouse and duo[0]
    if b_isFullHouse:
        return True, hand
    else:
        return False, None


def is_flush(hand):
    """
    check if hand contains flush
    :return: status, True for flush and sorted hand
    :rtype: tuple(True, hand) or tuple(False, None)
    """
    hand.sort(reverse=True)
    suites_in_hand = [c.suite for c in hand]
    b_isFlush = suites_in_hand.count(suites_in_hand[0]) == len(suites_in_hand)
    if b_isFlush:
        return True, hand
    else:
        return False, None


def is_straight(hand):
    """
    check if hand contains straight
    :return: status, True for straight and sorted hand
    :rtype: tuple(True, hand) or tuple(False, None)
    """
    hand.sort(reverse=True)
    if hand[0].value == "A" and hand[1].value.isdigit():
        # if Ace in hand but no other face cards, Ace treated as 1
        hand = hand[1:] + hand[0:1]
    card_pairs = list(pairwise(hand))
    deltas = [c1 - c2 for c1, c2 in card_pairs]
    if deltas.count(1) == 4:
        return True, hand
    else:
        return False, None


def is_threekind(hand):
    """
    check if hand contains three of a kind
    :return: status and three of a kind cards
    :rtype: tuple(True, (Card,Card,Card)) or tuple(False, None)
    """
    hand.sort(reverse=True)
    for i in range(3):
        tres = hand[i:i + 3]
        if tres[0].value == tres[1].value == tres[2].value:
            return True, tres
    return False, None


def is_twopair(hand):
    """
    check if hand contains two pairs
    :return: status and pairs of cards if they exist
    :rtype: tuple(True, (Card,Card, Card, Card)) or tuple(False, None)
    """
    hand.sort(reverse=True)
    card_pairs = list(pairwise(hand))
    two_pairs = []
    skipNext = False
    for c1, c2 in card_pairs:
        if skipNext:
            skipNext = False
        elif c1.value == c2.value:
            two_pairs.extend([c1, c2])
            skipNext = True
            # to avoid detecting a triple as two pair, skip the next overlapping pair
    if len(two_pairs) == 4:
        return True, two_pairs
    else:
        return False, None


def is_pair(hand):
    """
    check if hand contains pair
    :return: status and pair of cards if they exist
    :rtype: tuple(True, (Card,Card)) or tuple(False, None)
    """
    hand.sort(reverse=True)
    card_pairs = list(pairwise(hand))
    for c1, c2 in card_pairs:
        if c1.value == c2.value:
            return True, (c1, c2)
    return False, None


def is_highcard(hand):
    """
    check if hand is of type HighCard and return the high card
    :param hand: a list of five Cards
    :return: tuple(True, Card) Card is the highest card in hand
    :rtype: tuple(bool, Card)
    """
    hand.sort(reverse=True)
    return True, hand[0]