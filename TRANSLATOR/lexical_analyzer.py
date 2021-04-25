import pprint

programFileName = 'test.dch'

# Таблиця лексем мови
tableOfLanguageTokens = {'true': 'boolval',
                         'false': 'boolval',
                         'program': 'keyword',
                         'var': 'keyword',
                         'begin': 'keyword',
                         'end': 'keyword',
                         'integer': 'keyword',
                         'real': 'keyword',
                         'boolean': 'keyword',
                         'read': 'keyword',
                         'write': 'keyword',
                         'for': 'keyword',
                         'if': 'keyword',
                         'then': 'keyword',
                         '=': 'assign_op',
                         '+': 'add_op',
                         '-': 'add_op',
                         '*': 'mult_op',
                         '/': 'mult_op',
                         'div': 'mult_op',
                         '^': 'pow_op',
                         '<': 'rel_op',
                         '<=': 'rel_op',
                         '==': 'rel_op',
                         '>=': 'rel_op',
                         '>': 'rel_op',
                         '!=': 'rel_op',
                         '(': 'brackets_op',
                         ')': 'brackets_op',
                         '{': 'brackets_op',
                         '}': 'brackets_op',
                         '.': 'punct',
                         ',': 'punct',
                         ';': 'punct',
                         ' ': 'ws',
                         '\t': 'ws',
                         '\n': 'eol',
                         '\r\n': 'eol',
                         '\0': 'eof'}

# Решту токенів визначаємо не за лексемою, а за заключним станом
tableIdIntRealNum = {2: 'id',
                     6: 'intnum',
                     5: 'realnum'}

# Діаграма станів
#                      Q                               q0                 F
# M = ({0,1,2,3,4,5,6,7,8,9,10,11,12,13,101,102}, Σ,  δ , 0 , {2,5,6,7,8,9,10,11,12,101,102})

# δ - state-transition_function
stf = {(0, 'Letter'): 1,  (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'dot'): 4, (4, 'Digit'): 4, (4, 'other'): 5, (3, 'other'): 6,
       (0, 'dot'): 4, (4, 'Digit'): 4, (4, 'other'): 5,
       (0, 'ws'): 0,
       (0, 'nl'): 10,
       (0, 'Brackets'): 9,
       (0, 'Arithmetic'): 12,
       (0, ','): 11, (0, ';'): 11,
       (0, '!'): 13, (13, '='): 8,
       (0, '<'): 7, (0, '>'): 7, (0, '='): 7, (7, '='): 8,
       (13, 'other'): 102,
       (0, 'other'): 101
       }

initState = 0   # q0 - стартовий стан
F = {2, 5, 6, 7, 8, 9, 10, 11, 12, 101, 102}
Fstar = {2, 5, 6}   # зірочка
Ferror = {101, 102}  # обробка помилок


tableOfId = {}   # Таблиця ідентифікаторів
tableOfConst = {}  # Таблиць констант
tableOfSymb = {}  # Таблиця символів програми (таблиця розбору)
tableOfLabel={}  # Таблиця символів міток програми 

state = initState  # поточний стан

f = open(programFileName, 'r')
sourceCode = f.read()
f.close()

# FSuccess - ознака успішності розбору
FSuccess = (True, 'Lexer')

# номер останнього символа у файлі з кодом програми
lenCode = len(sourceCode) - 1
numLine = 1                       # лексичний аналіз починаємо з першого рядка
# з першого символа (в Python'і нумерація - з 0)
numChar = -1
char = ''                         # ще не брали жодного символа
lexeme = ''                       # ще не починали розпізнавати лексеми


def lex():
	global state, numLine, char, lexeme, numChar, FSuccess
	try:
		while numChar < lenCode:
			char = nextChar()					# прочитати наступний символ
			classCh = classOfChar(char)		    # до якого класу належить
			state = nextState(state, classCh)   # обчислити наступний стан
			if (is_final(state)): 				# якщо стан заключний
				processing()					# виконати семантичні процедури
				# if state in Ferror:	    # якщо це стан обробки помилки
				# break					#      то припинити подальшу обробку
			elif state == initState:
				lexeme = ''  # якщо стан НЕ заключний, а стартовий - нова лексема
			else:
				lexeme += char		# якщо стан НЕ закл. і не стартовий - додати символ до лексеми

		char = '\n'							# передати заключний символ
		classCh = classOfChar(char)		    # до якого класу належить
		state = nextState(state, classCh)   # обчислити наступний стан
		if (is_final(state)): 				# якщо стан заключний
			processing()					# виконати семантичні процедури

		print('Lexer: Лексичний аналіз завершено успішно')
	except SystemExit as e:
		# Встановити ознаку неуспішності
		FSuccess = (False, 'Lexer')
		# Повідомити про факт виявлення помилки
		print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))


