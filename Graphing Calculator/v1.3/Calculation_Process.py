import copy
import math
import Variables

def StringScroll(string, index, prompt, part, backwards = False):
    offset = 1
    br_char = ['(', ')']
    if backwards == True:
        offset = -1
        br_char = [')', '(']
    if string[index] == br_char[0]:
        br_count = 1
        Done = False
        variable = string[index]
        while Done == False:
            index = index + offset
            if string[index] == br_char[0]:
                br_count += 1
            elif string[index] == br_char[1]:
                br_count -= 1
            #print("BRC:",br_count)
            variable = variable + string[index]
            if br_count == 0:
                Done = True
            #print(index)
    else:
        variable = string[index]
        Done = False
        while Done == False:
            index = index + offset
            try:
                if part != '':
                    if part[0] != '*':
                        if string[index] in "+-*/" or index < 0:
                            Done = True
                        else:
                            variable = variable + string[index]
                    else:
                        if string[index] in "+*/" or index < 0:
                            Done = True
                        else:
                            variable = variable + string[index]
                else:
                        if string[index] in "+-*/" or index < 0:
                            Done = True
                        else:
                            variable = variable + string[index]
            except:
                Done = True
            #print(index)
    if backwards == True:
        variable = variable[::-1]
    if part != '':
        variable = "(" + variable + part + ")"
    #print(prompt + ":", variable)
    return [variable, index]

#Input("x^4+x^3+x^2+x^1", "Differentiation", [['x', 0]])
#Input("(x-2)*(x-2)^2", "Differentiation", [['x', 0]])
#Input("3*x^2", "Differentiation", [['x', 0]])
#StringScroll("(x-2)*(x-2)^23", 12, "VAR", '', False)

def Differentiation(e, var):
    try:
        #print("e:", e)
        ComplexDiff = [
                        ["S(k*x)", "k*C(k*x)"],
                        ["C(k*x)", "-k*S(k*x)"],
                        ["T(k*x)", "k/C(k*x)"],
                        ["e^(k*x)", "k*e^(k*x)"],
                        ["E(k*x)", "1/x"],
                    ]
        for x in range(0, len(e)):
            for y in range(0, len(e[x])):
                if not isinstance(e[x][y], str):
                    e[x][y] = str(e[x][y])
        n = e[0].count('^')
        #print(n)
        e = ''.join(e[0])
        eo = e
        ind_list = []
        for i in range(0, n):
            ind_list.append(['', '', ''])
            index = eo.index('^')
            n_index = index - 1
            scroll = StringScroll(eo, n_index, "VAR", '', True)
            ind_list[i][1] = scroll[0]
            n_index = scroll[1]
            p_index = n_index
            n_index = index + 1
            try:
                scroll = StringScroll(eo, n_index, "IND", '-1', False)
                ind_list[i][2] = scroll[0]
                scroll = StringScroll(eo, n_index, "IND", '', False)
                placeholder = scroll[0]
                size = index + (len(placeholder) + 1)
            except:
                pass;
            try:
                Multiplication = False
                #print(eo[p_index])
                if eo[p_index-1] == '*':
                    Multiplication = True
                    p_index -= 2
                elif eo[p_index] == '*':
                    Multiplication = True
                    p_index -= 1
                if Multiplication == True:
                    scroll = StringScroll(eo, p_index, "COF", '*'+placeholder, True)
                    ind_list[i][0] = scroll[0]
                else:
                    ind_list[i][0] = placeholder
            except:
                pass;
            #print(ind_list)
            eo = eo[size:]
            #print(size)
            #print("")
        e = ''
        for i in range(0, len(ind_list)):
            e = e + str(Input(ind_list[i][0], "Calculation", [[]])) + '*' + ind_list[i][1] + '^' + str(Input(ind_list[i][2], "Calculation", [[]]))
            if i < len(ind_list) - 1:
                e = e + '+'
            #print(e)
        #print(var)
        for i in range(0, len(var)):
            e = e.replace("^1", "")
            e = e.replace("*" + var[i][0] + "^0", "")
            e = e.replace(var[i][0] + "^0", "1")
        return e
    except:
        return [["ERROR", "Differentiation Error"]]

#Calculate
def Calculation(e):
    #print("e:",e)
    #print("pre-res:", e)
    Operators = [
        [Indices, O_Indices, "^", "I"],
        [Division, O_Division, "/", "D"],
        [Multiplication, O_Multiplication, "*", "M"],
        [Addition, O_Addition, "+", "A"],
        [Subtraction, O_Subtraction, "-", "S"],
                 ]
    for m in range(0, 2):
        for n in range(0, 5):
            if m == 0:
                if sum(i.count(Operators[n][2]) for i in e) > 0 and e[0][0] != "ERROR":
                    #print(Operators[n][3])
                    e = Operators[n][0](e)
                    #print(Operators[n][3] + ":", e)
                elif e[0][0] == "ERROR":
                    return e[0][1]
            else:
                e = Operators[n][1](e)
    if e[0][0] == "ERROR" or isinstance(e[0][0], str):
        return e[0][1]
    else:
        res = e
        #print("RTRN:", e[0][0])
        return e[0][0]

