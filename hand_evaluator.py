suits = ('Spades', 'Hearts', 'Diamonds', 'Clubs')

cards = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

cards_value = {card: cards.index(card)+2 for card in cards}

straight_combs = [{i, i+1, i+2, i+3, i+4} for i in range(2, 11)]
straight_combs.insert(0, {14, 2, 3, 4, 5})
straight_combs.reverse()


def hand_level(flop, hand):
    """Takes a hand and a flop and returns a hand level with (if needed)
    additional information on high cards to evaluate the hand"""

    pair = False
    two_pairs = False
    three_of_a_kind = False
    straight = False
    flush = False
    full_house = False
    quads = False
    straight_flush = False
    royal_flush = False

    all = hand + flop

    hand_cards = [cards_value[card] for (card, _) in hand]
    hand_suits = [suit for (_, suit) in hand]

    flop_cards = [cards_value[card] for (card, _) in flop]
    flop_suits = [suit for (_, suit) in flop]

    all_cards = hand_cards + flop_cards
    all_suits = hand_suits + flop_suits

    high_card = sorted(all_cards, reverse=True)[:5]
    pair_cards = []
    three_of_a_kind_card = None
    straight_high_card = None
    flush_level = None
    flush_level_check_straight_flush = None
    full_house_cards = []
    quad_card = None

    for card in all_cards:
        card_count = all_cards.count(card)

        # Quads
        if card_count == 4 and card != quad_card:
            quads = True
            quad_card = card

        # Three of a Kind
        elif card_count == 3 and card != three_of_a_kind_card:
            three_of_a_kind = True
            if three_of_a_kind_card:
                if card > three_of_a_kind_card:
                    three_of_a_kind_card = card
            else:
                three_of_a_kind_card = card

        # Pair and Two Pairs
        elif card_count == 2 and card not in pair_cards:
            pair = True
            pair_cards.append(card)
            if len(pair_cards) >= 2:
                two_pairs = True
                pair_cards = sorted(pair_cards, reverse=True)[:2]

    # Flush
    for suit in all_suits:
        if all_suits.count(suit) >= 5:
            flush = True
            flush_level_check_straight_flush = sorted(
                [cards_value[card] for (card, suit) in all if suit == suit], reverse=True)
            flush_level = flush_level_check_straight_flush[:5]

    # Straight, Straight Flush and Royal Flush
    # Straight
    for comb in straight_combs:
        if comb.issubset(all_cards):
            straight = True
            # Check for low straight
            if comb != straight_combs[-1]:
                straight_high_card = max(comb)
            else:
                straight_high_card = 5

        # Straight Flush
        if straight and flush:
            if comb.issubset(flush_level_check_straight_flush):
                straight_flush = True
                # Check for royal flush
                if comb == straight_combs[0]:
                    royal_flush = True

    # Full house
    if three_of_a_kind and pair:
        full_house = True
        full_house_cards.append(three_of_a_kind_card)
        full_house_cards.append(max(pair_cards))

    hand_level = 0

    # Sorts out hand level and returns it with additional info
    if royal_flush:
        hand_level = 9
        return (hand_level, 'Royal Flush Motherfucker')
    elif straight_flush:
        hand_level = 8
        return (hand_level, straight_high_card)
    elif quads:
        hand_level = 7
        high_card = max(card for card in all_cards if card != quad_card)
        return (hand_level, high_card)
    elif full_house:
        hand_level = 6
        return (hand_level, full_house_cards)
    elif flush:
        hand_level = 5
        return (hand_level, flush_level)
    elif straight:
        hand_level = 4
        return (hand_level, straight_high_card)
    elif three_of_a_kind:
        hand_level = 3
        n_all_cards = [card for card in all_cards if card != three_of_a_kind_card]
        highest_cards = sorted(n_all_cards, reverse=True)[:2]
        return (hand_level, three_of_a_kind_card, highest_cards)
    elif two_pairs:
        hand_level = 2
        n_all_cards = [card for card in all_cards if card not in pair_cards]
        high_card = max(n_all_cards)
        return (hand_level, pair_cards, high_card)
    elif pair:
        hand_level = 1
        n_all_cards = [card for card in all_cards if card not in pair_cards]
        highest_cards = sorted(n_all_cards, reverse=True)[:3]
        return (hand_level, pair_cards[0], highest_cards)
    else:
        hand_level = 0
        return (hand_level, high_card)
