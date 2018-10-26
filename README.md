# blackjack_simulator


# -----------instructions-----------
# Game(self, num_players,
# init_balance=10000000,
# min_bet=100,
# used_hands=3,                       <-- number of rounds before reshuffling
# rules=bj_rules.VegasRules           <-- blackjack rules, see bj_rules.py (other: EuropeanRules, CustomRules)
# always_shuffle=False                <-- if True: re-shuffle deck after every round, regardless of used_hands
# )
#
# start(epoch=10, rounds=10000)       <-- only useful for automatic play, total rounds played = epoch * rounds
#
#
#
#
# Run this file
#
#
# Use auto strategy?
# (1) Basic strategy                  <-- only strategy implemented for now, basic_strategy.xlsx
# (2) Advanced strategy               <-- Choose this will default to None
# (3) Stand all                       <-- Choose this will default to None
# (4) None                            <-- No strategy, player decision (manual game)
#
# ---------------------------------------------------------------------------------------------------------------------
# Blackjack
#
# Objective:
# Get as close to 21 without going over
#
# Scores of card:
# Score = Rank of card
# except: J Q K --> count as 10
#         A --> count as 1 or 11, highest without busting
#
# e.g. [A][3] --> score: 4 or 14 (soft)
#      [A][3][9] --> score: 13 (hard)
#      [2][2] --> score: 4 (hard)
#      [10][J] --> score: 20 (hard)
#      [A][A] --> score: 2 or 12 (soft)
#      [A][A][10] --> score: 12 (hard)
#
# ** Soft hand: 2 possible scores **
# ** Hard hand: Only 1 possible score **
# ** The suit of the card has no meaning in Blackjack **
#
# Options:
# Hit - get a card
# Stand - Keep current card, next player
# Double down - double your bet on that hand, gets one extra card, not allowed anymore cards
# Split - Split into two separate hands, only available when dealt a pair
#
# Insurance - Only available when dealer has Ace card, place insurance bet equals to half your original bet if player
#             chooses to do so, pays 2 to 1 if dealer second card is a 10 (10, J, Q, K) making a Blackjack
#
# Blackjack: An Ace and a 10 card (10, J, Q, K) making 21 - Pays 3 to 2 (rather than 1 to 1) if player has a Blackjack
#
# ** 21 is not equal to a Blackjack**
# ** If player gets a A + 10 after a split, that doesn't count as Blackjack, only a 21
#
# ---------------------------------------------------------------------------------------------------------------------
#
#
