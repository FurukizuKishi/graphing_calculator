import sys
import subprocess
import Calculation_Process
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, pyqtSignal, pyqtSlot, SIGNAL
import _thread
import threading
import queue
import math
import platform

class Window(QtGui.QMainWindow):
    winX = 48
    winY = 48
    winW = 640
    winH = 480
    def __init__(self, winX, winY, winW, winH, parent = None):
        super(Window, self).__init__(parent)
        self.winW = winW
        self.winH = winH
        self.winTitle = "Calculator"
        self.setGeometry(winX, winY, winW, winH)
        self.setWindowTitle(self.winTitle)
        self.MenuWidgets = []
        self.CalculatorWidgets = []
        self.percent = 0
        self.Equation = ""
        self.CalculatorExpression = ""
        self.expList = [[""]]
        self.Answer = 0
        self.AnswerExpression = ""
        self.GraphWidgets = []
        self.PropertiesWidgets = []
        self.CurveSlots = []
        self.Curve = None
        self.CreatingGraph = False
        self.PropertiesWidgetsCreated = False
        self.BoundsUneven = False
        self.Curves = []
        self.Bounds = []
        self.Menu((self.winW / 2), (self.winH / 3), 128, 64,
            [
                ["Calculator", 0, self.MOVECalculator],
                ["Graph", 0, self.MOVEGraphProperties, [[]]],
                ["Quit", 0, sys.exit],
            ])

    def update(self, e):
        if self.percent == 100:
            self.Curve = DrawCurve(Points, Gradients, Bound, 0, 0, self.winW, self.winH, self)

    def CorrectFontErrors(self, text):
        if platform.system == "Windows" and platform.release in ["10"]:
            return text
        else:
            CharReplace = [
                    [",", ";"],
                    ["\N{MATHEMATICAL ITALIC SMALL X}", "x"],
                    ["\N{MATHEMATICAL ITALIC SMALL Y}", "y"],
                    ["\N{MATHEMATICAL ITALIC SMALL Z}", "z"],
                    ["\N{MATHEMATICAL ITALIC SMALL A}", "a"],
                    ["\N{MATHEMATICAL ITALIC SMALL B}", "b"],
                    ["\N{MATHEMATICAL ITALIC SMALL C}", "c"],
                    ["\N{MATHEMATICAL BOLD SMALL PI}",  "π"],
                    ["\N{MATHEMATICAL BOLD SMALL PHI}", "φ"],
                    ["\N{MATHEMATICAL ITALIC SMALL E}", "e"],
                ]
            for i in range(0, len(CharReplace)):
                text = text.replace(CharReplace[i][0], CharReplace[i][1])
            #print(text)
            return text
    
    def Button(self, x, y, w, h, msg, List, Shown, color, cmd, args = ()):
        if msg == self.CalculatorExpression or msg == self.Answer or color == "equation":
            btn = QtGui.QPushButton("", self)
            lbl = QtGui.QLabel(msg, self)
        else:
            msg = self.CorrectFontErrors(msg)
            btn = QtGui.QPushButton(msg, self)
        if args != ():
            btn.clicked.connect(lambda: cmd(*args))
        else:
            btn.clicked.connect(cmd)
        btn.move(x, y)
        btn.resize(w, h)
        try:
            lbl.move(x+12, y)
            lbl.resize(w-24, h)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            List.append([btn, lbl])
        except:
            List.append([btn])
        if Shown == True:
            btn.show()
            try:
                lbl.show()
            except:
                pass
        if color != "default" and color != "equation":
            btn.setStyleSheet("background-color: " + color);
        btn.setStyleSheet("font-family: arial_unicode_ms")

    def Label(self, x, y, w, h, msg, List):
        lbl = QtGui.QLabel(msg, self)
        lbl.move(x, y)
        lbl.resize(w*2.5, h)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.show()
        List.append([lbl])

    def TextBox(self, x, y, w, h, msg, List):
        box = QtGui.QLineEdit(self)
        lbl = QtGui.QLabel(msg, self)
        box.move(x, y)
        box.resize(w, h)
        box.show()
        lbl.move(x-(w*0.75), y-32)
        lbl.resize(w*2.5, h)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.show()
        List.append([box, lbl])
    
    def SpinBox(self, x, y, w, h, msg, nMin, nMax, List):
        box = QtGui.QSpinBox(self)
        lbl = QtGui.QLabel(msg, self)
        box.move(x, y)
        box.resize(w, h)
        box.show()
        box.setMinimum(nMin)
        box.setMaximum(nMax)
        lbl.move(x-(w*0.75), y-32)
        lbl.resize(w*2.5, h)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.show()
        #print(msg + ":", len(List))
        List.append([box, lbl])

    def UpdateButton(self, x, y, w, h, msg, List, Index, color, cmd, args = ()):
        if msg == self.CalculatorExpression or msg == str(self.Answer) or msg == self.AnswerExpression or color == "equation":
            btn = QtGui.QPushButton("", self)
            lbl = QtGui.QLabel(msg, self)
        else:
            btn = QtGui.QPushButton(msg, self)
        if args != ():
            btn.clicked.connect(lambda: cmd(*args))
        else:
            btn.clicked.connect(cmd)
        List[Index][0] = btn
        btn.move(x, y)
        btn.resize(w, h)
        if msg == self.CalculatorExpression or msg == str(self.Answer) or msg == self.AnswerExpression:
            try:
                List[Index][1].hide()
                List[Index][1] = lbl
                lbl.move(x+16, y)
                lbl.resize(w-16, h) 
                lbl.show()
            except:
                pass
        if color != "default" and color != "equation":
                btn.setStyleSheet("background-color:" + color);
        if "Error" in msg:
            if msg == str(self.Answer):
                try:
                    lbl.setStyleSheet("color: red");
                except:
                    pass
            else:
                btn.setStyleSheet("color: red");
        btn.show()
    
    def Menu(self, x, y, w, h, Buttons):
        self.MenuWidgets = []
        for i in range(0, len(Buttons)):
            Offset = (Buttons[i][1] - 1) * (w / 2)
            try:
                self.Button(x+Offset, y+(i*h), w, h, Buttons[i][0], self.MenuWidgets, True, "default", Buttons[i][2], Buttons[i][3])
            except:
                self.Button(x+Offset, y+(i*h), w, h, Buttons[i][0], self.MenuWidgets, True, "default", Buttons[i][2])
        self.ShowWidgets(self.MenuWidgets)
        self.show()

    def CalculateGraph(self):
        self.expList = [self.Equation]
        self.MOVEGraphProperties(self.expList)
    
    def Calculator(self, Layout):
        gbw = self.winW / len(Layout[1])
        #print(gbw)
        gbh = self.winH / len(Layout)
        for y in range(0, len(Layout)):
            cx = 0
            for x in range(len(Layout[y])):
                bw = int(gbw)
                if Layout[y][x] == " ":
                    bw = int(gbw)
                elif Layout[y][x].count(" ") > 0 or Layout[y][x].count("#") == len(Layout[y][x]):
                    bw = (round((len(Layout[y][x]) - 1) / 3) * gbw)
                if Layout[y][x] != " ":
                    #print(Layout[y][x])
                    if Layout[y][x].count("#") == len(Layout[y][x]):
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, self.CalculatorExpression, self.CalculatorWidgets, True, "default", print, self.CalculatorExpression)
                    elif "GRAPH" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, (Layout[y][x]).replace(" ",""), self.CalculatorWidgets, True, "default", self.CalculateGraph)
                        #print("GRAPH Button")
                    elif "CLOSE" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, (Layout[y][x]).replace(" ",""), self.CalculatorWidgets, True, "default", self.MOVEMenu)
                        #print("CLOSE Button")
                    elif "=" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, (Layout[y][x]).replace(" ",""), self.CalculatorWidgets, True, "default", self.Calculate, (True, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                        #print("EQUATION Button")
                    elif "AC" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, (Layout[y][x]).replace(" ",""), self.CalculatorWidgets, True, "default", self.THREADUpdate, ("AC", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "ROUND" in Layout[y][x]:
                        self.SpinBox(cx, y*gbh+(gbh/2), min(self.winW, bw, self.winW - cx), (gbh/2), "Round to ... d.p.", 0, 10, self.CalculatorWidgets)
                    elif "*" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "×", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("*", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "/" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "÷", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("/", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "^" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL X}" + "\N{SUPERSCRIPT LATIN SMALL LETTER N}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("^", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "|" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "abs", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("A(", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "CALC" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "DIFFERENTIATE", self.CalculatorWidgets, True, "default", self.Differentiate, (0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))               
                    elif "S" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "sin", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("S(", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "C" in Layout[y][x] and not "AC" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "cos", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("C(", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif "T" in Layout[y][x]:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "tan", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("T(", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "!":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL X}" + "!", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("!", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "π":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL BOLD SMALL PI}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("π", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "φ":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL BOLD SMALL PHI}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("φ", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "L":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "log", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("L(", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "E":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "ln", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("E(", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "√":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{SUPERSCRIPT LATIN SMALL LETTER N}" + "\N{SQUARE ROOT}" + "\N{MATHEMATICAL ITALIC SMALL X}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("√x", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "a":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL A}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("a", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "b":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL B}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("b", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "c":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL C}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("c", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "e":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL E}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("e", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "x":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL X}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("x", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                    elif Layout[y][x] == "y":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL Y}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("y", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))               
                    elif Layout[y][x] == "z":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "\N{MATHEMATICAL ITALIC SMALL Z}", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("z", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))               
                    elif Layout[y][x] == "F":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "f(" + "\N{MATHEMATICAL ITALIC SMALL X}" + ")", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))               
                    elif Layout[y][x] == "v":
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, "var", self.CalculatorWidgets, True, "default", self.THREADUpdate, ("", False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))               
                    else:
                        self.Button(cx, y*gbh, min(self.winW, bw, self.winW - cx), gbh, (Layout[y][x]).replace(" ",""), self.CalculatorWidgets, True, "default", self.THREADUpdate, ((Layout[y][x]).replace(" ",""), False, 0, 0, min(self.winW, round((len(Layout[0][0]) - 1) / 3) * gbw), gbh))
                cx += bw
        self.ShowWidgets(self.CalculatorWidgets)

    def Calculate(self, GiveAnswer, x, y, w, h):
        #print("Expression:", self.Equation)
        if self.Equation != "":
            self.Answer = Calculation_Process.Input(self.Equation, "Calculation", [['x', 1], ['y', 2], ['z', 3], ['a', 5], ['b', 10], ['c', 20]])
        if not isinstance(self.Answer, str):
            if self.CalculatorWidgets[40][0].text() == "0":
                self.Answer = int(round(self.Answer, int(self.CalculatorWidgets[40][0].text())))
            else:
                self.Answer = round(self.Answer, int(self.CalculatorWidgets[40][0].text()))
        self.AnswerExpression = self.FormatExpression(str(self.Answer), str(self.AnswerExpression))
        #print("Answer:", self.AnswerExpression)
        #print("")
        self.UpdateExpression("", True, x, y, w, h)

    def Differentiate(self, x, y, w, h):
        #print("Expression:", self.Equation)
        if self.Equation != "":
            self.Answer = Calculation_Process.Input(self.Equation, "Differentiation", [['x', 1], ['y', 2], ['z', 3], ['a', 5], ['b', 10], ['c', 20]])
        self.AnswerExpression = self.Answer
        self.AnswerExpression = self.FormatExpression(str(self.Answer), str(self.AnswerExpression))
        #print("Differential:", self.AnswerExpression)
        #print("")
        self.UpdateExpression("", True, x, y, w, h)

    def THREADUpdate(self, char, GiveAnswer, x, y, w, h):
        self.UpdateExpression(char, GiveAnswer, x, y, w, h)

    def FormatExpression(self, Equation, CalculatorExpression):
        #print("-----------Formatting-----------")
        #print(Equation)
        CalculatorExpression = Equation
        #print(CalculatorExpression)
        Term = ""
        Digits = "0123456789."
        Variables = "πφeabcdefghijklmnopqrstuvwxyz"
        Operators = "+-×÷^"
        Functions = [["S(", "sin("], ["C(", "cos("], ["T(", "tan("], ["L(", "log("], ["E(", "ln("], ["A(", "abs("]]
        Primary = Digits + Variables + "-("
        Precendentary = ")"
        Prohibited = ["√x", "^", "+", "-", "×", "÷"]
        Primary.replace("-", Operators)
        Modulus = False
        InBrackets = False
        Done = False
        for i in range(0, len(Variables)):
            CalculatorExpression = CalculatorExpression.replace("*" + Variables[i], Variables[i])
            CalculatorExpression = CalculatorExpression.replace("*" + "(", "(")
            CalculatorExpression = CalculatorExpression.replace(")" + "*" + "(", ")(")
            CalculatorExpression = CalculatorExpression.replace(Variables[i] + "^0.5", "√" + Variables[i])
        CalculatorExpression = CalculatorExpression.replace("*", "×")
        CalculatorExpression = CalculatorExpression.replace("/", "÷")
        if Term != "^":
            Encapsulations = [["S", "C", "T", "L", "E", "A", "("], [")"]]
            while CalculatorExpression.count("^") > 0:
                index = CalculatorExpression.index("^")
                #print("Index:",index)
                e = ''
                #print("Length:",len(CalculatorExpression))
                for i in range(index+1, len(CalculatorExpression)):
                    if CalculatorExpression[index+1] not in Encapsulations[0]:
                        if CalculatorExpression[i] in ("1234567890." + Variables):
                            e = e + CalculatorExpression[i]
                            #print('e:',e)
                        else:
                            break;
                    else:
                        e = e + CalculatorExpression[i]
                        #print('e:',e)
                        if e[-1] in Encapsulations[1]:
                            break;
                    #print("i:",i)
                #print("")
                eo = e
                if e == '':
                    e = '\N{REPLACEMENT CHARACTER}'
                e = '<sup>' + e + '</sup>'
                #print("New e:",e)
                CalculatorExpression = CalculatorExpression.replace("^"+eo,e)
        for i in range(0, len(Functions)):
            CalculatorExpression = CalculatorExpression.replace("*" + Functions[i][0], Functions[i][0])
            CalculatorExpression = CalculatorExpression.replace(Functions[i][0], Functions[i][1])
        #print("Equation:",Equation)
        #print("Expression:",CalculatorExpression)
        CalculatorExpression = CalculatorExpression.replace('a', '\N{MATHEMATICAL ITALIC SMALL A}')
        CalculatorExpression = CalculatorExpression.replace('b', '\N{MATHEMATICAL ITALIC SMALL B}')
        CalculatorExpression = CalculatorExpression.replace('c', '\N{MATHEMATICAL ITALIC SMALL C}')
        CalculatorExpression = CalculatorExpression.replace('x', '\N{MATHEMATICAL ITALIC SMALL X}')
        CalculatorExpression = CalculatorExpression.replace('y', '\N{MATHEMATICAL ITALIC SMALL Y}')
        CalculatorExpression = CalculatorExpression.replace('z', '\N{MATHEMATICAL ITALIC SMALL Z}')
        CalculatorExpression = CalculatorExpression.replace('e', '\N{MATHEMATICAL ITALIC SMALL E}')
        CalculatorExpression = self.CorrectFontErrors(CalculatorExpression)
        #print("Formatted Expression:", CalculatorExpression)
        #print("---------!Formatting-----------")
        return CalculatorExpression

    def UpdateExpression(self, char, GiveAnswer, x, y, w, h):
        #print("UPDATE")
        self.CalculatorWidgets[0][0].hide()
        Term = ""
        Digits = "0123456789."
        Variables = "πφeabcdefghijklmnopqrstuvwxyz"
        Operators = "+-×÷^"
        Functions = [["S(", "sin("], ["C(", "cos("], ["T(", "tan("], ["L(", "log("], ["E(", "ln("], ["A(", "abs("]]
        Primary = Digits + Variables + "-("
        Precendentary = ")"
        Prohibited = ["√x", "^", "+", "-", "×", "÷"]
        #print(Digits[:-1])
        Function = False
        for i in range(0, len(Functions)):
            if char == Functions[i][0]:
                if len(self.Equation) == 0:
                    Term += char
                elif len(self.Equation) > 1 and ((self.Equation[-2] in Digits[:-1] or self.Equation[-2] in Variables) and (self.Equation[-1] == "*")) or (self.Equation[-1] == "(") or (self.Equation[-1] in "+-*/^"):
                    Term += char
                Function = True
        if Function == False:
            if char == "←":
                self.Equation = self.Equation[:-1]
            elif len(self.Equation) == 0 and char in Primary:
                Term += char
            elif len(self.Equation) > 0:
                #print(self.Equation[-1])
                if char in "+-×÷^" and (self.Equation[-1] in Digits[:-1] or self.Equation[-1] in Variables or self.Equation[-1] in Precendentary):
                    Term += char
                if char in Variables and len(self.Equation) > 1 and ((self.Equation[-2] in Digits[:-1] or self.Equation[-2] in Variables) and (self.Equation[-1] == "*")) or (self.Equation[-1] == "(") or (self.Equation[-1] in Operators):
                    Term += char
                elif char == "√x" and (self.Equation[-1] in Digits[:-1] or self.Equation[-1] in Variables or self.Equation[-1] in Precendentary):
                    Term += "^0.5"
                else:
                    if char not in Prohibited and char not in Variables:
                        Term += char
        self.Equation += Term
        self.CalculatorExpression = self.Equation
        self.CalculatorExpression = self.FormatExpression(self.Equation, self.CalculatorExpression)
        if Term == "AC":
            self.Equation = ""
            self.CalculatorExpression = ""
        self.expList = [[self.Equation]]
        #print("List:",self.expList)
        if GiveAnswer == True:
            self.UpdateButton(x, y, w, h, self.AnswerExpression, self.CalculatorWidgets, 0, "default", print, self.AnswerExpression)
        else:
            self.UpdateButton(x, y, w, h, self.CalculatorExpression, self.CalculatorWidgets, 0, "default", print, (self.Equation, "\n", self.CalculatorExpression))

    def RefreshWidgets(self, List):
        #print(List)
        for i in range(len(List)):
            try:
                List[i][0].update()
                try:
                    List[i][1].update()
                except:
                    pass
            except:
                List[i].update()

    def HideWidgets(self, List):
        #print(List)
        for i in range(len(List)):
            try:
                List[i][0].hide()
                try:
                    List[i][1].hide()
                except:
                    pass
            except:
                List[i].hide()

    def ShowWidgets(self, List):
        #print(List)
        for i in range(len(List)):
            try:
                List[i][0].show()
                try:
                    List[i][1].show()
                except:
                    pass
            except:
                List[i].show()

    def MOVECalculator(self):
        self.Equation = ""
        self.CalculatorExpression = self.Equation
        self.HideWidgets(self.MenuWidgets)
        self.Calculator(
            [
                ["##############################################"],
                ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                ["  +   ", "  -   ", "  *   ", "  /   ", "^", "√"],
                [".", " ", " ", "a", "x", " ", " ", "S", "L", "π"],
                ["|", "(", ")", "b", "y", " ", " ", "C", "E", "e"],
                ["!", " ", " ", "c", "z", " ", " ", "T", " ", "φ"],
                ["   GRAPH   ", "    CALC   ", "   ←  ", "  AC  "],
                ["   ROUND   ", "               =               "],
                ["                   CLOSE                      "],
            ])

    def CreateCurve(self):
        if len(self.Curves) < int(self.PropertiesWidgets[2][0].text()):
            functionText = [["sin", "S"], ["cos", "C"], ["tan", "T"], ["log", "L"], ["ln", "E"], ["abs", "A"]]
            CurveText = self.PropertiesWidgets[0][0].text()
            for i in range(0, len(functionText)):
                CurveText = CurveText.replace(functionText[i][0], functionText[i][1])
            #print(CurveText)
            self.Curves.append(CurveText)
            self.PropertiesWidgets[0][0].setText("")
        #print(self.Curves)
        for i in range(0, 5):
            if i < len(self.Curves):
                self.CurveSlots[i][1].setText(self.FormatExpression(self.Curves[i], self.Curves[i]))
            else:
                self.CurveSlots[i][1].setText(" ")

    def CreateGraph(self):
        self.MOVEGraph(self.Curves, self.PropertiesWidgets[3][0].text(), self.PropertiesWidgets[4][0].text())

    def expressionTextChanged(self):
        if self.CreatingGraph == True:
            if self.PropertiesWidgets[0][0].text() == '':
                self.PropertiesWidgets[1][0].setEnabled(False)
            else:
                self.PropertiesWidgets[1][0].setEnabled(True)

    def valueChanged(self):
        if len(self.Curves) > int(self.PropertiesWidgets[2][0].text()):
            self.Curves = self.Curves[:int(self.PropertiesWidgets[2][0].text())]
        for i in range(0, 5):
            if i < int(self.PropertiesWidgets[2][0].text()):
                self.CurveSlots[i][0].show()
                self.CurveSlots[i][1].show()
            else:
                self.CurveSlots[i][0].hide()
                self.CurveSlots[i][1].hide()

    def graphEnabled(self):
        if self.Curves == [] or self.PropertiesWidgets[3][0].text() == '' or self.PropertiesWidgets[4][0].text() == '' or self.BoundsUneven == True:
            self.PropertiesWidgets[6][0].setEnabled(False)
        else:
            self.PropertiesWidgets[6][0].setEnabled(True)

    def boundTextChanged(self, Bound):
        try:
            if float(Calculation_Process.Input(self.PropertiesWidgets[3][0].text(), "Calculation", [])) >= float(Calculation_Process.Input(self.PropertiesWidgets[4][0].text(), "Calculation", [])):
                self.BoundsUneven = True
                #print("Uneven Bounds")
                if Bound == "Lower":
                    self.PropertiesWidgets[3][0].setStyleSheet("background-color: red")
                    self.PropertiesWidgets[4][0].setStyleSheet("background-color: white")
                elif Bound == "Upper":
                    self.PropertiesWidgets[3][0].setStyleSheet("background-color: white")
                    self.PropertiesWidgets[4][0].setStyleSheet("background-color: red")
            else:
                self.BoundsUneven = False
                #print("Even Bounds")
                self.PropertiesWidgets[3][0].setStyleSheet("background-color: white")
                self.PropertiesWidgets[4][0].setStyleSheet("background-color: white")
        except:
            pass;
        if self.Curves == [] or self.PropertiesWidgets[4][0].text() == '' or self.PropertiesWidgets[4][0].text() == '' or self.BoundsUneven == True:
            self.PropertiesWidgets[6][0].setEnabled(False)
        else:
            self.PropertiesWidgets[6][0].setEnabled(True)
    
    def MOVEGraphProperties(self, Curves):
        self.CreatingGraph = True
        self.HideWidgets(self.CalculatorWidgets)
        self.HideWidgets(self.MenuWidgets)
        if self.PropertiesWidgetsCreated == False:
            self.Curves = Curves
            w = 128
            h = 64
            s = 64
            self.TextBox(64, self.winH - (h * 4.5 + 32), self.winW - 128, 32, "", self.PropertiesWidgets)
            self.Button((self.winW / 2) - (w / 2), self.winH - (h * 3.5 + 32), w, h, "Create Curve", self.PropertiesWidgets, True, "default", self.CreateCurve)
            
            self.SpinBox(s, s, s, 32, "Number of Curves", 1, 5, self.PropertiesWidgets)
            self.TextBox(self.winW - (s * 4), s, s, 32, "Lower Bound", self.PropertiesWidgets)
            self.TextBox(self.winW - (s * 2), s, s, 32, "Upper Bound", self.PropertiesWidgets)
            
            self.PropertiesWidgets[0][0].textChanged.connect(self.expressionTextChanged)
            self.PropertiesWidgets[1][0].clicked.connect(self.graphEnabled)
            self.PropertiesWidgets[2][0].valueChanged.connect(self.valueChanged)
            self.PropertiesWidgets[3][0].textChanged.connect(lambda: self.boundTextChanged("Lower"))
            self.PropertiesWidgets[4][0].textChanged.connect(lambda: self.boundTextChanged("Upper"))
            
            self.Button((self.winW / 2) - (w + 32), self.winH - (h + 64), w, h, "Exit", self.PropertiesWidgets, True, "default", self.MOVEMenu)
            self.Button((self.winW / 2) + 32, self.winH - (h + 64), w, h, "Create Graph", self.PropertiesWidgets, True, "default", self.CreateGraph)
            
            for i in range(0, 5):
                if i < len(self.Curves):
                    self.Button(64, self.winH - (h * 4.5 + (80 + (i * 32))), self.winW - 128, 32, self.FormatExpression(self.Curves[i], self.Curves[i]), self.CurveSlots, False, "equation", print, self.Curves)
                else:
                    self.Button(64, self.winH - (h * 4.5 + (80 + (i * 32))), self.winW - 128, 32, " ", self.CurveSlots, False, "equation", print, self.Curves)
                #print(" - " + str(self.CurveSlots[i]))
            self.CurveSlots[0][0].show()
            self.CurveSlots[0][1].show()
            #print("len:", str(len(self.CurveSlots)))
            
            self.PropertiesWidgets[1][0].setEnabled(False)
            self.PropertiesWidgets[6][0].setEnabled(False)
            if Curves != []:
                self.Curves = Curves
                self.PropertiesWidgets[0][0].setEnabled(False)
                self.PropertiesWidgets[2][0].setEnabled(False)
            else:
                self.PropertiesWidgets[0][0].setEnabled(True)
                self.PropertiesWidgets[2][0].setEnabled(True)
            self.PropertiesWidgetsCreated = True
        else:
            self.PropertiesWidgets[0][0].setText('')
            self.PropertiesWidgets[2][0].setValue(1)
            for i in range(0, 5):
                if i < len(self.Curves):
                    self.CurveSlots[i][0].setText(self.FormatExpression(self.Curves[i], self.Curves[i]))
                else:
                    self.CurveSlots[i][0].setText(" ")
            self.ShowWidgets(self.PropertiesWidgets)
            self.CurveSlots[0][0].show()
            self.CurveSlots[0][1].show()
            self.PropertiesWidgets[1][0].setEnabled(False)
            self.PropertiesWidgets[6][0].setEnabled(False)
            if Curves != []:
                self.Curves = Curves
                self.PropertiesWidgets[0][0].setEnabled(False)
                self.PropertiesWidgets[2][0].setEnabled(False)
            else:
                self.PropertiesWidgets[0][0].setEnabled(True)
                self.PropertiesWidgets[2][0].setEnabled(True)                
        #print("C:", Curves)
    
    def MOVEGraph(self, Curves, lBound, uBound):
        self.CreatingGraph = False
        self.HideWidgets(self.CalculatorWidgets)
        self.HideWidgets(self.PropertiesWidgets)
        self.HideWidgets(self.CurveSlots)
        self.HideWidgets(self.MenuWidgets)
        if Curves == []:
            for i in range(0, int(input("How many curves do you want to graph? "))):
                Curves.append(input("Curve " + str(i+1) + ": "))
        else:
            if '' in Curves:
                Curves = [self.Equation]
        #print(Curves)
        #print(self.Curves)
        #print("Equation:",self.Equation)
        #print("Curves:",Curves)
        Bound = [str(lBound), str(uBound)]
        if Bound[0] == "0" and Bound[1] == "0":
            Bound[0] = input("Lower Bound: ")
            Bound[1] = input("Upper Bound: ")
        #print("Given Bounds:", Bound)
        for i in range(0, len(Bound)):
            Bound[i] = Bound[i]
            r = int(Calculation_Process.Input(Bound[i], "Calculation", []))
            Bound[i] = r
        #print("Calculated Bounds:", Bound)
        self.bar = []
        for i in range(0, len(Curves)):
            self.bar.append(QtGui.QProgressBar(self))
            w = 48
            h = (self.winH - (w * 2)) / len(Curves)
            self.bar[i].setGeometry(48, (self.winH - 48) - ((i + 1) * h), w, h)
            self.bar[i].setOrientation(QtCore.Qt.Vertical)
            self.bar[i].show()
            self.bar[i].setValue(self.percent)
        GraphQueue = queue.Queue()
        self.THREADGraph = threading.Thread(target = self.Graph, args = (Curves, Bound, GraphQueue))
        self.THREADGraph.start()
        while self.percent < 100 and i < len(Curves):
            QtGui.QApplication.processEvents()
            pass
        values = GraphQueue.get()
        self.Curve = DrawCurve(values[0], values[1], Bound, 0, 0, self.winW, self.winH, self)

    def MOVEMenu(self):
        self.HideWidgets(self.CalculatorWidgets)
        self.HideWidgets(self.PropertiesWidgets)
        self.HideWidgets(self.CurveSlots)
        self.HideWidgets(self.GraphWidgets)
        self.Curves = []
        for i in range(0, len(self.CurveSlots)):
            self.CurveSlots[i][1].setText(" ")
        self.Menu((self.winW / 2), (self.winH / 3), 128, 64,
            [
                ["Calculator", 0, self.MOVECalculator],
                ["Graph", 0, self.MOVEGraphProperties, [[]]],
                ["Quit", 0, sys.exit],
            ])

    def SetBar(self, n, e):
        self.percent += 100 / self.winW
        self.bar[n].setValue(self.percent)
        
    def Graph(self, Expression, Bound, Queue):
        Points = []
        Gradients = []
        for i in range(0, len(Expression)):
            self.percent = 0
            Points.append([])
            dydx = Calculation_Process.Input(Expression[i], "Differentiation", [['x', 0]])
            ##print("y:", Expression[i])
            ##print("dy/dx:", dydx)
            ##print("")
            for x in range(0, self.winW+1):
                ##print(Expression[i])
                y = Calculation_Process.Input(Expression[i], "Calculation",
                    [
                        ['x', Bound[0]+((Bound[1]-Bound[0])*(x/self.winW))],
                    ])
                if y != "ERROR" and "Error" not in dydx:
                    ##print(dydx)
                    m = Calculation_Process.Input(str(dydx), "Calculation",
                        [
                            ['x', Bound[0]+((Bound[1]-Bound[0])*(x/self.winW))],
                        ])
                    #print(Expression[i] + ":", str(y), str(m), str(round(self.percent, 3)) + "%")
                    Gradients.append(m)
                else:
                    #print(Expression[i] + ":", str(y), str(round(self.percent, 3)) + "%")
                    continue;
                ##print(Bound[0]+((Bound[1]-Bound[0])*(x/self.winW)))
                ##print("")
                Points[i].append([x, y, [Bound[0]+((Bound[1]-Bound[0])*(x/self.winW))]])
                self.SetBar(i, Expression)
        for i in range(0, len(Expression)): 
            self.bar[i].hide()
        ##print("")
        Queue.put((Points, Gradients))
        btn = self.Button(0, 0, 48, 32, "CLOSE", self.GraphWidgets, True, "default", self.MOVEMenu)

class DrawCurve(QtGui.QWidget):
    Points = []
    Bound = [0, 0]
    winX = 48
    winY = 48
    winW = 640
    winH = 480
    def __init__(self, Points, Gradients, Bound, winX, winY, winW, winH, parent):
        super(DrawCurve, self).__init__(parent)
        self.setGeometry(winX, winY, winW, winH)
        self.setWindowTitle("Graph")
        self.winW = winW
        self.winH = winH
        self.winX = winX
        self.winY = winY
        self.Points = Points
        self.Bound = Bound
        self.initUI()
        self.show()

    def initUI(self):
        btn = QtGui.QPushButton('Exit', self)
        btn.clicked.connect(self.appRestart)
        btn.resize(128, 64)
        btn.move(16, 16)
        btn.show()
    
    def appRestart(self):
        #os.system("Menu.py 1")
        new = subprocess.Popen(['Menu.py', 'htmlfilename.htm'], shell = True)
        sys.exit()

    def paintEvent(self, e):
        #print("...")
        #print("")
        #print("Bound:", self.Bound)
        Line = QtGui.QPainter()
        Line.begin(self)
        axis_pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        Line.setPen(axis_pen)
        y_values = []
        for i in range(0, len(self.Points)):
            for ii in range(0, len(self.Points[i])):
                if "Error" not in str(self.Points[i][ii][1]):
                    if isinstance(self.Points[i][ii][1], str):
                        if sum(i.count(".") for i in str(self.Points[i][ii][1])) > 0:
                            y_values.append(float(self.Points[i][ii][1]))
                        else:
                            y_values.append(int(self.Points[i][ii][1]))
                    else:
                        y_values.append(self.Points[i][ii][1])
        min_y = min(y_values)
        max_y = max(y_values)
        #print("Min:", min_y)
        #print("Max:", max_y)
        if self.Bound[0] <= 0 and self.Bound[1] >= 0:
            i = (0 - self.Bound[0]) / (self.Bound[1] - self.Bound[0]) * self.winW
            #print("Y Axis:", i)
            Line.drawLine(i, 0, i, self.winH)
        x_axis = ((max_y)/(max_y-min_y))*self.winH
        #print("X Axis:", x_axis)
        Line.drawLine(0, x_axis, self.winW, x_axis)
        curve_pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        Line.setPen(curve_pen)
        ##print('\n' * 99)
        for i in range(0, len(self.Points)):
            for ii in range(0, len(self.Points[i])-1):
                ##print(self.Points[i])
                try:
                    Line.drawLine(ii*(self.winW/(len(self.Points[i]))), ((max_y-self.Points[i][ii][1])/(max_y-min_y))*self.winH, (ii+1)*(self.winW/(len(self.Points[i]))), ((max_y-self.Points[i][ii+1][1])/(max_y-min_y))*self.winH)
                except:
                    pass
        self.show()
        Line.end()

class SubWindow(QtGui.QMainWindow):
    def __init__(self):
        pass

def main():
    #print(threading.enumerate())
    app = QtGui.QApplication(sys.argv)
    font = QtGui.QFont("Lucida Sans Unicode")
    app.setFont(font)
    winW = 480
    winH = 640
    winX = 48
    if winW <= app.desktop().screenGeometry().width():
        winX = (app.desktop().screenGeometry().width() / 2) - (winW / 2)
    winY = 48
    if winH <= app.desktop().screenGeometry().height():
        winY = (app.desktop().screenGeometry().height() / 2) - (winH / 2)
    MainWindow = Window(winX, winY, winW, winH)
    sys.exit(app.exec_())

main()
