import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')

@bot.command()
async def ticket(ctx):
    # Überprüfe, ob der Benutzer bereits ein Ticket hat
    ticket_channel = discord.utils.get(ctx.guild.channels, name=f"ticket-{ctx.author.id}")
    if ticket_channel:
        await ctx.send("Du hast bereits ein offenes Ticket!")
    else:
        # Kanal erstellen und konfigurieren
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ticket_channel = await ctx.guild.create_text_channel(f"ticket-{ctx.author.id}", overwrites=overwrites)
        await ctx.send(f"Ticket erstellt: {ticket_channel.mention}")

@bot.command()
async def close(ctx):
    # Überprüfe, ob der Befehl im richtigen Kanal verwendet wird
    if not ctx.channel.name.startswith("ticket-"):
        await ctx.send("Dieser Befehl kann nur in einem Ticket-Kanal verwendet werden.")
    else:
        await ctx.channel.delete()
        await ctx.send("Ticket geschlossen.")

# Füge hier deinen Bot-Token ein
bot.run('DEIN_DISCORD_BOT_TOKEN')
