from lex_my_lang import lex
from lex_my_lang import tableOfSymb  # , tableOfVar, tableOfConst


lex()
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow = 1
# кількість записів у таблиці розбору
len_tableOfSymb = len(tableOfSymb)

# Функція для розбору за правилом
# Program = program StatementList end
# читає таблицю розбору tableOfSymb


def parseProgram():
       try:
            # перевірити наявність ключового слова 'program'
            parseToken('program', 'keyword', '')

            # перевірити синтаксичну коректність списку інструкцій StatementList
            parseStatementList()

            # перевірити наявність ключового слова 'end'
            parseToken('end', 'keyword', '')

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
            failParse('неочікуваний кінець програми', (lexeme,token,numRow))

        # прочитати з таблиці розбору
        # номер рядка програми, лексему та її токен
        numLine, lex, tok = getSymb()
        # тепер поточним буде наступний рядок таблиці розбору
        numRow += 1

        # чи збігаються лексема та токен таблиці розбору з заданими
        if (lex, tok) == (lexeme, token):
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent+'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme,token)))
            return True
        else:
            # згенерувати помилку та інформацію про те, що
            # лексема та токен таблиці розбору (lex,tok) відрізняються від
            # очікуваних (lexeme,token)
            failParse('невідповідність токенів', (numLine,lex,tok,lexeme,token))
            return False


# Прочитати з таблиці розбору поточний запис за його номером numRow
# Повертає номер рядка програми, лексему та її токен
def getSymb():
    # таблиця розбору реалізована у формі словника (dictionary)
    # tableOfSymb = {numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow]
    return numLine, lexeme, token


# Обробити помилки
# зараз це - єдина можлива з описом 'невідповідність токенів'
def failParse(str, tuple):
       if str == 'неочікуваний кінець програми':
            (lexeme,token,numRow) = tuple
            print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format((lexeme, token),numRow))
            exit(1001)
        elif str == 'невідповідність токенів':
            (numLine,lexeme,token,lex,tok) = tuple
            print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(numLine, lexeme,token,lex,tok))
            exit(1)


# Функція-заглушка (stub) для розбору за правилом для StatementList
# просто повідомляє про її виклик
# завжди повертає True
def parseStatementList():
       print('\t parseStatementList():')
        return True


parseProgram()
