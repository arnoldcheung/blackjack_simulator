from random import shuffle
import deck
import bj_rules
import strategies
import counting

scores = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}


class Hand:

    # Constructor
    def __init__(self, init_card=None, bet=0, split=False):

        # All the different states of a hand
        if init_card:
            self.cards = [init_card]
        else:
            self.cards = []
        self.bet = bet
        self.num_ace = 0
        self.score = 0
        self.soft = False
        self.bust = False
        self.blackjack = False
        self.twenty_one = False
        self.pair = False
        self.split_aces = False
        self.dd = False
        self.split = split

    # Returns the hand index of a player
    def get_name(self, player):

        hand_index = str(player.hands.index(self) + 1)
        return "Hand " + hand_index

    # Returns the score of the hand, changes the state depending on the score
    def get_score(self):

        score = 0
        # Whether the hand is soft or not can differ for every check
        self.soft = False
        
        for card in self.cards:
            score += scores[card.rank]
        
        # If Ace is treated as 11 instead of 1, the hand is soft    
        if score <= 11 and self.num_ace > 0:
            score += 10
            self.soft = True
        
        # The difference between blackjack and a normal 21: blackjack can only happen for an initial hand    
        if score > 21:
            self.bust = True
            
        if not self.blackjack and score == 21:
            self.twenty_one = True
            
        return score

    # Prints the status of an individual hand of a player
    def hand_status(self, player):
        
        if player.id == "dealer":
            print(self.get_name(player))
        else:
            print("{}   Bet: {}".format(self.get_name(player), self.bet))
            
        for card in self.cards:
            print(card)
            
        print("Total score: {}".format(self.score))

        if player.count_strategy:
            print("{} count: {}   True count: {}".format(player.count_strategy.name,
                                                         player.card_count,
                                                         player.true_count))
            
        if self.bust:
            print("--Bust--\n")
            
        if self.blackjack:
            print("--Blackjack--\n")
            
        print("----------------------------")


class Player:
    
    # Constructor
    def __init__(self, deposit, id, num_deck, strategy=None, count_strategy=None, bet_strategy=None):
        
        self.id = id
        self.balance = deposit
        self.join = True
        self.hands = []
        self.insurance = 0
        
        # Auto-play
        self.strategy = strategy

        # Card counting
        self.count_strategy = count_strategy
        self.card_count = 0
        self.true_count = 0
        self.true_count_list = []

        # Bet Strategy
        self.bet_strategy = bet_strategy
        
        # Statistics
        self.total_bet = 0
        self.dd_count = 0
        self.dd_win = 0
        self.split_count = 0
        self.split_win = 0
        self.win_count = 0
        self.lose_count = 0
        self.push_count = 0
        
        # Dealer doesn't go through place_bet(), hand is initialised here
        if self.id == "dealer":
            self.hands.append(Hand())

    # Re-initialises the player after every round
    def reset(self):
        
        self.join = True
        self.hands = []
        self.insurance = 0
        
        # Dealer doesn't go through place_bet(), hand is initialised here 
        if self.id == "dealer":
            self.hands.append(Hand())

    # Returns the name of the player
    def __str__(self):
        
        if self.id == "dealer":
            return "Dealer"
        else:
            return "Player " + str(self.id)

    # Gets called in the main game, if the player wishes to do an action but fund is insufficient
    def ask_top_up(self):
        
        while True:
            
            answer = str(input("Would you like to top up? (1)Yes (2)No\n"))
            
            if answer == "1":
                while True:
                    
                    try:
                        amount = float(input("Please enter the amount to top up\n"))
                    except ValueError:
                        print("Invalid amount\n")
                        continue
                        
                    if amount < 0:
                        print("Invalid amount\n")
                        continue
                        
                    elif amount == 0:
                        print("No top up\n")
                        break
                        
                    else:
                        self.balance += amount
                        break
                        
                break
                
            elif answer == "2":
                print("No top up")
                break
                
            else:
                print("Please enter a valid input")
                continue

    # Prints the full player's status
    def player_status(self):
        
        print("----------------------------")
        if self.id == "dealer":
            print(self)
        else:
            print("{}   Balance: {}   Total bet: {}".format(self, self.balance, self.total_bet))
        
        # Prints hand status for every hand    
        for hand in self.hands:
            hand.hand_status(self)
            
        print("----------------------------\n")


