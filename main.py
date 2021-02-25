import os
import asyncio

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

# Gives the status of the server, including number of players online.
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


# Turns the server on.
@bot.command(name='wake')
async def wake(ctx):
    # 3 minutes of trying to wake
    tries = 9
    time_between_tries = 20
    
    # sending WOL packet
    send_magic_packet(MC_MAC)
    response = f'Turning server on 🌞. Please wait'
    await ctx.send(response)

    # waiting for response
    for i in range(tries):
        try:
            status = mcserver.status()
        except:
            # server still off
            await asyncio.sleep(time_between_tries)
            continue
        
        # success
        success_response = f'Server online ✅'
        await ctx.send(success_response)
        return
    
    # failure
    failure_response = f'Couldn\'t turn the server on!'
    await ctx.send(failure_response)


bot.run(TOKEN)
