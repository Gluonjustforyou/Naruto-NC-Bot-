import discord
from discord.ext import commands
import socket

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user.name} ({bot.user.id})')

@bot.command()
async def checkport(ctx):
    hostname = 'de-fra-game1.ips-hosting.com' #this shi ist just for me u need some kind of adrress
    port = 2200 #just the prot 

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((hostname, port))
        sock.close()

        if result == 0:
            await ctx.send(f"🍜 Naruto Chronicles | NarutoRP 🍥 ist online")
            await ctx.send(f"steam://connect/84.200.229.42:27022")
        else:
            await ctx.send(f"Port {port} auf {hostname} ist geschlossen.")
    except socket.error as e:
        await ctx.send(f"Fehler beim Prüfen des Ports: {e}")

bot.run('Token')
#no comms cuz it's Logic