class Game:
    
    # Constructor
    def __init__(self, num_players,
                 init_balance=10000000,
                 min_bet=1,
                 used_hands=3,
                 always_shuffle=False,
                 rules=bj_rules.VegasRules,
                 ):
        print("""                                                         
          ____    _                  _        _                  _        
         | __ )  | |   __ _    ___  | | __   (_)   __ _    ___  | | __    
         |  _ \  | |  / _` |  / __| | |/ /   | |  / _` |  / __| | |/ /    
         | |_) | | | | (_| | | (__  |   <    | | | (_| | | (__  |   <     
         |____/  |_|  \__,_|  \___| |_|\_\  _/ |  \__,_|  \___| |_|\_|    
                                           |__/                       """)

        # Sets and prints rules
        self.rules = rules
        self.rules.print_rules()
        
        self.num_players = num_players
        
        # Checks if the game allow certain actions based on current rules
        self.allow_hit = False
        self.allow_double_down = False
        self.allow_split = False
        
        # Counter
        self.rounds = 0

        # Max player handler
        if num_players > 7:
            print("\nThe maximum number of players is 7\n")
            self.num_players = 7
        
        # Sets game parameters
        self.init_balance = init_balance
        self.min_bet = min_bet
        # Initialises shoe
        self.shoe = deck.Deck(self.rules.num_deck).deck
        self.num_deck = self.rules.num_deck
        self.remaining_deck = self.num_deck
        # Empty used_deck
        self.used_deck = []

        # Add players to the game, Player 0 (self.players[0] is the dealer)
        for i in range(num_players + 1):
            if i == 0:
                self.players = [Player(init_balance, "dealer", self.num_deck)]
            else:
                self.players.append(Player(init_balance, i, self.num_deck))

        # Continuous shuffler
        self.used_hands = used_hands
        self.always_shuffle = always_shuffle
        self.hand_counter = 0

        # Ask what strategy does the player want to use (auto)
        for player in self.players[1:]:
            print("{}: Use auto strategy?".format(player))
            print("(1) Basic strategy")
            print("(2) Advanced strategy")
            print("(3) Stand all")
            print("(4) None")

            # Returns none if player chooses to play manually
            selection = strategies.Strategy.selector()

            if selection:
                player.strategy = strategies.Strategy(selection)

            print("{}: Use card counter?".format(player))
            print("(1) Hi-Lo")
            print("(2) Hi-Opt I")
            print("(3) Hi-Opt II")
            print("(4) KO")
            print("(5) Omega II")
            print("(6) Halves")
            print("(7) Zen count")
            print("(8) None")

            selection = counting.selector()

            if selection:
                player.count_strategy = selection
                player.true_count_list = [0] * ((2 * player.count_strategy.max_count_per_deck * self.num_deck) + 1)

            if player.count_strategy:
                while True:
                    answer = str(input("{}: Use auto-bet strategy? (1)Yes (2)No\n".format(player)))

                    if answer == "1":
                        player.bet_strategy = strategies.LinearRamp
                        print("Linear ramp")
                        break

                    elif answer == "2":
                        player.bet_strategy = None
                        print("None")
                        break

                    else:
                        print("Please enter a valid input")
                        continue

    # Main function
    def start(self, epoch=10, rounds=30000):

        for j in range(epoch):
            print("Epoch: {}".format(j))

            while any(x.balance > 1000 for x in self.players[1:]) and self.rounds <= rounds:
                self.place_bets()
                self.init_deal()
                if sum(player.join for player in self.players[1:]) >= 1:
                    self.player_round()
                self.dealer_round(self.players[0])
                self.payout(self.players[0].hands[0])

                # Reshuffle deck when used deck starts to pile up
                self.reshuffle()
                self.rounds += 1
            self.rounds = 0

        for player in self.players[1:]:
            hands_played = player.win_count + player.lose_count + player.push_count
            dd_percentage = 100 * player.dd_count/hands_played
            dd_win_percentage = player.dd_win/player.dd_count
            win_percentage = 100 * player.win_count/hands_played
            lose_percentage = 100 * player.lose_count/hands_played
            push_percentage = 100 * player.push_count/hands_played
            gain = player.balance - self.init_balance
            edge = 100 * gain/player.total_bet
            balance_percentage = 100 * gain/self.init_balance
            print("\n\n")
            print("{}   bet per hand: {}".format(player, player.strategy.bet))
            print("Hands played: {}".format(hands_played))
            print("Gain: {}".format(gain))
            print("Total bet: {}\n".format(player.total_bet))
            print("Wins: {}".format(player.win_count))
            print("Loses: {}".format(player.lose_count))
            print("Pushes: {}\n".format(player.push_count))
            print("Balance percentage: {}%".format(balance_percentage))
            print("Win percentage: {}%".format(win_percentage))
            print("Lose percentage: {}%".format(lose_percentage))
            print("Push percentage: {}%".format(push_percentage))
            print("Edge: {}%\n".format(edge))
            print("Double down percentage: {}%".format(dd_percentage))
            print("Double down win percentage: {}%\n".format(dd_win_percentage))

            if player.count_strategy:
                print("True counts: {}".format(player.true_count_list))

    def place_bets(self):

        # Every player except dealer
        for player in self.players[1:]:
            while True:

                if player.strategy:
                    amount = player.strategy.bet

                    if player.bet_strategy:
                        amount = player.bet_strategy.bet(player.true_count, self.min_bet, 50)

                else:

                    print("{}   Balance: {}   Total bet: {}".format(player, player.balance, player.total_bet))

                    if player.count_strategy:
                        print("{} count: {}   True count: {}".format(player.count_strategy.name,
                                                                     player.card_count,
                                                                     player.true_count))

                    if player.bet_strategy:
                        amount = player.bet_strategy.bet(player.true_count, self.min_bet, 1)

                    else:
                        try:
                            amount = float(input("Please place your bets \n"))

                        except ValueError:
                            print("Invalid bet\n")
                            continue

                if amount < 0:
                    print("Invalid bet\n")
                    continue

                elif amount == 0:
                    print("No bet\n")
                    player.join = False
                    break

                elif amount < self.min_bet:
                    print("The minimum bet is {}\n".format(self.min_bet))
                    continue

                elif player.balance >= amount:
                    # If player placed a bet, hand gets initialised here
                    player.hands.append(Hand())
                    # Transfers value from balance to bet
                    player.balance -= amount
                    player.hands[0].bet = amount
                    player.total_bet += amount
                    player.join = True

                    if player.strategy is None:
                        print("{}   Balance: {}   Total bet: {}".format(player, player.balance, player.total_bet))
                        print("{}   Bet: {}\n".format(player.hands[0].get_name(player), amount))
                    break

                else:
                    print("Insufficient funds\n")
                    player.ask_top_up()
                    continue

    # Deals 2 card to all players who joined the game by placing a bet > 0
    def init_deal(self):

        for player in self.players:
            if player.join:
                for hand in player.hands:
                    if player.id == "dealer":
                        # Face card
                        self.deal(hand)
                        # Hole card
                        self.deal(hand, shown=False)

                    else:
                        for i in range(2):  # Two cards
                            self.deal(hand)

                    hand.score = hand.get_score()

                    if hand.score == 21:
                        hand.blackjack = True

                    if self.rules.check_pair(hand):
                        hand.pair = True

    # Starts by printing dealer's face card
    def start_round(self, player):

        if player.count_strategy:
            player.true_count_list[player.true_count + (player.count_strategy.max_count_per_deck * self.num_deck)] += 1
            
        if player.strategy is None:
            print("Dealer")
            # self.players[0].hands[0].cards[0] is the dealer's face card
            print("{}\n".format(self.players[0].hands[0].cards[0]))
            print("{}   Balance: {}".format(player, player.balance))
            print("----------------------------")
        self.insurance(player, player.hands[0])

    # Deals a card, if ace, adds 1 to ace counter
    def deal(self, hand, shown=True):

        # new_card = deck.Card("Spades", "6")  # To deal desired cards for debugging
        new_card = self.shoe.pop()  # Comment this line out when using above line

        if new_card.rank == "A":
            hand.num_ace += 1

        hand.cards.append(new_card)

        for player in self.players[1:]:
            if player.count_strategy and shown:
                player.card_count += player.count_strategy.count(new_card)
                player.true_count = round(player.card_count / self.remaining_deck)

    # The insurance side bet
    def insurance(self, player, hand):

        # Only available when dealer's face card is ace
        if self.players[0].hands[0].cards[0].rank == "A" and player.insurance == 0:
            if player.strategy:

                # If auto-play, strategy decides to buy insurance or not
                answer = player.strategy.insurance_decision(self)

            else:
                answer = str(input("Would you like to place an insurance bet? (1)Yes (2)No\n"))

            while True:
                if answer == "1":

                    # Insurance bet is half the original bet
                    if player.balance >= 0.5 * hand.bet:
                        player.balance -= 0.5 * hand.bet
                        player.insurance += 0.5 * hand.bet
                        if player.strategy is None:
                            print("Insurance placed\n")
                        break

                    else:
                        print("Insufficient funds")
                        print("------------------")
                        player.ask_top_up()
                        print("Balance: {}".format(player.balance))
                        continue

                elif answer == "2":
                    if player.strategy is None:
                        print("No insurance bet\n")
                    break

                else:
                    print("Please enter a valid input")
                    continue

    # Main action: hit
    def hit(self, hand, player):

        # Prints error if hit is not allowed
        if player.strategy is None:
            print(self.rules.hit_rules(self, hand))

        if self.allow_hit:

            self.deal(hand)
            hand.score = hand.get_score()
            if player.strategy is None:
                print("--Hit--")
                hand.hand_status(player)

    # Main action: stand
    def stand(self, hand, player):

        hand.score = hand.get_score()
        if player.strategy is None:
            print("--Stand--")
            hand.hand_status(player)

    # Main action: double down
    def double_down(self, hand, player):

        # Prints error if double down is not allowed
        if player.strategy is None:
            print(self.rules.double_down_rules(self, hand))

        if self.allow_double_down:
            if player.balance >= hand.bet:

                player.balance -= hand.bet
                player.total_bet += hand.bet
                hand.bet += hand.bet
                self.deal(hand)
                hand.score = hand.get_score()
                hand.dd = True
                player.dd_count += 1

                if player.strategy is None:
                    print("--Double down--")
                    hand.hand_status(player)

                return True

            else:
                print("Insufficient funds")
                print("------------------")
                player.ask_top_up()
                print("Balance: {}".format(player.balance))
                return False

    # Main action: split
    def split(self, hand, player):

        # Prints error if split is not allowed
        if player.strategy is None:
            print(self.rules.split_rules(self, player, hand))

        if self.allow_split:
            if player.balance >= hand.bet:

                player.balance -= hand.bet
                player.total_bet += hand.bet

                # Creates a new hand, and add one of the cards to the new hand, mark as 'split'
                player.hands.append(Hand(hand.cards.pop(), hand.bet, split=True))

                # Marks current hand as 'split'
                hand.split = True

                for split_hand in player.hands:
                    if split_hand.split:

                        # Split aces functions differently
                        if split_hand.cards[0].rank == "A":
                            split_hand.split_aces = True
                            split_hand.num_ace += 1

                        self.deal(split_hand)

                        # Checks if after deal is a new pair
                        if self.rules.check_pair(split_hand):
                            split_hand.pair = True

                        else:
                            split_hand.pair = False

                        split_hand.score = split_hand.get_score()
                        split_hand.split = False

                if player.strategy is None:
                    print("--Split--")
                    hand.hand_status(player)

            else:
                print("Insufficient funds")
                print("------------------")
                player.ask_top_up()
                print("Balance: {}".format(player.balance))

    # Prompts player with options
    def player_round(self):

        # For every player that isn't the dealer
        for player in self.players[1:]:
            self.start_round(player)

            for hand in player.hands:

                if player.strategy is None:
                    hand.hand_status(player)

                while not hand.bust and not hand.blackjack and not hand.twenty_one:

                    # Checks if the actions are allowed
                    self.rules.hit_rules(self, hand)
                    self.rules.double_down_rules(self, hand)
                    self.rules.split_rules(self, player, hand)

                    if player.strategy:
                        action = player.strategy.decision(self.players[0].hands[0], hand, self)

                    else:
                        action = str(input("(1)Hit (2)Stand (3)Double Down (4)Split\n"))

                    if action == "1":
                        self.hit(hand, player)

                    elif action == "2":
                        self.stand(hand, player)
                        break

                    elif action == "3":
                        if self.double_down(hand, player):
                            break

                        else:
                            continue

                    elif action == "4":
                        self.split(hand, player)
                        continue

                    else:
                        print("Please enter a valid input")
                        continue

            if player.strategy is None:
                player.player_status()


    # Auto dealer, based on dealer rules
    def dealer_round(self, dealer):

        for player in self.players[1:]:
            if player.count_strategy:
                player.card_count += player.count_strategy.count(self.players[0].hands[0].cards[1])
                player.true_count = round(player.card_count / self.remaining_deck)
        self.rules.dealer_logic(self, dealer)
        if any(player.strategy is None for player in self.players[1:]):
            dealer.player_status()

    # Pays out depending on result states
    def payout(self, dealer):

        for player in self.players[1:]:

            if player.strategy is None:
                print("{}   Balance: {}".format(player, player.balance))

            for hand in player.hands:

                # Player bust
                if hand.bust:
                    hand.bet = 0
                    player.lose_count += 1

                    if player.strategy is None:
                        print(hand.get_name(player))
                        print("Bust\n")

                # Player win
                elif dealer.bust or hand.score > dealer.score or (hand.blackjack and not dealer.blackjack):
                    if hand.blackjack:
                        value = 2.5 * hand.bet
                        player.balance += value

                    else:
                        value = 2 * hand.bet
                        player.balance += value

                    if not hand.bust:
                        player.win_count += 1
                        if hand.dd:
                            player.dd_win += 1

                        if player.strategy is None:
                            print(hand.get_name(player))
                            print("Win: {}\n".format(value))

                # Push
                elif hand.score == dealer.score or (hand.blackjack and dealer.blackjack):

                    # Bet returns to player
                    player.balance += hand.bet
                    if not hand.bust:
                        player.push_count += 1

                        if player.strategy is None:
                            print(hand.get_name(player))
                            print("Push\n")

                # Dealer win
                else:
                    if not hand.bust:
                        player.lose_count += 1

                        if player.strategy is None:
                            print(hand.get_name(player))
                            print("Lose\n")

                # Send used cards to used pile
                self.used_deck.extend(hand.cards)
                self.remaining_deck = (len(self.shoe) // 52) + 1

            # Pays for insurance if the player has placed a bet
            if player.insurance > 0 and dealer.blackjack:
                value = 3 * player.insurance
                player.balance += value
                player.insurance = 0

                if player.strategy is None:
                    print("Insurance win: {}\n".format(value))

            # Resets player
            player.reset()

        # Resets dealer after all pay outs
        self.used_deck.extend(self.players[0].hands[0].cards)
        self.players[0].reset()

        # Number of hands played before reshuffling
        self.hand_counter += 1

    # Re-shuffler, configurable
    def reshuffle(self):
        if (self.hand_counter == self.used_hands) or (len(self.shoe) < 5 * len(self.players)) or self.always_shuffle:
            self.shoe.extend(self.used_deck)
            self.used_deck = []
            shuffle(self.shoe)
            self.hand_counter = 0
            for player in self.players:
                player.card_count = 0
                player.true_count = 0
            self.remaining_deck = self.num_deck
            if any(player.strategy is None for player in self.players[1:]):
                print("-------Deck reshuffled------\n")
















































