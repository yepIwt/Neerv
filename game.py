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
		self.create_deck()
		self.shuffle()

	def create_deck(self):
		for new_suit in range(4):
			for new_value in range(13):
				self._cards.append(Card(new_suit, new_value))

	def shuffle(self):
		random.shuffle(self._cards)

	def take_card(self):
		return self._cards.pop()

class Player:

	def __init__(self, nickname: str, money: int):
		self.nickname = nickname
		self.money = money

	def take_2_cards(self, cards:tuple):
		self._handcards = cards

class Game:

	def __init__(self):
		self.players = []
		self.button_player: int
		self.game_limit = 20 # размер блайнда стола
		self._small_blind_player: int
		self.big_blind_player: int
		self.bets: dict
		self.all_in_bet = 0
		self.player_bet = self.game_limit * 2
		self.deck = Deck()
		self.folded_bets = []
		self.cursor = 0

	def give_func_to_ask(self, argfunc):
		self.get_player_action = argfunc

	def give_func_to_print(self, argfunc):
		self.print_cout = argfunc

	def give_func_to_bet(self, argfunc):
		self.ask_new_bet = argfunc

	def player_next_to(self, next_to: int) -> int:
		return (next_to + 1) % len(self.players)

	def add_player(self, nick: str, money: int) -> None:
		self.players.append(Player(nick,money))

	def choose_dealer(self) -> int:
		self.button_player = random.randrange(len(self.players))
		return self.button_player

	def choose_blinds_players(self) -> None:
		self.small_blind_player = self.player_next_to(self.button_player)
		self.big_blind_player = self.player_next_to(self.small_blind_player)
		self.cursor = self.player_next_to(self.big_blind_player)

	def bets_are_equal(self) -> bool:
		setted_bets = set(self.bets)
		if len(setted_bets) == 1:
			return True
		return False

	def all_in_rule_completed(self) -> bool:
		#debug
		print("ALL IN COMPLETED", self.bets)
		for bet_i in range(self.bets):
			if self.bets[bet_i] == self.all_in_bet:
				pass
			elif self.players[bet_i].money == 0:
				pass
			else:
				return False
		return True

	def make_zero_bets(self) -> None:
		self.bets = [0 for x in range(len(self.players))]

	def bet_small_blind(self) -> None:
		self.players[self.small_blind_player].money -= self.game_limit
		self.bets[self.small_blind_player] += self.game_limit
		return self.players[self.small_blind_player].nickname
	
	def bet_big_blind(self) -> None:
		self.players[self.big_blind_player].money -= self.game_limit * 2
		self.bets[self.big_blind_player] += self.game_limit * 2
		return self.players[self.big_blind_player].nickname

	def deal_card(self) -> None:
		for player in self.players:
			player.take_2_cards(
				(self.deck.take_card(), self.deck.take_card())	
			)

	def calc_pot(self) -> int:
		pot = 0
		for bet in self.bets:
			pot += bet
		for fold_bet in self.folded_bets:
			pot += fold_bet[1]
		return pot

	def player_stack_info(self):
		string = f"In {self.players[self.cursor].nickname}'s stack: {self.players[self.cursor].money}"
		return string

	async def player_bets(self):
		prev_bet = self.player_bet
		await self.print_cout(f"Your bank is {self.players[self.cursor].money}$. Type /bet INT to bet")
		self.player_bet = await self.ask_new_bet()
		if self.player_bet == self.players[self.cursor].money:
			await self.print_cout(f"{self.players[self.cursor].nickname} all-ined...")
			self.all_in()
		elif self.player_bet == prev_bet:
			await self.print_cout(f"{self.players[self.cursor].nickname} calls...")
		else:
			await self.print_cout(f"{self.players[self.cursor].nickname} bets {self.player_bet}...")
		self.bet(self.player_bet)
		self.cursor = self.player_next_to(self.cursor)

	async def player_calls(self):
		while self.player_bet > self.players[self.cursor].money:
			await self.print_cout("You can't call. You don't have enough money!")
			await self.print_cout(self.player_stack_info())
			await self.print_cout("Type /action INT (only fold or allin)")
			self.player_action = self.get_player_action()
			await self.handle_player_action()

	def bet(self, howmch: int):
		self.bets[self.cursor] += howmch
		self.players[self.cursor].money -= howmch

	def call(self):
		self.bet(self.player_bet)

	def fold(self):
		self.folded_bets.append(
			(self.players[self.cursor].nickname,self.bets[self.cursor])
		)
		self.players.pop(self.cursor)
		self.bets.pop(self.cursor)
		if self.cursor >= len(self.players): self.cursor = 0

	def all_in(self):
		self.bets[self.cursor] += self.players[self.cursor].money
		self.players[self.cursor].money = 0
		self.all_in_bet = self.bets[self.cursor]

	async def handle_player_action(self):
		if self.player_action == 1:
			await self.print_cout(f"{self.players[self.cursor].nickname} folds...")
			self.fold()
		elif self.player_action == 2:
			await self.player_bets()
		elif self.player_action == 3:
			await self.player_calls()
		elif self.player_action == 4:
			await self.print_cout(f"{self.players[self.cursor].nickname} all-ined...")
			self.all_in()

	async def makeBets(self):
		while self.bets_are_equal() != True and not self.all_in_bet:
			await self.print_cout(f"LastBet: {self.player_bet}$")
			await self.print_cout(f"Pot: {self.calc_pot()}$")
			await self.print_cout("Type /action INT to action. (1) fold (2) bet (3) call (4) all-in")
			self.player_action = await self.get_player_action()
			await self.handle_player_action()
		await self.print_cout("Торги окончены")