#I - Indices
def Indices(e):
    #Inside
    for i in range(0, len(e)):
        while e[i].count("^") > 0:
            try:
                ii = e[i].index('^')
                e[i][ii] = e[i][ii-1] ** e[i][ii+1]
                del e[i][ii-1]
                del e[i][ii]
            except:
                e = [["ERROR", "Syntax Error"]]
    return e
def O_Indices(e):
    #Outside
    ic = e.count(["^"])
    for i in range(ic):
        i = e.index(['^'])
        try:
            e[i][0] = e[i-1][0] ** e[i+1][0]
            del e[i-1]
            del e[i]
        except:
            e = [["ERROR", "Syntax Error"]]
    return e

#D - Division
def Division(e):
    #Inside
    for i in range(0, len(e)):
        while e[i].count("/") > 0:
            try:
                ii = e[i].index('/')
                if e[i][ii+1] != 0:
                    e[i][ii] = e[i][ii-1] / e[i][ii+1]
                    del e[i][ii-1]
                    del e[i][ii]
                else:
                    e = [["ERROR", "Divide by Zero Error"]]
            except:
                e = [["ERROR", "Syntax Error"]]
    return e
def O_Division(e):
    #Outside
    ic = e.count(["/"])
    for i in range(ic):
        i = e.index(['/'])
        try:
            if e[i+1][0] != 0:
                e[i][0] = e[i-1][0] / e[i+1][0]
                del e[i-1]
                del e[i]
            else:
               e = [["ERROR", "Divide by Zero Error"]] 
        except:
            e = [["ERROR", "Syntax Error"]]
    return e

#M - Multiplication
def Multiplication(e):
    #Inside
    for i in range(0, len(e)):
        while e[i].count("*") > 0:
            try:
                ii = e[i].index('*')
                if isinstance(e[i][ii+1], int) or isinstance(e[i][ii+1], float):
                    e[i][ii] = e[i][ii-1] * e[i][ii+1]
                    del e[i][ii-1]
                    del e[i][ii]
                else:
                    return [["ERROR", "Syntax Error"]]
            except:
                e = [["ERROR", "Syntax Error"]]
    return e
def O_Multiplication(e):
    #Outside
    ic = e.count(["*"])
    for i in range(ic):
        try:
            i = e.index(['*'])
            e[i][0] = e[i-1][0] * e[i+1][0]
            del e[i-1]
            del e[i]
        except:
            e = [["ERROR", "Syntax Error"]]
    return e

#A - Addition
def Addition(e):
    #Inside
    for i in range(0, len(e)):
        while e[i].count("+") > 0:
            try:
                ii = e[i].index('+')
                e[i][ii] = e[i][ii-1] + e[i][ii+1]
                del e[i][ii-1]
                del e[i][ii]
            except:
                e = [["ERROR", "Syntax Error"]]
    return e
def O_Addition(e):
    #Outside
    ic = e.count(["+"])
    for i in range(ic):
        try:
            i = e.index(['+'])
            e[i][0] = e[i-1][0] + e[i+1][0]
            del e[i-1]
            del e[i]
        except:
            e = [["ERROR", "Syntax Error"]]
    return e

#S - Subtraction
def Subtraction(e):
    #Inside
    for i in range(0, len(e)):
        while e[i].count("-") > 0:
            try:
                ii = e[i].index('-')
                e[i][ii] = e[i][ii-1] - e[i][ii+1]
                del e[i][ii-1]
                del e[i][ii]
            except:
                e = [["ERROR", "Syntax Error"]]
    return e
def O_Subtraction(e):
    #Outside
    ic = e.count(["-"])
    for i in range(ic):
        try:
            i = e.index(['-'])
            e[i][0] = e[i-1][0] - e[i+1][0]
            del e[i-1]
            del e[i]
        except:
            e = [["ERROR", "Syntax Error"]]
    return e

