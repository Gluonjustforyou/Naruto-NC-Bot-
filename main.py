import socket
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user.name} ({bot.user.id})')

@bot.command()
async def checkserver(ctx):
    server_ip = '84.200.229.42'  # IP-Adresse des Gmod-Servers
    server_port = 27022  # Port des Gmod-Servers

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((server_ip, server_port))
        sock.close()

        if result == 0:
            await ctx.send("Der Gmod-Server ist online.")
        else:
            await ctx.send("Der Gmod-Server ist offline.")
    except socket.error as e:
        await ctx.send(f"Fehler beim Überprüfen des Gmod-Servers: {e}")


bot.run('Token')
#no comms cuz it's Logic
