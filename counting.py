class HiLo:
    count_table = {"A": -1,
                   "2": 1, "3": 1, "4": 1, "5": 1, "6": 1,
                   "7": 0, "8": 0, "9": 0,
                   "10": -1, "J": -1, "Q": -1, "K": -1}
    name = "Hi-Lo"
    max_count_per_deck = 5

    @staticmethod
    def count(card):
        count = HiLo.count_table[card.rank]
        return count


class HiOptI:
    count_table = {"A": 0,
                   "2": 0, "3": 1, "4": 1, "5": 1, "6": 1,
                   "7": 0, "8": 0, "9": 0,
                   "10": -1, "J": -1, "Q": -1, "K": -1}
    name = "Hi-Opt I"
    max_count_per_deck = 4

    @staticmethod
    def count(card):
        count = HiOptI.count_table[card.rank]
        return count


class HiOptII:
    count_table = {"A": 0,
                   "2": 1, "3": 1, "4": 2, "5": 2, "6": 1,
                   "7": 1, "8": 0, "9": 0,
                   "10": -2, "J": -2, "Q": -2, "K": -2}
    name = "Hi-Opt II"
    max_count_per_deck = 8

    @staticmethod
    def count(card):
        count = HiOptI.count_table[card.rank]
        return count


class KO:
    count_table = {"A": -1,
                   "2": 1, "3": 1, "4": 1, "5": 1, "6": 1,
                   "7": 1, "8": 0, "9": 0,
                   "10": -1, "J": -1, "Q": -1, "K": -1}
    name = "KO"
    max_count_per_deck = 6

    @staticmethod
    def count(card):
        count = HiOptI.count_table[card.rank]
        return count


class OmegaII:
    count_table = {"A": 0,
                   "2": 1, "3": 1, "4": 2, "5": 2, "6": 2,
                   "7": 1, "8": 0, "9": -1,
                   "10": -2, "J": -2, "Q": -2, "K": -2}
    name = "OmegaII"
    max_count_per_deck = 9

    @staticmethod
    def count(card):
        count = OmegaII.count_table[card.rank]
        return count


class Halves:
    count_table = {"A": -1,
                   "2": 0.5, "3": 1, "4": 1, "5": 1.5, "6": 1,
                   "7": 0.5, "8": 0, "9": -0.5,
                   "10": -1, "J": -1, "Q": -1, "K": -1}
    name = "Halves"
    max_count_per_deck = 6

    @staticmethod
    def count(card):
        count = Halves.count_table[card.rank]
        return count


class ZenCount:
    count_table = {"A": -1,
                   "2": 1, "3": 1, "4": 2, "5": 2, "6": 2,
                   "7": 1, "8": 0, "9": 0,
                   "10": -2, "J": -2, "Q": -2, "K": -2}
    name = "ZenCount"
    max_count_per_deck = 9

    @staticmethod
    def count(card):
        count = ZenCount.count_table[card.rank]
        return count


def selector():
    while True:
        answer = str(input(""))
        if answer == "1":
            print("Hi-Lo\n")
            selection = HiLo
            break

        elif answer == "2":
            print("Hi-Opt I\n")
            selection = HiOptI
            break

        elif answer == "3":
            print("Hi-opt II\n")
            selection = HiOptII
            break

        elif answer == "4":
            print("KO\n")
            selection = KO
            break

        elif answer == "5":
            print("Omega II\n")
            selection = OmegaII
            break

        elif answer == "6":
            print("Halves\n")
            selection = Halves
            break

        elif answer == "7":
            print("Zen Count\n")
            selection = ZenCount
            break

        elif answer == "8":
            print("None\n")
            selection = None
            break

        else:
            print("Please enter a valid input")
            continue

    return selection
