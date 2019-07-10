from hand_evaluator import hand_level, suits, cards
from random import shuffle


class Player():

    def __init__(self):

        self.hand = []


class DeckOfCards():

    def __init__(self):

        self.deck = []
        self.cards = []
        self.burned_cards = []

    def new_deck(self):

        self.deck = [(card, color) for card in cards for color in suits]
        self.cards = []
        self.burned_cards = []

    def shuffle_deck(self):

        shuffle(self.deck)

    def deal(self):
        cards = [self.deck.pop(), self.deck.pop()]
        for card in cards:
            self.burned_cards.append(card)
        return cards

    def one_card(self):
        card = self.deck.pop()
        self.burned_cards.append(card)

        return card

    def flop(self):

        for i in range(8):
            if i == 0 or i == 4 or i == 6:
                self.burned_cards.append(self.deck.pop())
            elif 1 <= i < 4 or i == 5 or i == 7:
                self.cards.append(self.deck.pop())

        return self.cards

    def reset_deck(self):

        for card in self.burned_cards:
            self.deck.append(card)

        self.burned_cards = []

        for card in self.cards:
            self.deck.append(card)

        self.cards = []

    def give_hands(self, list_of_players_cards_variable):
        for i in range(2):
            for player in list_of_players_cards_variable:
                player.append(self.deck.pop())

    def simulated_hands(self, number_of_hands_to_sim):
        for i in range(number_of_hands_to_sim):
            self.burned_cards.append(self.deck.pop())
            self.burned_cards.append(self.deck.pop())


