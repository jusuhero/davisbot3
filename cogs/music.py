import os
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio


class MusicCog(commands.Cog, description="Can play music from local files or Youtube."):

    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    async def join_voice(self, interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            if not self.voice_client or not self.voice_client.is_connected():
                self.voice_client = await channel.connect()
            elif self.voice_client.channel != channel:
                await self.voice_client.move_to(channel)
        else:
            await interaction.response.send_message(
                "You must be in a voice channel to use this command.", ephemeral=True
            )
            return False
        return True

    @app_commands.command()
    async def stop(self, interaction: discord.Interaction):
        """
        Stops playback and disconnects from channel.
        """
        self.voice_client.stop()
        await self.voice_client.disconnect()
        await interaction.response.send_message("Bis Baldrian!")


    @app_commands.command(name="yt", description="Playback audio from a youtube video.")
    @app_commands.describe(url="Youtube URL to play.")
    async def play_youtube(self, interaction: discord.Interaction, url: str):
        if not await self.join_voice(interaction):
            return
        
        # Defer interaction since loading might (and usually will) take longer than 3 seconds
        await interaction.response.defer()

        # Use yt-dlp to get the direct audio URL
        ydl_opts = {"format": "bestaudio", "quiet": True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info["url"]
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            return

        # Play audio in the voice channel
        self.voice_client.play(
            discord.FFmpegPCMAudio(audio_url),
            after=lambda e: print(f"Finished playing: {e}"),
        )
        await interaction.followup.send(f"Playing audio from {url}")

    @commands.command()
    async def super_command(self, ctx: commands.Context):
        pass


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
