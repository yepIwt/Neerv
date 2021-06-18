"""
	actions:
	(1) FOLD
	(2) BET
	(3) CALL
	(4) ALL_IN
"""
MONEY = [1000,2000,3000,4000,5000]
BETS = [10,20,0,0,0]
CURSOR = None
PLAYER_BET = 0
FOLDED_BETS = 0
ALL_IN_BET = 0

def next(to):
	global FOLDED_BETS, BETS, CURSOR
	return (to + 1) % len(BETS)

def bets_are_equal():
	global FOLDED_BETS, BETS, CURSOR
	if len(set(BETS)) == 1:
		return True
	return False

def avaliable_player_actions():
	global CURSOR, MONEY, ALL_IN_BET
	if ALL_IN_BET:
		if ALL_IN_BET - BETS[CURSOR] > MONEY[CURSOR]:
			return [1,4]
		return [1,3]
	elif MONEY[CURSOR] < PLAYER_BET:
		return [1,4]
	else:
		return [1,2,3,4]

def input_action():
	act = int(input(f"Введите действие: {avaliable_player_actions()}: "))
	while act not in avaliable_player_actions():
		act = int(input(f"Введите действие: {avaliable_player_actions()}: "))
	return act

def bet(howmch: int):
	global FOLDED_BETS, BETS, CURSOR
	BETS[CURSOR] += howmch

def call():
	global FOLDED_BETS, BETS, CURSOR, ALL_IN_BET
	if not ALL_IN_BET:
		MONEY[CURSOR] -= PLAYER_BET - BETS[CURSOR]
		BETS[CURSOR] += PLAYER_BET - BETS[CURSOR]
	else:
		MONEY[CURSOR] -= ALL_IN_BET - BETS[CURSOR]
		BETS[CURSOR] += ALL_IN_BET - BETS[CURSOR]
	CURSOR = next(CURSOR)

def fold():
	global FOLDED_BETS, BETS, CURSOR
	FOLDED_BETS += BETS[CURSOR]
	#players.erase
	BETS.pop(CURSOR)
	print("Player folds...")
	if CURSOR >= len(BETS): CURSOR = 0

def all_in():
	global FOLDED_BETS, BETS, CURSOR,ALL_IN_BET
	BETS[CURSOR] += MONEY[CURSOR]
	if not ALL_IN_BET:
		ALL_IN_BET = MONEY[CURSOR]
	MONEY[CURSOR] = 0
	CURSOR = next(CURSOR)

def player_bets():
	global FOLDED_BETS, BETS, CURSOR,PLAYER_BET
	prev_bet = PLAYER_BET
	# your bank is ..
	print(f'[PLAYER_BETS] Your bank is {MONEY[CURSOR]}')
	PLAYER_BET = int(input('Enter bet: '))
	while PLAYER_BET > MONEY[CURSOR] or PLAYER_BET < PLAYER_BET:
		PLAYER_BET = int(input('Enter valid bet: '))

	if PLAYER_BET == MONEY[CURSOR]:
		print("Player allin...")
		all_in()
		#CURSOR = next(CURSOR)
	else:
		if prev_bet == PLAYER_BET:
			print('Player calls...')
		else:
			print(f'Player bets {PLAYER_BET}...')
		bet(PLAYER_BET)
		CURSOR = next(CURSOR)

def all_in_completed():
	global BETS,ALL_IN_BET,MONEY,CURSOR
	print("========ALL IN COMPLETED:", BETS)
	for bet_i in range(len(BETS)):
		if BETS[bet_i] >= ALL_IN_BET:
			continue
		else:
			if MONEY[bet_i] == 0:
				continue
			else:
				return False
	return True

def handle_action(act):
    if act == 1:
        fold()
    elif act == 2:
    	player_bets()
    elif act == 3:
        call()
    elif act == 4:
        all_in()

def makeBets():
	global FOLDED_BETS, BETS, CURSOR, ALL_IN_BET, PLAYER_BET
	CURSOR = 2
	PLAYER_BET = 20
	while bets_are_equal() != True and not ALL_IN_BET:
		print("////////PLAYERS: ", BETS)
		print("////////PLAYER:  CURSOR: , ", CURSOR)
		player_action = input_action()
		handle_action(player_action)

	while not all_in_completed():
		print("////////PLAYERS: ", BETS)
		print("////////PLAYER:  CURSOR: , ", CURSOR)
		to_call = ALL_IN_BET - BETS[CURSOR]
		print(f"Your bank is {MONEY[CURSOR]}. To call: {to_call}",)
		player_action = input_action()
		handle_action(player_action)

if __name__ == '__main__':
    makeBets()
    print("Торги закончены")
    print(BETS,MONEY)