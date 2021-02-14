import os

from discord.ext import commands
from wakeonlan import send_magic_packet
from mcstatus import MinecraftServer
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MC_IP = os.getenv('MC_SERVER_IP')
MC_MAC = os.getenv('MC_SERVER_MAC')

bot = commands.Bot(command_prefix='?')

mcserver = MinecraftServer(MC_IP)


@bot.command(name='status')
async def status(ctx):
    status = None
    try:
        status = mcserver.status()
    except:
        await ctx.send('Server offline ❌, try ?wake to wake the server up')
        return

    response = f'Server online ✅, {status.players.online} players online'

    await ctx.send(response)


@bot.command(name='wake')
async def wake(ctx):
    send_magic_packet(MC_MAC)
    response = f'Turning server on 🌞'

    await ctx.send(response)


bot.run(TOKEN)
