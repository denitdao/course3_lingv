from lexical_analyzer import lex
from lexical_analyzer import tableOfSymb  # , tableOfVar, tableOfConst

lex()
print('-'*30)

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow = 1
# кількість записів у таблиці розбору
len_tableOfSymb = len(tableOfSymb)


def parseProgram():
    try:
        # перевірити наявність ключового слова 'program'
        parseToken('program', 'keyword', '')

        parseProgName()
        parseDeclSection()
        parseDoSection()

        # повідомити про синтаксичну коректність програми
        print('Parser: Синтаксичний аналіз завершився успішно')
        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('Parser: Аварійне завершення програми з кодом {0}'.format(e))


# Функція перевіряє, чи у поточному рядку таблиці розбору
# зустрілась вказана лексема lexeme з токеном token
# параметр indent - відступ при виведенні у консоль
def parseToken(lexeme, token, indent):
    # доступ до поточного рядка таблиці розбору
    global numRow

    # перевірити, чи є ще записи в таблиці розбору
    # len_tableOfSymb - кількість лексем (записів) у таблиці розбору
    if numRow > len_tableOfSymb:
        failParse('неочікуваний кінець програми', (lexeme, token, numRow))

    # прочитати з таблиці розбору
    # номер рядка програми, лексему та її токен
    numLine, lex, tok = getSymb()
    # тепер поточним буде наступний рядок таблиці розбору
    numRow += 1

    # чи збігаються лексема та токен таблиці розбору з заданими
    if (lex, tok) == (lexeme, token):
        # вивести у консоль номер рядка програми та лексему і токен
        print(
            '+ '+indent+'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
        return True
    else:
        # згенерувати помилку та інформацію про те, що
        # лексема та токен таблиці розбору (lex,tok) відрізняються від
        # очікуваних (lexeme,token)
        failParse('невідповідність токенів',
                  (numLine, lex, tok, lexeme, token))
        return False


# Прочитати з таблиці розбору поточний запис
# Повертає номер рядка програми, лексему та її токен
def getSymb():
    if numRow > len_tableOfSymb:
        failParse('getSymb(): неочікуваний кінець програми', numRow)
    # таблиця розбору реалізована у формі словника (dictionary)
    # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow]
    return numLine, lexeme, token


# Обробити помилки
# зараз це - єдина можлива з описом 'невідповідність токенів'
def failParse(str, tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme, token, numRow) = tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(
            (lexeme, token), numRow))
        exit(1001)
    if str == 'getSymb(): неочікуваний кінець програми':
        numRow = tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(
            numRow, tableOfSymb[numRow-1]))
        exit(1002)
    elif str == 'невідповідність токенів':
        (numLine, lexeme, token, lex, tok) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - ({3}, {4}).'.format(
            numLine, lexeme, token, lex, tok))
        exit(1)
    elif str == 'невідповідність інструкцій':
        (numLine, lex, tok, expected) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.'.format(
            numLine, lex, tok, expected))
        exit(2)
    elif str == 'невідповідність у Expression.Factor':
        (numLine, lex, tok, expected) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.'.format(
            numLine, lex, tok, expected))
        exit(3)
    elif str == 'mismatch in BoolExpr':
        (numLine, lex, tok, expected) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.'.format(
            numLine, lex, tok, expected))
        exit(4)  

# ---------------------------------- PARSERS ----------------------------------


def parseProgName():
    print('parseProgName():')
    return parseIdent()


def parseDeclSection():
    print('parseDeclSection():')
    parseToken('var', 'keyword', '')
    parseDeclarList()
    return True


def parseDoSection():
    print('parseDoSection():')
    parseToken('begin', 'keyword', '')
    parseStatementList()
    parseToken('end', 'keyword', '')
    return True


def parseDeclarList():
    print('\tparseDeclarList():')
    while parseDeclaration():
        parseToken(';', 'punct', '\t'*2)
    return True


def parseDeclaration():
    F = parseType()
    if F:
        return parseIdentList()
    return F


def parseType():
    global numRow
    print('\t'*2 + 'parseType():')
    numLine, lex, tok = getSymb()
    if tok == 'keyword' and lex in ('real', 'integer', 'boolean'):
        numRow += 1
        print('+'+'\t'*3 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        return True
    elif (lex, tok) == ('begin', 'keyword'):
        return False
    else:
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'keyword'))
        return False