#F - Functions
def Functions(e):
    #print("F")
    #Inside
    Functions = [
        ["S", math.radians, math.sin],
        ["C", math.radians, math.cos],
        ["T", math.radians, math.tan],
        ["L", math.log10],
        ["E", math.log1p],
        ["A", abs],
        ["!", math.factorial],
        ]
    #print(e)
    for i in range(0, len(e)):
        for f in range(0, len(Functions)):
            #print(Functions[f][0])
            #print(e)
            while e[i].count(Functions[f][0]) > 0:
                ii = e[i].index(Functions[f][0])
                for p in range(1, len(Functions[f])):
                    if Functions[f][0] == "T":
                        if (e[i][ii+1] - 90) % 90 == 0:
                            return [["ERROR", "Complex Error"]]
                    if Functions[f][0] == "E":
                        e[i][ii+1] = e[i][ii+1] - 1
                    try:
                        if Functions[f][0] == "!":
                            e[i][ii-1] = Functions[f][p](e[i][ii-1])
                        else:
                            e[i][ii+1] = Functions[f][p](e[i][ii+1])
                    except:
                        pass;
                    #print(str(p) + (" " * p), end = "")
                    #print(e[i][ii+1], end = "\n")
                #print(e)
                del e[i][ii]
    return e

#B - Brackets
def Brackets(e):
    e_temp = e
    for x in range(len(e)):
        for y in range(len(e[x])):
            if isinstance(e[x][y], int) or isinstance(e[x][y], float):
                #print("1a. PRV:", e)
                e[x][y] = str(e[x][y])
                #print("1b. PST:", e)
    for x in range(len(e_temp)):
        for y in range(len(e_temp[x])):
            if isinstance(e_temp[x][y], int) or isinstance(e[x][y], float):
                #print("2a. PRV:", e)
                e_temp[x][y] = str(e_temp[x][y])
                #print("2b. PST:", e)
    digits = "0123456789."
    for x in range(len(e_temp)):
        y = 0
        while y < len(e_temp[x]):
            digits.split()
            if y > 0:
                operators = "+-*/^()"
                if e_temp[x][y] not in operators:
                    if y < len(e_temp[x]) - 1:
                        digits.join('')
                        if e_temp[x][y+1] in digits:
                            e_temp[x][y] = e_temp[x][y] + e_temp[x][y+1]
                            del e_temp[x][y+1]
                        else:
                            try:
                                if sum(i.count(".") for i in e_temp[x][y]) > 0:
                                    e_temp[x][y] = float(e_temp[x][y])
                                else:
                                    e_temp[x][y] = int(e_temp[x][y])
                            except:
                                pass
                            y += 1
                    else:
                        try:
                            if sum(i.count(".") for i in e_temp[x][y]) > 0:
                                e_temp[x][y] = float(e_temp[x][y])
                            else:
                                e_temp[x][y] = int(e_temp[x][y])
                        except:
                            pass
                        y += 1
                else:
                    y += 1
            else:
                operators = "+*/^()"
                #print("0a. STR:", e_temp)
                if e_temp[x][y] not in operators:
                    if y < len(e_temp[x]) - 1:
                        #print("0b. STR:", e_temp)
                        digits.join('')
                        if e_temp[x][y+1] in digits:
                            #print("0c. STR:", e_temp)
                            e_temp[x][y] = e_temp[x][y] + e_temp[x][y+1]
                            del e_temp[x][y+1]
                        else:
                            #print("0d. STR:", e_temp)
                            try:
                                if sum(i.count(".") for i in e_temp[x][y]) > 0:
                                    e_temp[x][y] = float(e_temp[x][y])
                                else:
                                    e_temp[x][y] = int(e_temp[x][y])
                            except:
                                pass
                            y += 1
                    else:
                        try:
                            #print("0ei. STR:", e_temp)
                            if sum(i.count(".") for i in e_temp[x][y]) > 0:
                                e_temp[x][y] = float(e_temp[x][y])
                            else:
                                e_temp[x][y] = int(e_temp[x][y])
                            #print("0e2. STR:", e_temp)
                        except:
                            pass
                        y += 1
                else:
                    y += 1
    #print("1. STR:", e_temp)
    e = e_temp
    if sum(i.count("(") for i in e_temp) == sum(i.count(")") for i in e_temp):
        if sum(i.count("(") for i in e_temp) > 0:
            BracketBegin = [-1, -1]
            BracketEnd = [-1, -1]
        while sum(i.count(")") for i in e_temp) > 0:
            #print("")
            for x in range(len(e_temp)):
                #print("Length:", len(e_temp[x]))
                #print("y:", end = " ")
                for y in range(len(e_temp[x])):
                    #print(y, end = "")
                    if e_temp[x][y] == "(":
                        BracketBegin = [x, y]
                        #print("B", end = "")
                    elif e_temp[x][y] == ")":
                        BracketEnd = [x, y]
                        #print("E", end = "")
                        break;
                    #print("", end = " ")
                #print("\n" * 0)
            #print("[" + str(BracketBegin[0]), str(BracketBegin[1]) + "] [" + str(BracketEnd[0]), str(BracketEnd[1]) + "]")
            #print(e_temp[BracketBegin[0]][BracketBegin[1]] + "..." + e_temp[BracketEnd[0]][BracketEnd[1]])
            eu = e_temp[BracketBegin[0]][BracketBegin[1]:BracketEnd[1]+1]
            #print("1. eu:",eu)
            eu.remove("(")
            #print("1a. eu:",eu)
            eu.remove(")")
            #print("1b. eu:",eu)
            eu = [eu]
            #print("2. eu:",eu)
            #print("3. e_temp:",e_temp)
            eo = copy.deepcopy(eu)
            #print("4. eu:",eu)
            #print("5. eo:",eo)
            for i in range(0, len(eo[0])):
                if isinstance(eo[0][i], int):
                    eo[0][i] = str(eo[0][i])
            #print("6. eu:",eu)
            #print("7. eo:",eo)
            try:
                eo = "".join(eo[0])
            except:
                pass;
            #print("8. ej:",eo)
            res = eu[0][0]
            #print(res)
            try:
                res = Calculation(eu)
            except:
                pass;
            #print("res:", res)
            del e_temp[0][BracketBegin[1]:BracketEnd[1]+1]
            e_temp[0].insert(BracketBegin[1], res)
        else:
            pass;
        #print("brac:", e_temp)
        try:
            e = Functions(e_temp)
        except:
            return "Math Domain Error"
        #print("func:", e)
        res = Calculation(e)
        #print("calc:", res)
        return res
    else:
        #print("[ERROR]: Invalid expression - Imbalanced brackets.")
        return "Parse Error"

