from sympy import symbols, Eq, solve


def calculateABC(A, B, C):
    x = symbols('x')
    equation = Eq(A*x**2+B*x+C, 0)
    return " or ".join(('%.15f' % v).rstrip('0').rstrip('.') for v in solve(equation))

def get_aliases():
    return ["calculateabc"]

def run(args, bot):
    try:
        a = float(args[0])
    except:
        return "a is not a correct number"

    try:
        b = float(args[1])
    except:
        return "b is not a correct number"

    try:
        c = float(args[2])
    except:
        return "c is not a correct number"

    return "```{}```".format(calculateABC(a,b,c))