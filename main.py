import socket
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import asyncio

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user.name} ({bot.user.id})')

    # Starte die Aktualisierung der Serverstatus-Nachricht
    await update_server_status()

async def update_server_status():
    server_ip = '84.200.229.42'  # IP-Adresse des Gmod-Servers
    server_port = 27022  # Port des Gmod-Servers
    channel_id = '1101229312008540200'  # ID des Kanals, in dem die Nachricht angezeigt werden soll
    message_id = None  # ID der Nachricht, die aktualisiert werden soll
    image_path = 'ilias_ist_ein_lauch.png'  # Pfad zum Bild
    interval_seconds = 10  # Aktualisierungsintervall in Sekunden

    previous_status = None  # Vorheriger Serverstatus

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((server_ip, server_port))
            sock.close()

            channel = bot.get_channel(int(channel_id))

            if message_id is None:
                # Erste Ausführung: Bild mit Text erstellen und senden
                current_status = "Der Server ist Offline"
                if result == 0:
                    current_status = "Der Server ist online"

                connectlink = "steam://connect/84.200.229.42:27022"

                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype("njnaruto.ttf", 35)  # Schriftart und Größe anpassen
                text_bbox = draw.textbbox((0, 0), current_status, font=font)
                text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
                text_position = (290, 45)  # Position oben links
                
                draw.text(text_position, current_status, font=font, fill=(255, 255, 255))  # Text auf Bild zeichnen
                draw.text(text_position, current_status, font=font, fill="#E1EDFA")  # Text auf Bild zeichnen


                link_font = ImageFont.truetype("lastninja.ttf", 35)  # Schriftart und Größe des Links
                link_bbox = draw.textbbox((0, 0), connectlink, font=link_font)
                link_text_width, link_text_height = link_bbox[2] - link_bbox[0], link_bbox[3] - link_bbox[1]
                link_position = (image.width - link_text_width - 10, image.height - link_text_height - 10)  # Position unten rechts
                draw.text(link_position, connectlink, font=link_font, fill=(255, 255, 255))  # Link auf Bild zeichnen
                draw.text(link_position, connectlink, font=link_font, fill="#E1EDFA")  # Link auf Bild zeichnen

                with io.BytesIO() as image_bytes:
                    image.save(image_bytes, format='PNG')
                    image_bytes.seek(0)
                    file = discord.File(image_bytes, filename='ellias_steifenerguss.png')
                    message = await channel.send(file=file)
                    message_id = message.id

            else:
                # Folgeausführungen: Bild aktualisieren
                message = await channel.fetch_message(message_id)

                current_status = "Der Server ist offline"
                if result == 0:
                    current_status = "Der Server ist online"

                if current_status != previous_status:  # Überprüfe, ob sich der Serverstatus geändert hat
                    image = Image.open(image_path)
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype("njnaruto.ttf", 35)  # Schriftart und Größe anpassen
                    text_bbox = draw.textbbox((0, 0), current_status, font=font)
                    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
                    text_position = (290, 45)  # Position oben links
                    draw.text(text_position, current_status, font=font, fill=(255, 255, 255))  # Text auf Bild zeichnen
                    draw.text(text_position, current_status, font=font, fill="#E1EDFA")  # Text auf Bild zeichnen
                  
                    link_font = ImageFont.truetype("lastninja.ttf", 25)  # Schriftart und Größe des Links
                    link_bbox = draw.textbbox((0, 0), connectlink, font=link_font)
                    link_text_width, link_text_height = link_bbox[2] - link_bbox[0], link_bbox[3] - link_bbox[1]
                    link_position = (image.width - link_text_width - 10, image.height - link_text_height - 10)  # Position unten rechts
                    draw.text(link_position, connectlink, font=link_font, fill=(255, 255, 255))  # Link auf Bild zeichnen
                    draw.text(link_position, connectlink, font=link_font, fill="#E1EDFA")  # Link auf Bild zeichnen

                    with io.BytesIO() as image_bytes:
                        image.save(image_bytes, format='PNG')
                        image_bytes.seek(0)
                        file = discord.File(image_bytes, filename='status.png')

                        try:
                            await message.delete()  # Alte Nachricht löschen
                            message = await channel.send(file=file)  # Neue Nachricht senden
                            message_id = message.id

                        except discord.NotFound:
                            # Nachricht wurde inzwischen gelöscht, eine neue Nachricht senden
                            message = await channel.send(file=file)
                            message_id = message.id

                    previous_status = current_status

        except socket.error as e:
            print(f"Fehler beim Überprüfen des Gmod-Servers: {e}")

        await asyncio.sleep(interval_seconds)

@bot.command()
async def get_channel_id(ctx):
    channel = ctx.channel
    await ctx.send(f"Die ID des Kanals ist: {channel.id}")


bot.run('Token')
