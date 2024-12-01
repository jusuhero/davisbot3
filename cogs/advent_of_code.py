import requests
import os
import json
import discord
from discord.ext import commands, tasks

from collections import namedtuple
from datetime import datetime
from pytz import timezone

Star = namedtuple("Star", ["username", "day", "star", "timestamp"])
User = namedtuple("User", ["username", "stars", "score"])

class AOCCog(commands.Cog, description="Advent of Code stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 915670668979347498 #1312765325422624839
        self.year = 2024
        self.leaderboard_id = 1065710
        self.channel = None
        self.leaderboard_link = f"https://adventofcode.com/{self.year}/leaderboard/private/view/{self.leaderboard_id}"
        self.json_link = f"{self.leaderboard_link}.json" 
        self.cookie = os.getenv("AOC_COOKIE")
        self.leaderboard_path = "leaderboard.json"
        self.json = self.load_json(path=self.leaderboard_path)
        
    def load_json(self, path: str) -> dict:
        if not os.path.isfile(path):
            print(f"File {path} does not exist. Using empty dict instead.")
            return {"members": []}
        try:
            with open(path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading json from file.")
            return {"members": []}
        
    def save_json(self, path: str) -> None:
        with open(path, "w") as file:
            json.dump(self.json, file, indent=2)

    def get_new_members(self, old, new):
        new_members = []
        for member, entry in new["members"].items():
            if member not in old["members"]:
                new_members.append(entry["name"])
        return new_members
    
    def get_new_stars(self, old, new) -> list[Star]:
        new_stars = []
        for member, entry in new["members"].items():
            for day, stars in entry["completion_day_level"].items():
                for star in stars:
                    old_members = old["members"]
                    if member in old_members:
                        old_days = old_members[member]["completion_day_level"]
                        if day in old_days:
                            old_stars = old_days[day]
                            if star in old_stars:
                                continue
                    new_stars.append(Star(entry["name"], day, star, stars[star]["get_star_ts"]))
        return sorted(new_stars, key=lambda x: x.timestamp)

    
    @commands.hybrid_command(name="aocupdate")
    async def manual_leaderboard_update(self, ctx: commands.Context):
        await self.leaderboard_update()

    async def leaderboard_update(self):
        response = requests.get(self.json_link, cookies={"session": self.cookie})
        json_new = response.json()

        new_members = self.get_new_members(self.json, json_new)
        for new_member in new_members:
            await self.channel.send(f"{new_member} ist dem Leaderboard beigetreten. Zieht euch warm an!")

        new_stars = self.get_new_stars(self.json, json_new)
        for star in new_stars:
            tz_cet = timezone("Europe/Berlin")
            time = datetime.fromtimestamp(star.timestamp).astimezone(tz_cet).strftime("%d.%m. %H:%M:%S")
            msg = f"{time}: {star.username} hat den {star.star}. Stern von Tag {star.day} erhalten. Glückwunsch!"
            await self.channel.send(msg)

        self.json=json_new
        self.save_json(self.leaderboard_path)

    @commands.command()
    async def leaderboard(self, ctx):
        await self.leaderboard_update()
        
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}
        members = [User(m["name"], m["stars"], m["local_score"]) for m in self.json["members"].values()]
        members.sort(key=lambda user: (-user.stars, -user.score, user.username))
        msg = "\n".join(
            [
                f"{name.ljust(22)}⭐ {str(stars).rjust(2).ljust(6)}{medals[i] if i in medals else '🏅'} {str(score).rjust(3)}"
                for i, (name, stars, score) in enumerate(members)
                if score > 0
            ]
        )
        msg = f"```\n{msg}\n```"
        embed = discord.Embed(
            title=f"Advent of Code {self.year} Leaderboard",
            description=msg,
            url=self.leaderboard_link,
            color=0x0F0F23,
        )
        await self.channel.send(embed=embed)


    @tasks.loop(minutes=15)
    async def routine_leaderboard_update(self):
        await self.leaderboard_update()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(self.channel_id)
        self.routine_leaderboard_update.start()

    async def cog_unload(self):
        self.routine_leaderboard_update.stop()

async def setup(bot):
    await bot.add_cog(AOCCog(bot))

async def teardown():
    print("Advent of Code Extension unloaded!")