from discord.ext import commands

class UtilsCog(commands.Cog, description="Provides utility and information functions."):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"> Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name="refreshslashcommands")
    async def refresh_slashcommands(self, ctx: commands.Context):
        await self.bot.tree.sync()
        await ctx.send("Commands refreshed. Restart you client.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))

async def teardown():
    print("Utils Extension unloaded!")