def win_simulations(hand, flop=[], number_of_sim_to_run=10000, total_number_of_players=5):
    """Runs n number of simulations for m number of players given a hand and optionaly a flop.
    Prints the results of games won through specific hands, as well as general stats about the hand"""

    print('Hand: ', hand)
    print('Number of simulations: ', number_of_sim_to_run)

    # Counters for hands gotten and hands that won
    dict_hands = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
                  5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    dict_won_hands = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
                      5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    number_of_win = 0
    players = []

    # Creates Player instances
    for i in range(total_number_of_players-1):
        players.append(Player())

    d = DeckOfCards()
    d.new_deck()

    for i in range(number_of_sim_to_run):
        d.shuffle_deck()
        # Removes the given hand from the deck to avoid doubles
        d.deck.remove(hand[0]), d.deck.remove(hand[1])
        # Adds them to the burned cards for later use in reset_deck()
        d.burned_cards.append(hand[0]), d.burned_cards.append(hand[1])

        # Check if a flop was given
        if len(flop) == 0:
            new_flop = d.flop()

        # If 3 flop cards were given
        elif len(flop) == 3:
            new_flop = []
            for card in flop:
                new_flop.append(card)
                d.deck.remove(card)
                d.burned_cards.append(card)
            river_and_turn = d.deal()
            new_flop.append(river_and_turn[0])
            new_flop.append(river_and_turn[1])

        # If 4 flop cards were given
        elif len(flop) == 4:
            new_flop = []
            for card in flop:
                new_flop.append(card)
                d.deck.remove(card)
                d.burned_cards.append(card)
            new_flop.append(d.one_card())

        else:
            new_flop = flop

        # Deal hands to simulated players
        for player in players:
            player.hand = d.deal()

        # Evaluates level of given hand
        game_p1 = hand_level(new_flop, hand)

        # Evaluates level of simulated player hands
        i = 2
        games = []
        for player in players:
            games.append(hand_level(new_flop, player.hand))

        p1_hand_level = game_p1[0]

        # Duels won counter
        won = 0
        # Evaluting simulated player hands against given hand
        for game in games:
            game_hand_level = game[0]
            dict_hands[game_hand_level] += 1
            # Check higher for hand_level
            if p1_hand_level > game_hand_level:
                won += 1
                continue

            # elif p1_hand_level < game_hand_level:
                # dict_hands[game_hand_level] += 1
                # continue

            # If they are equal, start looking for high cards and stuff
            elif p1_hand_level == game_hand_level:

                # Royal Flush
                if p1_hand_level == 9:
                    won += 1
                    continue

                # Sraight and Straight Flush
                elif p1_hand_level in (4, 7, 8):
                    if game_p1[1] >= game[1]:
                        won += 1
                        continue
                    # else:
                        # dict_hands[game_hand_level] += 1
                        # continue

                # No hand, Flush and Full House
                elif p1_hand_level in (0, 5, 6):
                    for i in range(len(game_p1[1])):
                        if game_p1[1][i] >= game[1][i]:
                            won += 1
                            break
                        # else:
                            # dict_hands[game_hand_level] += 1
                            # break
                    continue

                # Two Pairs
                elif p1_hand_level == 2:
                    for i in range(len(game_p1[1])):
                        # Check if pairs are higher
                        if game_p1[1][i] > game[1][i]:
                            won += 1
                            break
                        # If not, check for high card
                        elif game_p1[1][i] == game[1][i]:
                            if game_p1[2] >= game[2]:
                                won += 1
                                break
                        # else:
                            # dict_hands[game_hand_level] += 1
                            # break
                    continue

                # One Pair, Three of a Kind and Quads
                elif p1_hand_level in (1, 3, 7):
                        # Check if pair or trips are higher
                    if game_p1[1] > game[1]:
                        won += 1
                        continue

                    # If they are the same, check for the high cards
                    elif game_p1[1] == game[1]:
                        for i in range(len(game_p1[2])):
                            if game_p1[2][i] >= game[2][i]:
                                won += 1
                                break
                            # else:
                                # dict_hands[game_hand_level] += 1
                                # break
                    # else:
                        # dict_hands[game_hand_level] += 1
                    continue

                else:
                    print('Something went wrong with hand, flop, hand_level: ', hand, flop, game_p1)

            # If won is equal to the number of players, then every player was beat
            # and the given hand won the game
        if won == len(players):
            number_of_win += 1
            dict_won_hands[p1_hand_level] += 1
            # Reset everything for next iteration
            won = 0
            games = []

        d.reset_deck()

    won_stats_dict = {'Games Won': round((number_of_win/number_of_sim_to_run)*100, 6),
                      'High Card': round((dict_won_hands[0]/number_of_sim_to_run)*100, 6),
                      'One Pair': round((dict_won_hands[1]/number_of_sim_to_run)*100, 6),
                      'Two Pairs': round((dict_won_hands[2]/number_of_sim_to_run)*100, 6),
                      'Three of a Kind': round((dict_won_hands[3]/number_of_sim_to_run)*100, 6),
                      'Straight': round((dict_won_hands[4]/number_of_sim_to_run)*100, 6),
                      'Flush': round((dict_won_hands[5]/number_of_sim_to_run)*100, 6),
                      'Full House': round((dict_won_hands[6]/number_of_sim_to_run)*100, 6),
                      'Quads': round((dict_won_hands[7]/number_of_sim_to_run)*100, 6),
                      'Straight Flush': round((dict_won_hands[8]/number_of_sim_to_run)*100, 6),
                      'Royal Flush': round((dict_won_hands[9]/number_of_sim_to_run)*100, 6)}

    general_stats_dict = {'High Card': round(((dict_hands[0]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'One Pair': round(((dict_hands[1]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Two Pairs': round(((dict_hands[2]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Three of a Kind': round(((dict_hands[3]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Straight': round(((dict_hands[4]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Flush': round(((dict_hands[5]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Full House': round(((dict_hands[6]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Quads': round(((dict_hands[7]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Straight Flush': round(((dict_hands[8]/total_number_of_players)/(number_of_sim_to_run))*100, 6),
                          'Royal Flush': round(((dict_hands[9]/total_number_of_players)/(number_of_sim_to_run))*100, 6)}

    return won_stats_dict, general_stats_dict