def Input(Expression, Mode, var):
    #print("Input your equation. Always space the elements amongst the operators.")
    #Input equation.
    #print(Expression)
    if Expression[0] == "-":
        Expression = "0" + Expression
    Replacements = [["--", "+"], ["++", "+"], ["+-", "-"], ["-+", "-"]]
    for i in range(0, len(Replacements)):
        try:
            Expression = Expression.replace(Replacements[i][0], Replacements[i][1])
        except:
            pass;
    #print(Expression)
    #Split the expression into the individual elements.
    expList = Expression.split()

    #Split the elements in a personal list.
    for i in range(0, len(expList)):
        expList[i] = list(expList[i])

    #Add preset variables.
    for i in range(0, len(Variables.presetVariables)):
        var.append([Variables.presetVariables[i].Alias, Variables.presetVariables[i].Value])

    #Create new variables.
    try:
        if Mode == "Calculation":
            for v_i in range(0, len(var)):
                for i in range(0, len(expList)):
                    for ii in range(0, len(expList[i])):
                            #print(i, ii, v_i)
                            #print(expList[i][ii], var[v_i])
                            if expList[i][ii] == var[v_i][0]:
                                expList[i][ii] = var[v_i][1]
    except:
        pass;
    for i in range(len(expList)):
        for j in range(len(expList[i])):
            expList[i][j] = str(expList[i][j])

    #print("Combination:")
    #Combine the individual figures into numbers.
    for i in range(0, len(expList)):
        #Search through the personal lists.
        o = 0
        for j in range(len(expList[i])):
            #print(expList[i][j-o], "(" + str(i) + ",", str(j) + ",", str(o) + ")")
            NegativeForebears = ["(", "*", "/", "^"]
            if any(char.isdigit() for char in expList[i][j-o]) == True or (expList[i][j-o] == "-" and j == 0) or (expList[i][j-o-1] in NegativeForebears and expList[i][j-o] == "-"):
                if j-o+1 < len(expList[i]):
                    if expList[i][j-o+1] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}:
                        expList[i][j-o] = str(expList[i][j-o]) + str(expList[i][j-o+1])
                        del expList[i][j-o+1]
                        #print(expList)
                        o += 1
                    else:
                        if j-o == len(expList[i]) - 1:
                            break;

    #Convert all numbers in the list to integers.
    for i in range(0, len(expList)):
        for j in range(0, len(expList[i])):
            try:
                if sum(i.count(".") for i in str(expList[i][j])) > 0:
                    expList[i][j] = float(expList[i][j])
                    #print("FLT:", expList)
                else:
                    expList[i][j] = int(expList[i][j])
                    #print("INT:", expList)
            except ValueError:
                pass
    if Mode == "Calculation":
        expList = Brackets(expList)
        #print("l:", expList)
    elif Mode == "Differentiation":
        v = []
        for i in range(0, len(var)):
            v.append(var[i])
        expList = Differentiation(expList, v)
    try:
        if (isinstance(expList, complex) or ((any(char.isdigit() for char in expList) == False) and "Error" not in expList)):
            #print("[ERROR]:", expList, "is not a real number.")
            expList = "Complex Error"
    except:
        pass
    if isinstance(expList, float):
        if expList.is_integer():
            expList = int(expList)
    #print(expList)
    return expList

#Input("-10", "Calculation", [])
Input("0.5*L(200*3.1415927)+100*(L(100)-L(e))", "Differentiation", [['x', 0]])
