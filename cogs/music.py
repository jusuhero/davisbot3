from discord.ext import commands

@commands.command()
async def super_command(ctx: commands.Context):
    pass

async def setup(bot):
    print("Music cog: Not implemented")