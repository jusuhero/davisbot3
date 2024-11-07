import discord
from discord.ext import commands
import os

DAVISBOT_TOKEN = os.getenv("DAVISBOT_TOKEN")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.guilds = True
intents.guild_messages = True
intents.reactions = True  # Required for tracking reactions
intents.guild_reactions = True  # For assigning roles via reactions

# Initialize the bot
bot = commands.Bot(command_prefix=".", intents=intents)

# Load cogs
initial_extensions = [
    "cogs.music",
    "cogs.advent_of_code",
    "cogs.utils"
]

async def setup_hook() -> None:
    for extension in initial_extensions:
        await bot.load_extension(extension)

@bot.event
async def on_ready() -> None:
    print("---------------------------")
    print("Logged in")
    print("Username: ", end="")
    print(bot.user.name)
    print("Userid: ", end="")
    print(bot.user.id)
    await bot.change_presence(
        status=discord.Status.dnd, activity=discord.Game("1&1 Kundenservice")
    )
    print("---------------------------")


if __name__ == "__main__":
    bot.setup_hook = setup_hook
    bot.run(DAVISBOT_TOKEN)