def parseIdentList():
    global numRow
    print('\t'*2 + 'parseIdentList():')
    parseIdent()

    F = True
    while F:
        numLine, lex, tok = getSymb()
        if tok == 'punct' and lex == ',':
            numRow += 1
            print('+'+'\t'*3 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parseIdent()
        else:
            F = False
    return True


def parseIdent():
    global numRow
    print('\t'*3 + 'parseIdent():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    if tok == 'id':
        numRow += 1
        print('+'+'\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        return True
    else:
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'id'))
        return False


def parseStatementList():
    print('~~~\tparseStatementList():')
    F = True
    while F:
        F = parseStatement()
        if F == 'пропуск символу ;':
            pass
        elif F == True:
            parseToken(';', 'punct', '\t')
        else: 
            break
    return True


def parseStatement():
    print('\t'*2 + 'parseStatement():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор, обробити інструкцію присвоювання
    if tok == 'id':
        return parseAssign()
    if (lex, tok) == ('read', 'keyword'):
        return parseInp()
    if (lex, tok) == ('write', 'keyword'):
        return parseOut()
    elif (lex, tok) == ('if', 'keyword'):
        return parseIfStatement()
    elif (lex, tok) == ('for', 'keyword'):
        return parseForStatement()
    # parseStatement() має завершити роботу
    elif (lex, tok) == ('end', 'keyword'):
        return False
    elif (lex, tok) == ('}', 'brackets_op'):
        return False
    # жодна з інструкцій не відповідає поточній лексемі у таблиці розбору
    else:
        failParse('невідповідність інструкцій',
                  (numLine, lex, tok, 'ident, if, for, read, write'))
        return False


def parseAssign():
    global numRow
    print('\t'*3 + 'parseAssign():')
    parseIdent()
    if parseToken('=', 'assign_op', '\t'*3):
        return parseArithmExpr()
    else:
        return False


def parseExpression():
    global numRow
    print('\t'*4 + 'parseExpression():')
    numLine, lex, tok = getSymb()
    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            print('+'+'\t'*5 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parseTerm()
        else:
            F = False
    return True


def parseArithmExpr():
    global numRow
    print('\t'*4 + 'parseArithmExpr():')
    
    # символи '+' або '-'
    numLine, lex, tok = getSymb()
    if (tok == 'add_op'):
        numRow += 1
        print('+'+'\t'*5 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    
    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            print('+'+'\t'*5 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parseTerm()
        else:
            F = False
    return True


def parseTerm():
    global numRow
    print('\t'*5 + 'parseTerm():')
    parseFactor()
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*', '/', '^'...
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op', 'pow_op'):
            numRow += 1
            print('+'+'\t'*6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parseFactor()
        else:
            F = False
    return True


def parseFactor():
    global numRow
    numLine, lex, tok = getSymb()
    print('\t'*6 + 'parseFactor():')

    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('intnum', 'realnum', 'boolval', 'id'):
        numRow += 1
        print('+'+'\t'*6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))

    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex == '(' and tok == 'brackets_op':
        parseToken('(', 'brackets_op', '--\t'*6)
        parseArithmExpr()
        parseToken(')', 'brackets_op', '--\t'*6)
    else:
        failParse('невідповідність у Expression.Factor', (numLine, lex,
                                                          tok, 'rel_op, int, float, ident або \'(\' Expression \')\''))
    return True


def parseInp():
    F = parseToken('read', 'keyword', '\t'*3)
    if F:
        F = (parseToken('(', 'brackets_op', '\t'*3) and 
            parseIdentList() and 
            parseToken(')', 'brackets_op', '\t'*3))
    return F


def parseOut():
    F = parseToken('write', 'keyword', '\t'*3)
    if F:
        F = parseToken('(', 'brackets_op', '\t'*3)
        _, lex, tok = getSymb()
        if (lex, tok) != (')', 'brackets_op'):
            parseIdentList() 
        F = F and parseToken(')', 'brackets_op', '\t'*3)
    return F


# IfStatement = if CondExpr then DoBlock
def parseIfStatement():
    global numRow
    print('\t'*3 + 'parseIfStatement():')
    numLine, lex, tok = getSymb()
    if lex == 'if' and tok == 'keyword':
        numRow += 1
        print('+'+'\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        parseBoolExpr()
        parseToken('then', 'keyword', '\t'*4)
        return parseDoBlock()
    else:
        return False


def parseForStatement():
    _, lex, tok = getSymb()
    if lex == 'for' and tok == 'keyword':
        parseToken('for', 'keyword', '\t'*5)
        parseToken('(', 'brackets_op', '--\t'*6)
        parseAssign()
        parseToken(';', 'punct', '\t'*6)
        parseBoolExpr()
        parseToken(';', 'punct', '\t'*6)
        parseAssign()
        parseToken(')', 'brackets_op', '--\t'*6)
        return parseDoBlock()
    else:
        return False


def parseDoBlock():
    print('\t'*3 + 'parseDoBlock():')
    _, lex, tok = getSymb()
    if lex == '{' and tok == 'brackets_op':
        parseToken('{', 'brackets_op', '--\t'*4)
        parseStatementList()
        parseToken('}', 'brackets_op', '--\t'*4)
        return 'пропуск символу ;' # для валідації, що після } не має бути ;
    else:
        return parseStatement()

# розбір логічного виразу за правиллом
# BoolExpr = ArithmExpr RelOp ArithmExpr
def parseBoolExpr():
    global numRow
    parseArithmExpr()
    numLine, lex, tok = getSymb()
    if tok in ('rel_op'):
        numRow += 1
        print('+'+'\t'*5 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    else:
        failParse('mismatch in BoolExpr', (numLine, lex, tok, 'relop'))
    parseArithmExpr()
    return True


# запуск парсера
parseProgram()
