from lexical_analyzer import lex, tableToPrint
from lexical_analyzer import tableOfSymb, tableOfId, tableOfConst, tableOfLabel, sourceCode
from postfix_translator import postfixTranslator, postfixCode, FSuccess
from my_stack import Stack

stack = Stack()
instrNum = 0

toView = False
simplePrint = False


def postfixInterpreter():
    FSuccess = postfixTranslator()
    # чи була успішною трансляція
    if (True, 'Translator') == FSuccess:
        # print('\nПостфіксний код: \n{0}'.format(postfixCode))
        if simplePrint: tableToPrint("all")
        return postfixProcessing()
    else:
        # Повідомити про факт виявлення помилки
        print('Interpreter: Translator завершив роботу аварійно')
        return False


def postfixProcessing():
    global stack, postfixCode, instrNum
    maxNumb = len(postfixCode)
    cycle = 0
    try:
        while instrNum < maxNumb and cycle < 100:
            lex, tok = postfixCode[instrNum]
            if tok in ('intnum', 'realnum', 'boolval', 'id', 'label'):
                stack.push((lex, tok))  # get the defined type of variable
                nextInstr = instrNum + 1
            elif tok == 'jump':
                nextInstr = doJump(lex, nextInstr)
                cycle += 1
            elif tok == 'iocmnd':
                doIO(lex)
                nextInstr = instrNum + 1
            else:
                doIt(lex, tok)
                nextInstr = instrNum + 1
            if toView:
                configToPrint(instrNum, lex, tok, maxNumb)
            instrNum = nextInstr
        
        if simplePrint: tableToPrint("Id")
        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('RunTime: Аварійне завершення програми з кодом {0}'.format(e))
    return True


def configToPrint(step, lex, tok, maxN):
    if step == 1:
        print('='*30+'\nInterpreter run\n')
        tableToPrint('All')

    print('\nКрок інтерпретації: {0}'.format(step))
    if tok in ('intnum', 'realnum'):
        print('Лексема: {0} у таблиці констант: {1}'.format(
            (lex, tok), lex + ':' + str(tableOfConst[lex])))
    elif tok in ('id'):
        print('Лексема: {0} у таблиці ідентифікаторів: {1}'.format(
            (lex, tok), lex + ':' + str(tableOfId[lex])))
    else:
        print('Лексема: {0}'.format((lex, tok)))

    print('postfixCode={0}'.format(postfixCode))
    stack.print()

    if step == maxN:
        for Tbl in ('Id', 'Const', 'Label'):
            tableToPrint(Tbl)
    return True


def doIO(lexL):
    # зняти з вершини стека змінну
    (lexR, tokR) = stack.pop()
    if tokR == 'id':
        tokR = tableOfId[lexR][1]
    
    if lexL == "OUT":
        if tableOfId[lexR][2] == 'val_undef':
            failRunTime('неініціалізована змінна', (lexR, tableOfId[lexR], (lexL, 'iocmnd'), '', (lexR, tokR)))
        print(tableOfId[lexR][2])
    elif lexL == "IN":
        try:
            if tokR == 'intnum':
                result = int(input())
                tableOfId[lexR] = (tableOfId[lexR][0], tokR, result)
            elif tokR == 'realnum':
                result = float(input())
                tableOfId[lexR] = (tableOfId[lexR][0], tokR, result)
            elif tokR == 'boolval':
                result = bool(input())
                tableOfId[lexR] = (tableOfId[lexR][0], tokR, result)
        except:
            failRunTime('невідповідність вводу',
                        (lexL, (lexR, tokR)))


def doJump(lex, nextInstr):
    # зняти з вершини стека мітку
    (lexL, tokL) = stack.pop()
    if lex == "JF":
        # зняти з вершини стека логічне значення
        (lexR, tokR) = stack.pop()
        if (tokR == 'boolval') and (lexR == 'false'):
            if simplePrint: print("->", lexR, lexL, "|", tokR, tokL)
            return tableOfLabel[lexL]
    elif lex == "JMP":
        if simplePrint: print("->", lexL, "|", tokL)
        return tableOfLabel[lexL]
    return nextInstr + 1


def doIt(lex, tok):
    global stack, postfixCode, tableOfId, tableOfConst
    if (lex, tok) == ('=', 'assign_op'):
        # зняти з вершини стека запис (правий операнд = число)
        (lexL, tokL) = stack.pop()
        # зняти з вершини стека ідентифікатор (лівий операнд)
        (lexR, tokR) = stack.pop()

        rightWasId = False

        if tokL == 'id':
            tokL = tableOfId[lexL][1]   
            rightWasId = True
             
        if tokR == 'id':
            tokR = tableOfId[lexR][1]

        if simplePrint: print(lexR, lex, lexL, "|", tokR, lex, tokL)
            
        if rightWasId and tableOfId[lexL][2] == 'val_undef':
            failRunTime('неініціалізована змінна', (lexL, tableOfId[lexL], (lexL, tokL), lex, (lexR, tokR)))

        # виконати операцію:
        # оновлюємо запис у таблиці ідентифікаторів
        # ідентифікатор/змінна
        # (index не змінюється,
        # тип - не змінюється,
        # значення - як у константи)

        if tokL != tokR and (tokL, tokR) not in (('intnum', 'realnum')):
            failRunTime('невідповідність типів',
                        ((lexL, tokL), lex, (lexR, tokR)))
        else:
            if (tokL == 'boolval'):
                tableOfId[lexR] = (tableOfId[lexR][0], tokR,
                                   True if (lexL == 'true') else False)
            else:
                # handle the case of: var = var
                tableOfId[lexR] = (tableOfId[lexR][0],
                                   tokR, tableOfId[lexL][2] if rightWasId else tableOfConst[lexL][2])

    elif tok in ('add_op', 'mult_op', 'pow_op', 'rel_op'):
        # зняти з вершини стека запис (правий операнд)
        (lexR, tokR) = stack.pop()
        # зняти з вершини стека запис (лівий операнд)
        (lexL, tokL) = stack.pop()

        processing_add_some_op((lexL, tokL), lex, tok, (lexR, tokR))

    return True


