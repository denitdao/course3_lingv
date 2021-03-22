 	
# Таблиця лексем мови
tableOfLanguageTokens = \
	{'program':'keyword', 'end':'keyword', \
	'if':'keyword', 'then':'keyword', 'else':'keyword', 'endif':'keyword', \
	':=':'assign_op', '.':'dot', ' ':'ws', '\t':'ws', '\n':'nl', '-':'add_op', \
	'+':'add_op', '*':'mult_op', '/':'mult_op', '(':'par_op', ')':'par_op',\
	'=':'rel_op','<=':'rel_op','>=':'rel_op','<':'rel_op','>':'rel_op','<>':'rel_op'}  

# , 'for':'keyword', 'endfor':'keyword',';':'semicolon' + ; в рядку 137 + перехід (рядок 24)

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
	 (0, '<'):20, (20, '='):21,
	              (20, '>'):22,  
				  (20,'other'):23,  \
	 (0, '>'):30, (30, '='):31,  \
		          (30, 'other'):33,  \
	 (0, '='):40,   \
     (0, 'other'):101
}



initState = 0   # q0 - стартовий стан
F={2,6,9,12,13,14,101,102, 21,22,23,31,33,40}
Fstar={2,6,9, 23,33}   # зірочка
Ferror={101,102}# обробка помилок


tableOfVar={}   # Таблиця ідентифікаторів
tableOfConst={} # Таблиць констант
tableOfSymb={}  # Таблиця символів програми (таблиця розбору)


state=initState # поточний стан

f = open('test1.my_lang', 'r')
sourceCode=f.read()
f.close()

# щоб коректно обробити код увипадку,
# якщо після останньої лексеми немає пробільного символу
# або символа нового рядка
sourceCode+=' '


lenCode=len(sourceCode)-1       # номер останнього символа у файлі з кодом програми
numLine=1                       # лексичний аналіз починаємо з першого рядка
numChar=-1                      # і з першого символа (в Python'і нумерація - з 0)
char=''                         # ще не брали жодного символа
lexeme=''                       # ще не розпізнавали лексем


def lex():
	global state,char,lexeme #,numChar, numLine
	while numChar<lenCode:
		char=nextChar()
		classCh=classOfChar(char)
		state=nextState(state,classCh)
		if (is_final(state)): 
			processing()
			if state in Ferror:
				break
		elif state==0:lexeme=''
		else: lexeme+=char

def processing():
	global state,lexeme,numLine,numChar #, tableOfSymb ,char
	if state==13:		# \n
		numLine+=1
		state=0
	if state in (2,6,9):	# keyword, ident, float, int
		token=getToken(state,lexeme) 
		if token!='keyword': # не keyword
			index=indexVarConst(state,lexeme)
			print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(numLine,lexeme,token,index))
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,index)
		else: # якщо keyword
			print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token)) #print(numLine,lexeme,token)
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		numChar=putCharBack(numChar) # зірочка
		state=0
	if state == 12:         
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		state=0
	if state == 14:         
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		state=0
	if state in (21,22,31,40):
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		state=0
	if state in (23,33):
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		numChar=putCharBack(numChar) # зірочка
		state=0
	if state in (101,102):  # ERROR
		fail()

def fail():
	print(numLine)
	if state == 101:
		print('у рядку ',numLine,' неочікуваний символ '+char)
	if state == 102:
		print('у рядку ',numLine,' очікувався символ =, а не '+char)
	
		
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
	elif char in "*/+-:=();<>" :
		res=char
	return res

def getToken(state,lexeme):
	try:
		return tableOfLanguageTokens[lexeme]
	except KeyError:
		return tableIdentFloatInt[state]

def indexVarConst(state,lexeme):
	indx=0
	if state==2:
		indx=tableOfVar.get(lexeme)
		if indx is None:
			indx=len(tableOfVar)+1
			tableOfVar[lexeme]=indx
	if state in (6,9):
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
# print('-'*30)
# print('tableOfSymb:{0}'.format(tableOfSymb))
# print('tableOfVar:{0}'.format(tableOfVar))
# print('tableOfConst:{0}'.format(tableOfConst))

