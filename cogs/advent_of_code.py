import requests
import os
from discord.ext import commands, tasks


class AOCCog(commands.Cog, description="Advent of Code stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.json_link = "https://adventofcode.com/2023/leaderboard/private/view/1065710.json"
        self.cookie = os.getenv("AOC_COOKIE")
    
    @commands.hybrid_command(name="aocupdate")
    async def manual_leaderboard_update(self, ctx: commands.Context):
        pass

    async def leaderboard_update(self):
        print(self.aoc_token)
        response = requests.get(self.json_link, cookies={"session": self.cookie})
        jsn_new = response.json()

    @tasks.loop(minutes=15)
    async def routine_leaderboard_update(self):
        await self.leaderboard_update()
    
    async def cog_load(self):
        self.routine_leaderboard_update.start()

    async def cog_unload(self):
        self.routine_leaderboard_update.stop()

async def setup(bot):
    await bot.add_cog(AOCCog(bot))

async def teardown():
    print("Advent of Code Extension unloaded!")