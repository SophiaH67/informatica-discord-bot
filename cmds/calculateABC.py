from sympy import symbols, Eq, solve, core
from discord.ext import commands
from discord import Embed
from discord.ext.commands.context import Context

def floatToString(flt:float) -> str:
    return ('%.15f' % flt).rstrip('0').rstrip('.')

def calculateABC(A:float, B:float, C:float) -> str:
    x = symbols('x')
    equation = Eq(A*x**2+B*x+C, 0)
    solutions = solve(equation)
    for solution in solutions:
        if not type(solution) is core.numbers.Float:
            return "This formula no workie"
    return " or ".join(floatToString(v) for v in solutions)


@commands.command(name="abc", aliases=["abcformula","calculate","solve"], help="Calculates quadratic formula")
async def run(ctx: commands.context.Context, A: float, B:float, C:float):
    e = Embed()
    e.add_field(name="{}x^2 + {}x + {} = 0".format(floatToString(A),floatToString(B),floatToString(C)), value=calculateABC(A,B,C))
    e.color = 0x00FF00
    return await ctx.send(embed=e)

async def setup(bot: commands.bot.Bot):
    bot.add_command(run)