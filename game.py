"""
	This is base gaming core.
	Neerv, 2021. yepIwt
"""
import random

class Card:

	def __init__(self, val: int, suit: int) -> None:
		self.value = val
		self.suit = suit

class Deck:

	cardsuits = ["Черви","Вини","Буби","Крести"]
	cardvalues = ["2","3","4","5","6","7","8","9","10","Валет","Дама","Король","Туз"]

	def __init__(self):
		self._cards = []
		create_deck()
		shuffle()

	def create_deck(self):
		for new_suit in range(4):
			for new_value in range(13):
				self._cards.append(Card(new_suit, new_value))

	def shuffle(self):
		random.shuffle(self._cards)

	def take_card(self):
		return self._cards.pop()