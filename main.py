import random


ALLOWED_SUITS = {
    "HEARTS": "\u2665",
    "SPADES": "\u2660",
    "CLUBS": "\u2663",
    "DIAMONDS": "\u2666"
}
ALLOWED_VALUES = [7, 8, 9, 10, "J", "Q", "K", "A"]
NUMBER_OF_PILES = 8
PILE_IDS = ["A", "B", "C", "D", "E", "F", "G", "H"]
SAVE_BUTTON = "L"


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return "[" + ALLOWED_SUITS.get(self.suit) + str(self.value) + "]"


class Pile:
    def __init__(self):
        self.cards = []
        self.pile_id = "X"

    def set_pile_id(self, pile_id):
        self.pile_id = pile_id

    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self):
        return self.cards.pop()

    def show_pile(self):
        print(self.cards)

    def shuffle_pile(self):
        random.shuffle(self.cards)

    #def __repr__(self):
     #   return "Pile " + self.pile_id + ": " + str(self.cards)


def setup_game():
    for suit in ALLOWED_SUITS.keys():
        for value in ALLOWED_VALUES:
            card = Card(suit, value)
            DECK.add_card(card)

    DECK.shuffle_pile()

    for i in range(0, NUMBER_OF_PILES):
        pile = Pile()
        pile.set_pile_id(PILE_IDS[i])
        PILES.append(pile)

    pile_counter = 0

    while len(DECK.cards) > 0:
        drawed_card = DECK.draw_card()
        PILES[pile_counter].add_card(drawed_card)
        pile_counter += 1
        if (pile_counter == 8):
            pile_counter = 0


def print_board():
    print("")

    print(" ", end=" ")
    for i in range(0, NUMBER_OF_PILES):
        print(PILES[i].pile_id, end="    ")

    print("")

    for i in range(0, NUMBER_OF_PILES):
        if len(PILES[i].cards) > 0:
            print(PILES[i].cards[-1], end=" ")
        else:
            print("[  ]", end=" ")

    print("")
    print(" ", end=" ")

    for i in range(0, NUMBER_OF_PILES):
        print(len(PILES[i].cards), end="    ")

    print("")


def valid_move_exists():
    unique_cards = []
    for i in range(0, NUMBER_OF_PILES):
        if len(PILES[i].cards) > 0:
            top_card = PILES[i].cards[-1]
            if top_card.value in unique_cards:
                return True
            unique_cards.append(top_card.value)

    return False


def player_has_won():
    for pile in PILES:
        if len(pile.cards) > 0:
            return False
    return True


def play_game():

    should_game_quit = False

    while True:
        if player_has_won():
            print("\nGratulerer! Du vant!")
            break

        if not valid_move_exists():
            print("\nDet finnes ingen lovlige trekk! Du tapte!")
            break

        print("")
        while True:
            pile_1 = input("Velg første bunke(0 = meny): ").upper()
            if pile_1 in PILE_IDS:
                has_remaining_cards = False
                for pile in PILES:
                    if pile.pile_id == pile_1 and len(pile.cards) > 0:
                        has_remaining_cards = True
                        break
                if has_remaining_cards:
                    break
            elif pile_1 == "0":
                meny = """
1 - Start nytt spill 
2 - Lagre spill
3 - Hent lagret spill
4 - Avslutt
                """
                print(meny)
                print("Velg handling(0 for meny)")
                choises = input("Velg> ")
                if choises == "1":
                    print(time.ctime())
                    print("Stokker kortstokken")
                    for elms in elems:
                        print(elms, end="")
                        time.sleep(0.2)
                    print("")
                    PILES.clear()
                    DECK.cards.clear()
                    setup_game()
                    print("Deler ut kort")
                    for elms in elems:
                        print(elms, end="")
                        time.sleep(0.2)
                    print_board()
                    play_game()
                if choises == "2":
                    save_game()
                    print_board()
                    print("")
                elif choises == "3":
                    load_game()
                    print_board()

                elif choises == "4":
                    should_game_quit = True
                    break


            else:
                print("Ugyldig bunke! Velg mellom A-H hvor bunken ikke er tom.")

        if should_game_quit == True:
            break

        while True:
            pile_2 = input("Velg andre bunke: ").upper()
            if pile_2 in PILE_IDS:
                has_remaining_cards = False
                for pile in PILES:
                    if pile.pile_id == pile_2 and len(pile.cards) > 0:
                        has_remaining_cards = True
                        break
                if has_remaining_cards:
                    break
            print("Ugyldig bunke! Velg mellom A-H hvor bunken ikke er tom.")

        card_1 = None
        card_2 = None
        for pile in PILES:
            if pile.pile_id == pile_1:
                card_1 = pile.draw_card()

            if pile.pile_id == pile_2:
                card_2 = pile.draw_card()

        if not card_1.value == card_2.value:
            print("\nDu har trukket to kort som ikke har samme verdi. Prøv igjen!")
            for pile in PILES:
                if pile.pile_id == pile_1:
                    pile.add_card(card_1)

                if pile.pile_id == pile_2:
                    pile.add_card(card_2)

        print_board()


def save_game():
    import time
    with open("save_files.txt", "w", encoding="utf-8") as save_file:
        save = input("Vil du lagre spillet (J/N)? ").upper()

        if save == "J":
            for pile in PILES:
                for card in pile.cards:
                    save_file.write(card.suit)
                    save_file.write(" ")
                    save_file.write(str(card.value))
                    save_file.write(",")
                save_file.write("\n")




def load_game():
    PILES.clear()
    with open("save_files.txt", "r") as save_file:
        piles_as_string = save_file.readlines()

    pile_counter = 0
    for pile_as_string in piles_as_string:
        cards_as_string = pile_as_string.strip().split(",")
        cards_as_string.pop()
        pile = Pile()
        for card_as_string in cards_as_string:
            suit = card_as_string.split(" ")[0]
            value = card_as_string.split(" ")[-1]

            card = Card(suit, value)
            pile.add_card(card)

        pile.set_pile_id(PILE_IDS[pile_counter])
        PILES.append(pile)
        pile_counter += 1


while True:
    import time
    DECK = Pile()
    PILES = []
    elems = "....."
    choises = input("Vil du starte ett spill(J/N)?> ").upper()
    if choises == "J":
        print(time.ctime())
        print("Stokker kortstokken")
        for elms in elems:
            print(elms, end="")
            time.sleep(0.2)
        print("")
        setup_game()
        print("Deler ut kort")
        for elms in elems:
            print(elms, end="")
            time.sleep(0.2)
        print_board()
        play_game()
    print("")
    print("Spill slutt!\n")
    play_again = input("Vil du spille igjen? [J/n]: ").lower()
    if play_again == "n":
        print("Takk for nå!")
        break

