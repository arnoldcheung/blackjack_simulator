import pandas as pd


class Strategy:

    def __init__(self, excel_file, bet=100):
        self.hard = pd.read_excel(excel_file, sheet_name="hard")
        self.soft = pd.read_excel(excel_file, sheet_name="soft")
        self.pairs = pd.read_excel(excel_file, sheet_name="pairs")
        self.hard.columns = self.hard.columns.astype(str)
        self.hard.index = self.hard.index.astype(str)

        self.soft.columns = self.soft.columns.astype(str)
        self.soft.index = self.soft.index.astype(str)

        self.pairs.columns = self.pairs.columns.astype(str)
        self.pairs.index = self.pairs.index.astype(str)

        self.bet = bet

    def decision(self, dealer_hand, player_hand, game):

        if player_hand.pair and game.allow_split:
            input = self.pairs.loc[player_hand.cards[0].rank, dealer_hand.cards[0].rank]

        elif player_hand.soft:
            input = self.soft.loc[str(player_hand.score), dealer_hand.cards[0].rank]

        else:
            input = self.hard.loc[str(player_hand.score), dealer_hand.cards[0].rank]

        if player_hand.split_aces:
            action = "2"

        elif input == "H":
            action = "1"

        elif input == "S":
            action = "2"
        elif input == ("Dh" or "Ds"):
            if game.allow_double_down:
                action = "3"
            elif input == "Dh":
                action = "1"
            else:
                action = "2"
        elif input == "P":
            action = "4"
        else:
            action = "2"
        return action

    def insurance_decision(self, game):
        action = "2"
        return action

    @staticmethod
    def selector():
        while True:
            answer = str(input(""))
            if answer == "1":
                print("Basic strategy\n")
                excel_file = "basic_strategy.xlsx"
                break
            elif answer == "2":
                print("Advanced strategy\n")
                excel_file = None
                break
            elif answer == "3":
                print("Stand all\n")
                excel_file = None
                break
            elif answer == "4":
                print("None\n")
                excel_file = None
                break
            else:
                print("Please enter a valid input")
                continue
        return excel_file


class LinearRamp:

    @staticmethod
    def bet(true_count, min_bet, bet_spread):
        amount = bet_spread * min_bet * true_count
        if amount > 0:
            return amount
        else:
            return min_bet


#class ExpoRamp:

    #@staticmethod
    #def bet(true_count, min_bet, bet_spread):
    #    amount =