def processing():
	global state, lexeme, char, numLine, numChar, tableOfSymb
	if state == 10:		# \n
		numLine += 1
		state = initState
	if state in Fstar:  # keyword, id, intnum, realnum
		token = getToken(state, lexeme)
		if token not in ('keyword', 'boolval', 'mult_op'):  # не keyword
			index = indexIdConst(state, lexeme, token)
			tableOfSymb[len(tableOfSymb)+1] = (numLine, lexeme, token, index)
		else:  # якщо keyword, boolval, div
			tableOfSymb[len(tableOfSymb)+1] = (numLine, lexeme, token, '')
		lexeme = ''
		numChar = putCharBack(numChar)  # зірочка
		state = initState
	if state in (8, 9, 11, 12):  # <=, >=, !=, ==, Brackets, ;, ,, Arithmetic
		lexeme += char
		token = getToken(state, lexeme)
		tableOfSymb[len(tableOfSymb)+1] = (numLine, lexeme, token, '')
		lexeme = ''
		state = initState
	if state == 7:  # assign_op, <, >
		charNext = nextChar()  # check next char
		numChar = putCharBack(numChar)
		lexeme += char
		if charNext != '=':
			token = getToken(state, lexeme)
			tableOfSymb[len(tableOfSymb)+1] = (numLine, lexeme, token, '')
			lexeme = ''
			state = initState
	if state in Ferror:  # (101,102):  # ERROR
		fail()


def fail():
	global state, numLine, char
	print(numLine)
	if state == 101:
		print('Lexer: у рядку ', numLine, ' неочікуваний символ \'' + char + '\'')
		exit(101)
	if state == 102:
		print('Lexer: у рядку ', numLine, ' очікувався символ =, а не \'' + char + '\'')
		exit(102)


def is_final(state):
	if (state in F):
		return True
	else:
		return False


def nextState(state, classCh):
	try:
		return stf[(state, classCh)]
	except KeyError:
		return stf[(state, 'other')]


def nextChar():
	global numChar
	numChar += 1
	return sourceCode[numChar]


def putCharBack(numChar):
	return numChar-1


def classOfChar(char):
	if char in '.':
		res = "dot"
	elif char in 'abcdefghijklmnopqrstuvwxyz':
		res = "Letter"
	elif char in "0123456789":
		res = "Digit"
	elif char in " \t":
		res = "ws"
	elif char in "\r\n":
		res = "nl"
	elif char in "(){}":
		res = "Brackets"
	elif char in "+-/*^":
		res = "Arithmetic"
	elif char in "!<>=;,":
		res = char
	else:
		res = 'символ не належить алфавіту'
	return res


def getToken(state, lexeme):
	try:
		return tableOfLanguageTokens[lexeme]
	except KeyError:
		return tableIdIntRealNum[state]


def indexIdConst(state, lexeme, token):
	indx = 0
	if state == 2: # id
		indx1 = tableOfId.get(lexeme)
		if indx1 is None:
			indx = len(tableOfId)+1
			tableOfId[lexeme] = (indx, 'type_undef', 'val_undef')
	if state == 6: # intnum
		indx1 = tableOfConst.get(lexeme)
		if indx1 is None:
			indx = len(tableOfConst)+1
			val = int(lexeme)
			tableOfConst[lexeme] = (indx, token, val)
	if state == 5: # realnum
		indx1 = tableOfConst.get(lexeme)
		if indx1 is None:
			indx = len(tableOfConst)+1
			val = float(lexeme)
			tableOfConst[lexeme] = (indx, token, val)
	if not (indx1 is None): 
		if len(indx1) == 2: 
			indx, _ = indx1
		else: 
			indx, _, _ = indx1
	return indx


def tableToPrint(Tbl):
	if Tbl == "Symb":
		tableOfSymbToPrint()
	elif Tbl == "Id":
		tableOfIdToPrint()
	elif Tbl == "Const":
		tableOfConstToPrint()
	else:
		tableOfSymbToPrint()
		tableOfIdToPrint()
		tableOfConstToPrint()
	return True


def tableOfSymbToPrint():
	print("\n Таблиця символів")
	s1 = '{0:<10s} {1:<10s} {2:<10s} {3:<10s} {4:<5s}'
	s2 = '{0:<10d} {1:<10d} {2:<10s} {3:<10s} {4:<5s}'
	print(s1.format("numRec", "numLine", "lexeme", "token", "index"))
	for numRec in tableOfSymb:  # range(1,lns+1):
		numLine, lexeme, token, index = tableOfSymb[numRec]
		print(s2.format(numRec, numLine, lexeme, token, str(index)))


def tableOfIdToPrint():
	print("\n Таблиця ідентифікаторів")
	s1 = '{0:<10s} {1:<15s} {2:<15s} {3:<10s} '
	print(s1.format("Ident", "Type", "Value", "Index"))
	s2 = '{0:<10s} {2:<15s} {3:<15s} {1:<10d} '
	for id in tableOfId:
		index, type, val = tableOfId[id]
		print(s2.format(id, index, type, str(val)))


def tableOfConstToPrint():
	print("\n Таблиця констант")
	s1 = '{0:<10s} {1:<10s} {2:<10s} {3:<10s} '
	print(s1.format("Const", "Type", "Value", "Index"))
	s2 = '{0:<10s} {2:<10s} {3:<10} {1:<10d} '
	for cnst in tableOfConst:
		index, type, val = tableOfConst[cnst]
		print(s2.format(str(cnst), index, type, val))


# запуск лексичного аналізатора
# lex()
# tableToPrint("All")

