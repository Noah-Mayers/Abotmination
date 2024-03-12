# bot.py

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sheets

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

COMMAND_PREFIX = '+'
ALIAS_HELP = ['?','commands']
ALIAS_1E = ['classic']
ALIAS_2E = ['modern']
ALIAS_DC = ['dceased','dchero']
ALIAS_FAN = ['fantasy','bp']
ALIAS_MZ = ['marvel','marvelhero','mzhero']
ALIAS_NLD = ['notld']
ALIAS_SCI = ['scifi','sci-fi','invader']
ALIAS_WES = ['western','uoa']
ALIAS_Z1E = ['zclassic','zombivor']
ALIAS_Z2E = ['zmodern','zombivor2e']
ALIAS_ZDC = ['dczombie','dcz']
ALIAS_ZMZ = ['mzzombie','mzz']

abotmination = commands.Bot(command_prefix = COMMAND_PREFIX, intents = discord.Intents.all())
abotmination.remove_command('help')

@abotmination.event
async def on_ready():
   print(f'{abotmination.user} has awoken!\n')
   sheets.populate_sheets()
   for server in abotmination.guilds:
        print('Spawned in', server.name)

@abotmination.command(name = '1e', aliases = ALIAS_1E)
async def on_command_1E(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_1e, discord.Color.blue(), '1E Survivor')

@abotmination.command(name = '2e', aliases = ALIAS_2E)
async def on_command_2E(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_2e, discord.Color.blue(), '2E Survivor')

@abotmination.command(name = 'dc', aliases = ALIAS_DC)
async def on_command_dc(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_dc, discord.Color.blue(), 'DCeased Heroes')

@abotmination.command(name = 'fan', aliases = ALIAS_FAN)
async def on_command_FAN(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_fan, discord.Color.blue(), 'Fantasy')

@abotmination.command(name = 'mz', aliases = ALIAS_MZ)
async def on_command_mz(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_mz, discord.Color.blue(), 'MZ Heroes')

@abotmination.command(name = 'nld', aliases = ALIAS_NLD)
async def on_command_nld(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_nld, discord.Color.blue(), 'NotLD')

@abotmination.command(name = 'sci', aliases = ALIAS_SCI)
async def on_command_sci(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_sci, discord.Color.blue(), 'SciFi')

@abotmination.command(name = 'wes', aliases = ALIAS_WES)
async def on_command_wes(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_wes, discord.Color.blue(), 'Western')

@abotmination.command(name = 'z1e', aliases = ALIAS_Z1E)
async def on_command_z1e(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_z1e, discord.Color.green(), '1E Zombivors')

@abotmination.command(name = 'z2e', aliases = ALIAS_Z2E)
async def on_command_z2e(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_z2e, discord.Color.green(), '2E Zombivors')

@abotmination.command(name = 'zdc', aliases = ALIAS_ZDC)
async def on_command_zdc(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_zdc, discord.Color.green(), 'DCeased Zombies')

@abotmination.command(name = 'zmz', aliases = ALIAS_ZMZ)
async def on_command_zmz(ctx, *, prompt):
    await survivor_search(ctx, prompt, sheets.sheet_zmz, discord.Color.green(), 'MZ Zombies')

@abotmination.command(name = 'help', aliases = ALIAS_HELP)
async def on_command_help(ctx):
    await ctx.message.add_reaction('🕒')
    text = (
        '```fix'
        + '\nCHARACTER LOOKUP COMMANDS'
        + '\n------------------------------------------------------'
        + '\n1st Edition: Survivors - 1e' + await list_alias(ALIAS_1E)
        + '\n1st Edition: Zombivors - z1e' + await list_alias(ALIAS_Z1E)
        + '\n\n2nd Edition: Survivors - 2e' + await list_alias(ALIAS_2E)
        + '\n2nd Edition: Zombivors - z2e' + await list_alias(ALIAS_Z2E)
        + '\n\nFantasy: Survivors - fan' + await list_alias(ALIAS_FAN)
        + '\n\nSci-fi: Survivors - sci' + await list_alias(ALIAS_SCI)
        + '\n\nWestern: Survivors - wes' + await list_alias(ALIAS_WES)   
        + '\n------------------------------------------------------'
        + '\nDCeased: Heroes - dc' + await list_alias(ALIAS_DC) 
        + '\nDCeased: Zombies - zdc' + await list_alias(ALIAS_ZDC)  
        + '\n\nMarvel Zombies: Heroes - mz' + await list_alias(ALIAS_MZ)
        + '\nMarvel Zombies: Zombies - zmz' + await list_alias(ALIAS_ZMZ)   
        + '\n------------------------------------------------------'
        + '\nNight of the Living Dead Survivors - nld' + await list_alias(ALIAS_NLD)
        + '\n```'
    )
    await ctx.reply(text, mention_author = False)
    await ctx.message.remove_reaction('🕒', abotmination.user)

async def list_alias(alias):
    text = ''
    for x in alias:
        text +=  ', ' + x
    return text

async def survivor_search(ctx, prompt, sheet, color, tab):
    await ctx.message.add_reaction('🕒')
    sheet_data = await sheet.search(prompt)
    embedData = None
    if not sheet_data:
        embedData = discord.Embed(
            title = 'Character not found',
            description = 'No character found by that name in: ' + tab,
            color = discord.Color.red()
        )
    else:
        embedData = discord.Embed(
            title = sheet_data[0],
            description = sheet_data[1],
            color = color 
        )
    await ctx.reply(embed = embedData, mention_author = False)
    await ctx.message.remove_reaction('🕒', abotmination.user)

abotmination.run(TOKEN)