import discord
from discord.ext import commands
from discord.ui import View, Select
from itertools import chain


class HelpSelect(Select):
    def __init__(self, bot):
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(label=cog_name, description=cog.__doc__)
                for cog_name, cog in bot.cogs.items()
            ],
        )

        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        try:
            cog = self.bot.get_cog(self.values[0])
            assert cog

            commands_list = list(chain(cog.walk_commands(), cog.walk_app_commands()))

            embed = discord.Embed(
                title=f"{cog.__cog_name__} Commands",
                description="\n".join(
                    f"• **{command.name}**: `{command.description or 'No Description provided'}`"
                    for command in commands_list
                ),
                color=discord.Color.blue(),
            )
            await interaction.response.edit_message(embed=embed)

        except AssertionError as ae:
            print(
                f"Could not load help info for cog {cog}. Does it exist? Error: {repr(ae)}"
            )


class UtilsCog(commands.Cog, description="Provides utility and information functions."):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"> Pong! {round(self.bot.latency * 1000)}ms")

    @commands.hybrid_command(
        name="help",
        description="Shows a help section with a list of commands available in all cogs..",
    )
    async def help_function(self, ctx: commands.Context):
        embed = discord.Embed(
            title=f"Davisbot v{self.bot.VERSION} - Help section",
            description="Select an entry from the dropdown menu below to see the available commands of the respective module. ",
        )
        view = View().add_item(HelpSelect(self.bot))
        await ctx.send(embed=embed, view=view, ephemeral=True)

    @commands.command(name="refreshslashcommands")
    async def refresh_slashcommands(self, ctx: commands.Context):
        await self.bot.tree.sync()
        await ctx.send("Commands refreshed. Restart you client.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(UtilsCog(bot))


async def teardown():
    print("Utils Extension unloaded!")
