 	
# Таблиця лексем мови
tableOfLanguageTokens = {'program':'keyword', 'end':'keyword', 'if':'keyword','then':'keyword','fi':'keyword',':=':'assign_op', '.':'dot', ' ':'ws', '\t':'ws', '\n':'nl', '-':'add_op', '+':'add_op', '*':'mult_op', '/':'mult_op', '(':'par_op', ')':'par_op'}
# Решту токенів визначаємо не за лексемою, а за заключним станом
tableIdentFloatInt = {2:'ident', 6:'float', 9:'int'}

# Діаграма станів
#               Q                                   q0          F
# M = ({0,1,2,4,5,6,9,11,12,13,14,101,102}, Σ,  δ , 0 , {2,6,9,12,13,14,101,102})

# δ - state-transition_function
stf={(0,'Letter'):1,  (1,'Letter'):1, (1,'Digit'):1, (1,'other'):2,\
     (0,'Digit'):4, (4,'Digit'):4, (4,'dot'):5, (4,'other'):9, (5,'Digit'):5, (5,'other'):6, \
     (0, ':'):11, (11,'='):12,\
                  (11,'other'):102,\
     (0, 'ws'):0, \
     (0, 'nl'):13, \
     (0, '+'):14, (0, '-'):14, (0, '*'):14, (0,'/'):14, (0, '('):14, (0, ')'):14, \
     (0, 'other'):101
}


initState = 0   # q0 - стартовий стан
F={2,6,9,12,13,14,101,102}
Fstar={2,6,9}   # зірочка
Ferror={101,102}# обробка помилок


tableOfId={}   # Таблиця ідентифікаторів
tableOfConst={} # Таблиць констант
tableOfSymb={}  # Таблиця символів програми (таблиця розбору)


state=initState # поточний стан

f = open('test.my_lang', 'r')
sourceCode=f.read()
f.close()

# FSuccess - ознака успішності розбору
FSuccess = (True,'Lexer')

lenCode=len(sourceCode)-1       # номер останнього символа у файлі з кодом програми
numLine=1                       # лексичний аналіз починаємо з першого рядка
numChar=-1                      # з першого символа (в Python'і нумерація - з 0)
char=''                         # ще не брали жодного символа
lexeme=''                       # ще не починали розпізнавати лексеми


def lex():
	global state,numLine,char,lexeme,numChar,FSuccess
	try:
		while numChar<lenCode:
			char=nextChar()					# прочитати наступний символ
			classCh=classOfChar(char)		# до якого класу належить 
			state=nextState(state,classCh)	# обчислити наступний стан
			if (is_final(state)): 			# якщо стан заключний
				processing()				# виконати семантичні процедури
				# if state in Ferror:	    # якщо це стан обробки помилки  
					# break					#      то припинити подальшу обробку 
			elif state==initState:lexeme=''	# якщо стан НЕ заключний, а стартовий - нова лексема
			else: lexeme+=char		# якщо стан НЕ закл. і не стартовий - додати символ до лексеми
		print('Lexer: Лексичний аналіз завершено успішно')
	except SystemExit as e:
		# Встановити ознаку неуспішності
		FSuccess = (False,'Lexer')
		# Повідомити про факт виявлення помилки
		print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))

def processing():
	global state,lexeme,char,numLine,numChar, tableOfSymb
	if state==13:		# \n
		numLine+=1
		state=initState
	if state in (2,6,9):	# keyword, ident, float, int
		token=getToken(state,lexeme) 
		if token!='keyword': # не keyword
			index=indexIdConst(state,lexeme)
			print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(numLine,lexeme,token,index))
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,index)
		else: # якщо keyword
			print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token)) #print(numLine,lexeme,token)
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		numChar=putCharBack(numChar) # зірочка
		state=initState
	if state in (12,14): #12:         # assign_op # in (12,14):  
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		state=initState
	if state in Ferror:  #(101,102):  # ERROR
		fail()

def fail():
	global state,numLine,char
	print(numLine)
	if state == 101:
		print('Lexer: у рядку ',numLine,' неочікуваний символ '+char)
		exit(101)
	if state == 102:
		print('Lexer: у рядку ',numLine,' очікувався символ =, а не '+char)
		exit(102)
	
		
def is_final(state):
	if (state in F):
		return True
	else:
		return False

def nextState(state,classCh):
	try:
		return stf[(state,classCh)]
	except KeyError:
		return stf[(state,'other')]

def nextChar():
	global numChar
	numChar+=1
	return sourceCode[numChar]

def putCharBack(numChar):
	return numChar-1

def classOfChar(char):
	if char in '.' :
		res="dot"
	elif char in 'abcdefghijklmnopqrstuvwxyz' :
		res="Letter"
	elif char in "0123456789" :
		res="Digit"
	elif char in " \t" :
		res="ws"
	elif char in "\n" :
		res="nl"
	elif char in "+-:=*/()" :
		res=char
	else: res='символ не належить алфавіту'
	return res

def getToken(state,lexeme):
	try:
		return tableOfLanguageTokens[lexeme]
	except KeyError:
		return tableIdentFloatInt[state]

def indexIdConst(state,lexeme):
	indx=0
	if state==2:
		indx=tableOfId.get(lexeme)
#		token=getToken(state,lexeme)
		if indx is None:
			indx=len(tableOfId)+1
			tableOfId[lexeme]=indx
	if state==6:
		indx=tableOfConst.get(lexeme)
		if indx is None:
			indx=len(tableOfConst)+1
			tableOfConst[lexeme]=indx
	if state==9:
		indx=tableOfConst.get(lexeme)
		if indx is None:
			indx=len(tableOfConst)+1
			tableOfConst[lexeme]=indx
	return indx


# запуск лексичного аналізатора	
lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('tableOfId:{0}'.format(tableOfId))
print('tableOfConst:{0}'.format(tableOfConst))

