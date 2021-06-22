from thpoker.core import Cards, Combo, Hand, Table
import random

CARDSUITS = ["Черви","Вини","Буби","Крести"]
CARDVALUES = ["2","3","4","5","6","7","8","9","10","Валет","Дама","Король","Туз"]
SHORTSUI = ['h','s','d','c']
SHORTVAL = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

# clubs - крести
# diamonds - буби
# hearts - черви
# spades - вини

class MyCard:

    def __init__(self, suit: int, val: int) -> None:
        self.value = val
        self.suit = suit
    
    def to_russian(self):
        global CARDSUITS, CARDVALUES
        return CARDVALUES[self.value] + " " + CARDSUITS[self.suit]
    
    def __str__(self):
        global SHORTSUI, SHORTVAL
        return SHORTVAL[self.value] + SHORTSUI[self.suit]


class Deck:

    def __init__(self):
        self.cards = []
        self.old_generate_deck()
        self.shuffle_cards()
    
    def generate_deck(self):
        for card_suit in ['h','s','c','d']:
            for card_value in ['2','3','4','5','6','7','8','9','T','J','Q','K','A']:
                card = card_value + card_suit
                self.cards.append(card)
    
    def old_generate_deck(self):
        for new_suit in range(4):
            for new_value in range(13):
                self.cards.append(MyCard(new_suit, new_value))
    
    def shuffle_cards(self):
        random.shuffle(self.cards)
    
    def take_hand_cards(self):
        return self.cards.pop(), self.cards.pop()
    
    def take_one(self):
        return self.cards.pop()

class OnTable:

    def __init__(self):
        self.cards = []
    
    def place_one_card(self, card: MyCard):
        self.cards.append(card)
    
    def currround(self):
        if len(self.cards) - 2 < 0:
            return 0
        else:
            return len(self.cards) - 2
    
    def to_russian(self):
        russian_cards = []
        for card_class in self.cards:
            russian_cards.append(card_class.to_russian())
        return russian_cards
    
    def __str__(self):
        string = ""
        for card in self.cards:
            string += str(card) + "/"
        string = string[:-1]
        return string

from game import Player
def pseudo_register(names):
    ps = []
    for name in names:
        p = Player(name,1000)
        ps.append(p)
    return ps

def random_gets_cards(players, that_deck):
    for pl in players:
        pl.take_2_cards(that_deck.take_hand_cards())

def best_combo(player_combinations):
    best = player_combinations.pop()
    for comb in player_combinations:
        if best['combo'] < comb['combo']:
            best = comb
    return best

def check_combo(hand_cards, table):
    string_hand_cards = str(hand_cards[0]) + '/' + str(hand_cards[1])
    string_table_cards = str(table)
    combo = Combo(hand=Hand(string_hand_cards), table=Table(string_table_cards))
    return combo

if __name__ == '__main__':
    table_cards = OnTable()
    mydeck = Deck()
    names = ['tim','nick','uli','max','dim']
    players = pseudo_register(names)
    random_gets_cards(players,mydeck)
    #flop
    [table_cards.place_one_card(mydeck.take_one()) for _ in range(3)]
    #turn
    table_cards.place_one_card(mydeck.take_one())
    #river
    table_cards.place_one_card(mydeck.take_one())
    print("На столе лежали карты")
    print(table_cards.to_russian())
    print("#############################################")

    player_combinations = []
    for pl in players:
        print(f"Игрок {pl.nickname}: {pl._handcards[0].to_russian()} | {pl._handcards[1].to_russian()}")
        combo = check_combo(pl._handcards, table_cards)
        n = {
            'name': pl.nickname,
            'combo': combo
        }
        player_combinations.append(n)
        print(f"===={combo}")

    best_combination = best_combo(player_combinations)
    print("=============================================")
    print(f"Победил игрок {best_combination['name']}: {best_combination['combo']}")