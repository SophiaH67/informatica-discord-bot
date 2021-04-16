from sympy import symbols, Eq, solve
import discord

def floatToString(flt):
    return ('%.15f' % flt).rstrip('0').rstrip('.')

def calculateABC(A, B, C):
    x = symbols('x')
    equation = Eq(A*x**2+B*x+C, 0)
    solutions = solve(equation)
    for solution in solutions:
        if "sympy.core.add.Add" in str(type(solution)):
            return "This formula no workie"
    return " or ".join(floatToString(v) for v in solutions)

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
    e = discord.Embed()
    e.add_field(name="{}x^2 + {}x + {} = 0".format(floatToString(a),floatToString(b),floatToString(c)), value=calculateABC(a,b,c))
    e.color = 0x00FF00
    return e