class Variable():
    Alias = ""
    Value = 0
    def __init__(self, Alias, Value):
        self.Alias = Alias
        self.Value = Value

var_Pi = Variable("π", 3.14159265359)
var_GR = Variable("φ", 1.61803398875)
var_Ex = Variable("e", 2.71828182846)

presetVariables = [var_Pi, var_GR, var_Ex]
customVariables = []