def processing_add_some_op(ltL, lex, tok, ltR):
    global stack, postfixCode, tableOfId, tableOfConst
    lexL, tokL = ltL
    lexR, tokR = ltR
    old_tokL = tokL  # for operations which return left token back to stack
    if tokL == 'id':
        if tableOfId[lexL][2] == 'val_undef' and lex != 'NEG':
            failRunTime('неініціалізована змінна', (lexL,
                                                    tableOfId[lexL], (lexL, tokL), lex, (lexR, tokR)))
        else:
            valL, tokL = (tableOfId[lexL][2], tableOfId[lexL][1])
    elif tokL == 'boolval':
        valL = True if (lexL == 'true') else False
    else:
        valL = tableOfConst[lexL][2]
    if tokR == 'id':
        if tableOfId[lexR][2] == 'val_undef':
            failRunTime('неініціалізована змінна', (lexR,
                                                    tableOfId[lexR], (lexL, tokL), lex, (lexR, tokR)))
        else:
            valR, tokR = (tableOfId[lexR][2], tableOfId[lexR][1])
    elif tokR == 'boolval':
        valR = True if (lexR == 'true') else False
    else:
        valR = tableOfConst[lexR][2]

    if tok in ('add_op', 'mult_op', 'pow_op') and (tokL != 'boolval' and tokR != 'boolval'):
        getNumValue((valL, lexL, tokL), lex, (valR, lexR, tokR), old_tokL)
    elif tok in ('rel_op'):
        getBoolValue((valL, lexL, tokL), lex, (valR, lexR, tokR))
    else:
        failRunTime('невідповідність типів',
                    ((lexL, tokL), lex, (lexR, tokR)))


def getNumValue(vtL, lex, vtR, old_tokL):
    global stack, postfixCode, tableOfId, tableOfConst
    valL, lexL, tokL = vtL
    valR, lexR, tokR = vtR
    if lex == '+':
        value = valL + valR
    elif lex == '-':
        value = valL - valR
    elif lex == '*':
        value = valL * valR
    elif lex == '/' and valR == 0:
        failRunTime('ділення на нуль', ((lexL, tokL), lex, (lexR, tokR)))
    elif lex == '/' and (tokL, tokR) == ('intnum', 'intnum'):
        value = int(valL / valR)
    elif lex == '/':
        value = valL / valR
    elif lex == '^':
        value = valL ** valR
    elif lex == 'div':
        value = valL % valR
    elif lex == 'NEG':
        value = -valR
        stack.push((lexL, old_tokL))
    else:
        pass
    if simplePrint: print(lexL, lex, lexR, "|", tokL, lex, tokR, " => ", value)

    if (tokL == tokR):
        stack.push((str(value), tokL))
        toTableOfConst(value, tokL)
    elif (tokL, tokR) in (('intnum', 'realnum'), ('realnum', 'intnum')):
        stack.push((str(value), 'realnum'))
        toTableOfConst(value, 'realnum')


def getBoolValue(vtL, lex, vtR):
    global stack, postfixCode, tableOfId, tableOfConst
    valL, lexL, tokL = vtL
    valR, lexR, tokR = vtR
    if lex == '==':
        value = valL == valR
    elif lex == '>':
        value = valL > valR
    elif lex == '<':
        value = valL < valR
    elif lex == '<=':
        value = valL <= valR
    elif lex == '>=':
        value = valL >= valR
    elif lex == '!=':
        value = valL != valR
    else:
        pass
    if simplePrint: print(lexL, lex, lexR, "|", tokL, lex, tokR, " => ", value)
    stack.push((str(value).lower(), 'boolval'))
    toTableOfConst(value, 'boolval')


def toTableOfConst(val, tok):
    lexeme = str(val)
    indx1 = tableOfConst.get(lexeme)
    if indx1 is None:
        indx = len(tableOfConst)+1
        tableOfConst[lexeme] = (indx, tok, val)


def failRunTime(str, tuple):
    if str == 'невідповідність типів':
        ((lexL, tokL), lex, (lexR, tokR)) = tuple
        print('RunTime ERROR: \n\t Типи операндів відрізняються у {0} {1} {2}'.format(
            (lexL, tokL), lex, (lexR, tokR)))
        exit(1)
    elif str == 'неініціалізована змінна':
        (lx, rec, (lexL, tokL), lex, (lexR, tokR)) = tuple
        print('RunTime ERROR: \n\t Значення змінної {0}:{1} не визначене. Зустрілось у {2} {3} {4}'.format(
            lx, rec, (lexL, tokL), lex, (lexR, tokR)))
        exit(2)
    elif str == 'ділення на нуль':
        ((lexL, tokL), lex, (lexR, tokR)) = tuple
        print('RunTime ERROR: \n\t Ділення на нуль у {0} {1} {2}. '.format(
            (lexL, tokL), lex, (lexR, tokR)))
        exit(3)
    elif str == 'невідповідність вводу':
        (lex, (lexR, tokR)) = tuple
        print('RunTime ERROR: \n\t Введене значення не відповідає потрібному {0} {1}'.format(lex, (lexR, tokR)))
        exit(4)


postfixInterpreter()
