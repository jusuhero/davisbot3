import discord
from discord.ext import commands
import os

DAVISBOT_TOKEN = os.getenv("DAVISBOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.guilds = True
intents.guild_messages = True
intents.reactions = True  # Required for tracking reactions
intents.guild_reactions = True  # For assigning roles via rea


class Davisbot(commands.Bot):

    # Available Cogs
    initial_extensions = ["cogs.music", "cogs.advent_of_code", "cogs.utils"]

    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(
            intents=intents, command_prefix=commands.when_mentioned_or(".")
        )

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(
                    f"Could not load extension {extension} due to {e.__class__.__name__}: {repr(e)}"
                )

    async def on_ready(self) -> None:
        print("---------------------------")
        print("Logged in")
        print("Username: ", end="")
        print(self.user.name)
        print("Userid: ", end="")
        print(self.user.id)
        await self.change_presence(
            status=discord.Status.dnd, activity=discord.Game("1&1 Kundenservice")
        )
        await self.tree.sync()
        print("---------------------------")


if __name__ == "__main__":
    bot = Davisbot(intents=intents)
    bot.run(DAVISBOT_TOKEN)
