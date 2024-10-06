
connectives = ["~", "^", "v", "->", "<->"] 
vars = ["p", "q", "r"]
matchingBrackets = {"(": ")"}  

openBrackets = set(matchingBrackets.keys())
closeBrackets = set(matchingBrackets.values())

firstVar = []
secondVar = []
thirdVar = []

negationFirstVar = [] 
negationSecondVar = []
negationThirdVar= []

variables = []

rowCount = 0
valid = True  # Glinobal ko kase para same sa lahat na ng fucking functions, (cge po)

# Flag to check if P Q R is negated
negateP = False 
negateQ = False
negateR = False

def userInput():
    global variables
    subStatements = []
    statement = input("Enter a statement: ").lower()
    words = statement.split()
    
    if checkParentheses(words) and syntaxChecker(words):
        variables, subStatements = extractPropositions(statement)

        print("Propositional Variables:", variables) #Print test forda variables bes same thing sa bottom
        print("Sub-statements:", subStatements)

    evaluateStatement(subStatements, variables)

def checkParentheses(words):
    global valid  # Idineclare ko para mamodify dito sa function yung tang-inang global var na yon
    stackParentheses = []  
    for word in words: 
        if word in matchingBrackets.keys():  
            stackParentheses.append(word)  
        elif word in matchingBrackets.values():  
            if stackParentheses and matchingBrackets[stackParentheses[-1]] == word:  
                stackParentheses.pop()  
            else:
                print("Invalid Statement: Unmatched closing parenthesis") 
                valid = False
                return False  

    if not stackParentheses:  
        print("Parentheses are balanced.")
    else:
        print("Parentheses are not balanced.")
        valid = False

    if valid:
        return True

def syntaxChecker(words):
    global valid, negateP, negateQ, negateR
    variables = []  # Store variables used
    connectivesUsed = []  # Store connectives used
    negationStack = []  # Store negation used
    
    # To check syntax din by Basilio

    for index, word in enumerate(words):
        if word.isalpha() and word in vars:  
            variables.append(word)
            if negationStack and negationStack[-1]:
                if word == "p":
                    negateP = True
                elif word == "q":
                    negateQ = True
                elif word == "r":
                    negateR = True
                negationStack.pop() 
        elif word in connectives: 
            connectivesUsed.append(word)
            if word == "~":
                negationStack.append(True)
        elif word in matchingBrackets.keys() or word in matchingBrackets.values():
            if word in matchingBrackets.keys():
                if words[index + 1] in connectives and words[index + 1] != "~":
                    print("Invalid Statement: Connective cannot follow an Open Parenthesis.") #this solves issues like ( p ( ^ q ))
                    valid = False
                    return
            if word in matchingBrackets.values():
                if words[index - 1] in connectives:
                    print("Invalid Statement: Closed Parenthesis cannot be preceeded by a connective.") #this solves issues like ( p ^ ) q 
                    valid = False
                    return
        else:
            print("Invalid Statement: Invalid syntax detected. due to " + word)
            valid = False
            return
        
    wordList = [word for word in words if word not in matchingBrackets.keys() and word not in matchingBrackets.values()]
    #copy of the list of words
    #this makes sure checking of adjacent variables and connectives will go smoothly
    # this allows ( ( ) ^ q ) and ( ( q ) q ) to be checked properly
    #only removes from the copy
    # also allows instances like ( ) to be marked as invalid
    
    if len(wordList) == 0:
        print("Invalid Statement: no variables or connectives detected")
        valid = False
        return
    # handles "( )" and other empty inputs
    
    if len(wordList) == 1 and wordList[0] in connectives:
        print("Invalid Statement: cannot evaluate a connective by itself")
        valid = False
        return
    # handles input that is just one connective

    # To check syntax for adjacent variables and connectives 
    for word1, word2 in zip(wordList, wordList[1:]):
        if word1 in vars and word2 in vars:
            print("Invalid Statement: Two variables cannot be adjacent.") # handles inputs like " p p ^ p "
            valid = False
            return
        if word1 in connectives and word2 in connectives and word2 != "~":
            print("Invalid Statement: Two connectives cannot be adjacent.") #handles inputs like " p ^ v p"
            valid = False
            return
        if wordList[-1] in connectives:
            print("Invalid Statement: The last word cannot be a connective.") # handles inputs like " p ^ "
            valid = False
            return
        if wordList[0] in connectives and wordList[0] != "~":
            print("Invalid Statement: The first word cannot be a connective.") # handles inputs like " ^ p"
            valid = False
            return

    if valid:
        uniqueVars = set(variables)  # Remove duplicates from vars
        varPopulator(len(uniqueVars)) 
        return True
        
