from sympy import symbols, Eq, solve, core
from discord.ext import commands
from discord import Embed

def floatToString(flt):
    return ('%.15f' % flt).rstrip('0').rstrip('.')

def calculateABC(A, B, C):
    x = symbols('x')
    equation = Eq(A*x**2+B*x+C, 0)
    solutions = solve(equation)
    for solution in solutions:
        if not type(solution) is core.numbers.Float:
            return "This formula no workie"
    return " or ".join(floatToString(v) for v in solutions)


@commands.command(name="abc", aliases=["abcformula","calculate","solve"], help="Calculates quadratic formula")
async def run(ctx, A,B,C):
    try:
        a = float(A)
    except:
        return await ctx.send("a is not a correct number")

    try:
        b = float(B)
    except:
        return await ctx.send("b is not a correct number")

    try:
        c = float(C)
    except:
        return await ctx.send("c is not a correct number")
    e = Embed()
    e.add_field(name="{}x^2 + {}x + {} = 0".format(floatToString(a),floatToString(b),floatToString(c)), value=calculateABC(a,b,c))
    e.color = 0x00FF00
    return await ctx.send(embed=e)

def setup(bot):
    bot.add_command(run)