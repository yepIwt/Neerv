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

	def curr_player(self):
		return self.players[self.cursor]

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

	def all_in_completed(self) -> bool:
		#print("========ALL IN COMPLETED:", self.bets)
		for bet_i in range(len(self.bets)):
			if self.bets[bet_i] == self.all_in_bet:
				continue
			else:
				if self.players[bet_i].money == 0:
					continue
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

	def avaliable_player_actions(self):
		if self.all_in_bet:
			if self.all_in_bet - self.bets[self.cursor] > self.players[self.cursor].money:
				return [1,4]
			return [1,3]
		elif self.players[self.cursor].money < self.player_bet:
			return [1,4]
		else:
			return [1,2,3,4]

	async def player_bets(self):
		prev_bet = self.player_bet
		await self.print_cout(f"Твой стек: {self.curr_player().money}$. Наберите /bet INT для того чтобы поставить")
		self.player_bet = await self.ask_new_bet()
		if self.player_bet == self.curr_player().money:
			await self.all_in()
		else:
			if self.player_bet == prev_bet:
				await self.print_cout(f"{self.curr_player().nickname} коллирует...")
			else:
				await self.print_cout(f"{self.curr_player().nickname} ставит {self.player_bet}...")
			self.bet(self.player_bet)
			self.cursor = self.player_next_to(self.cursor)

	def bet(self, howmch: int):
		self.bets[self.cursor] += howmch
		self.players[self.cursor].money -= howmch

	async def call(self):
		offset = self.all_in_bet or self.player_bet
		self.players[self.cursor].money -= offset - self.bets[self.cursor]
		self.bets[self.cursor] += offset - self.bets[self.cursor]
		await self.print_cout(f"{self.curr_player().nickname} calls...")
		self.cursor = self.player_next_to(self.cursor)

	async def fold(self):
		self.folded_bets.append(
			(self.curr_player().nickname, self.bets[self.cursor])
		)
		await self.print_cout(f"{self.curr_player().nickname} фолдит...")
		self.players.pop(self.cursor)
		self.bets.pop(self.cursor)
		if self.cursor >= len(self.players): self.cursor = 0

	async def all_in(self):
		self.bets[self.cursor] += self.curr_player().money
		if not self.all_in_bet:
			self.all_in_bet = self.curr_player().money
		self.players[self.cursor].money = 0
		await self.print_cout(f"{self.curr_player().nickname} идёт олл-ин...")
		self.cursor = self.player_next_to(self.cursor)

	async def handle_player_action(self, act: int):
		if act == 1:
			#await self.print_cout(f"{self.players[self.cursor].nickname} folds...")
			await self.fold()
		elif act == 2:
			await self.player_bets()
		elif act == 3:
			await self.call()
		elif act == 4:
			await self.all_in()

	async def makeBets(self):
		while self.bets_are_equal() != True and not self.all_in_bet:
			await self.print_cout(f"Последняя ставка: {self.player_bet}$")
			#await self.print_cout(f"Pot: {self.calc_pot()}$")
			await self.print_cout(f"Текущий игрок - {self.curr_player().nickname}\nТвой стек: {self.curr_player().money}")
			await self.print_cout(f"Используй команду /action INT для взаимодействия. Доступные для тебя хода: {self.avaliable_player_actions()}")
			act = await self.get_player_action()
			await self.handle_player_action(act)

		while not self.all_in_completed():
			to_call = self.all_in_bet - self.bets[self.cursor]
			await self.print_cout(f"Текущий игрок - {self.curr_player().nickname}\nТвой стек: {self.curr_player().money}. Для колла: {to_call}")
			await self.print_cout(f"Используй команду /action INT для взаимодействия. Доступные для тебя хода: {self.avaliable_player_actions()}")
			act = await self.get_player_action()
			await self.handle_player_action(act)
		await self.print_cout("==============Торги окончены!==============")