def varPopulator(n):
    global rowCount 
    rowCount = 2 ** n    # Number ng row sa truth table...tama tong formula dbaaaaaaaa 2^n?

    if n == 3:
        for i in range(rowCount): # alam niyo na to from 0 to 7 kung n = 3 and rowCount is 8
            firstVar.append("True" if (i // 4) % 2 == 0 else "False")  # nakafloor division yan ha...ieevaluate lang kung true or false tas iaappend sa first var and same din sa iba 
            secondVar.append("True" if (i // 2) % 2 == 0 else "False") # wag ko na explain ha, alam kong magaling kayo
            thirdVar.append("True" if i % 2 == 0 else "False")      

    elif n == 2:
        for i in range(rowCount):
            firstVar.append("True" if (i // 2) % 2 == 0 else "False") 
            secondVar.append("True" if (i % 2) == 0 else "False") 

    elif n == 1: #prinepare ko na to para sa mga kupal na mag-eenter ng p and not p etc
        for i in range(rowCount):
            firstVar.append("True" if (i % 2) == 0 else "False")  

    calculateNegations()

def calculateNegations():
    global negationFirstVar, negationSecondVar, negationThirdVar
    # If P is negated, create a list of the opposite values of P (True becomes False and vice versa) same for Q and R. basta awaten u lattan
    negationFirstVar = ["False" if temp == "True" else "True" for temp in firstVar] if negateP else []
    negationSecondVar = ["False" if temp == "True" else "True" for temp in secondVar] if negateQ else []
    negationThirdVar = ["False" if temp == "True" else "True" for temp in thirdVar] if negateR else []

def extractPropositions(statement):

    print(statement)#test
    propositions = set()
    subStatements = []
    stackOpenBracket = []

    for index, char in enumerate(statement):
        if char.isalpha() and char != 'v':
            propositions.add(char)

        if char in openBrackets:
            stackOpenBracket.append((char, index)) # If open parentheses siya, ilalagay sa stack yung parentheses at yung index bale kung ( p v r) v q 
                                                   # Unang parenthesis na maencounter is nakastore sa stack na parang [ ( '(' , 0 ) ] since zero yung index

        elif char in closeBrackets:

            if stackOpenBracket: #kung may laman

                latestOpenBracket, start = stackOpenBracket.pop() #kukunin niya yung latest na bracket na nasa top at yung index since two ang value ang nkstore sa stack

                if matchingBrackets[latestOpenBracket] == char: #yung char dito is yung current CLOSING bracket - titignan lang kung kamatch ng open yung close na bracket
                    subStatements.append(statement[start : index + 1]) #if oo, iadd niya sa substatement from sa index ng latest open bracket to the current index which is index ng closing bracket 

    subStatements.append(statement)
    return sorted(propositions), subStatements #sorted para magreturn as list yung propositions 

def evaluateStatement(subStatements, variables):
    results = [[] for _ in subStatements] #magcrecreate ng empty list for every substatements para sa mga results nila

    for i in range(rowCount): 
        if rowCount == 8:
            rowValues = {variables[0]: firstVar[i], variables[1]: secondVar[i], variables[2]: thirdVar[i]}  

        if rowCount == 4:
            rowValues= {variables[0]: firstVar[i], variables[1]: secondVar[i]}

        if rowCount == 2:
            rowValues = {variables[0]: firstVar[i]}

        for index, subStatement in enumerate(subStatements):
            evaluatedResult = evalProposition(subStatement, rowValues) 
            results[index].append(evaluatedResult)

    printFinalTable(results, subStatements, variables)

def evalProposition(subStatement, rowValues):

    if 'r' in rowValues:
        subStatement = subStatement.replace("r", rowValues['r'])
        # key r will be evaluated first and will be replaced by corresponding value
        # if otherwise, p and q which truth values happen to be True will have it's r be replaced with r's value
        # leading to errors such as TTrueue and TFalseue
        
    if 'p' in rowValues:
        subStatement = subStatement.replace("p", rowValues['p'])
    
    if 'q' in rowValues:
        subStatement = subStatement.replace("q", rowValues['q'])
    

    subStatement = subStatement.replace("~", " not ").replace("^", " and ").replace("v", " or ")
    subStatement = subStatement.replace("<->", " is ").replace("->", " <= ")

    return str(eval(subStatement)) #error sa boolean output try niyo nga lagyan ng try and exception para mas specific yung error diko madebug


def printFinalTable(results, subStatements, variables):

    #pagprint ng mga header lang
    if rowCount == 8:
        print(f"{variables[0]:<10} {variables[1]:<10} {variables[2]:<10}", end=" ")

    elif rowCount == 4:
        print(f"{variables[0]:<10} {variables[1]:<10}", end=" ")
        
    elif rowCount == 2:
        print(f"{variables[0]:<10}", end=" ")

    header = " ".join([f"{sub:<15}" for sub in subStatements])
    print(header)
    
    totalWidth = 10 * (3 if rowCount == 8 else (2 if rowCount == 4 else 1)) + len(header)
    print('-' * totalWidth)

    for i in range(rowCount):
        if rowCount == 8:
            print(f"{firstVar[i]:<10} {secondVar[i]:<10} {thirdVar[i]:<10}", end=" ")
        elif rowCount == 4:
            print(f"{firstVar[i]:<10} {secondVar[i]:<10}", end=" ")
        elif rowCount == 2:
            print(f"{firstVar[i]:<10}", end=" ")

        row = " ".join([f"{results[j][i]:<15}" for j in range(len(subStatements))])
        print(row)
        
# Entry point ng putang-inang user

userInput()
        
