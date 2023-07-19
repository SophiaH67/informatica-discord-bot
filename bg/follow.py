from discord.ext import commands
from discord.member import Member, VoiceState
from discord.guild import Guild
from discord.channel import VoiceChannel
from discord.member import Member
from typing import List
from discord.errors import ClientException


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.connected_guilds = {}

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        try:
            await self.join_biggest_vc(member.guild)
        except (ClientException, AttributeError):
            pass

    async def join_biggest_vc(self, guild: Guild):
        voice_channels: List[VoiceChannel] = guild.voice_channels
        highest_count = 0
        highest_channel = None
        for voice_channel in voice_channels:
            member_count = 0
            members = voice_channel.members
            members = (m for m in members if not (m._user.bot))
            for member in members:
                member_count += 1
            if member_count > highest_count:
                highest_count = member_count
                highest_channel = voice_channel

        if highest_channel is None:
            if guild.id in self.bot.connected_guilds:
                return await self.bot.connected_guilds[guild.id].disconnect()
            return
        if guild.id in self.bot.connected_guilds:
            if highest_channel.id == self.bot.connected_guilds[guild.id].channel.id:
                return
            await self.bot.connected_guilds[guild.id].disconnect()
        self.bot.connected_guilds[guild.id] = await highest_channel.connect()


async def setup(bot: commands.bot.Bot):
    await bot.add_cog(Events(bot))
