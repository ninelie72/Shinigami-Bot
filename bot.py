import discord
from discord.ext import commands

import datetime

#Fetch original app token for security reasons.
token = input('Please enter the sacred adage: ')    

#Define said bot, Shinigami as client.
client = commands.Bot(command_prefix = '#')     

#Making sure everything's online and ready.
@client.event
async def on_ready():
    print('Bot is ready.')

#Owner's key.
def owner_check(ctx):
    return ctx.author.id == ctx.guild.owner_id 

#Purge command.
@client.command()
@commands.check(owner_check)
async def purge(ctx):
    channel = ctx.message.channel                                                      #Fetches channel, guild from which the command has been issued,
    date = ctx.message.created_at - datetime.timedelta(30)                             #takes date 30 days prior, and the role immune to purge.
    guild = ctx.guild
    print(date)
    role = discord.utils.find(lambda i: i.id == 737360924276686929, guild.roles)
    active_users = dict()

    async for message in channel.history(limit = None, after = date):                  #Collects messages from the last 30 days, evaluates activity.
        if message.author in guild.members:
            if (not role in message.author.roles and not message.author.bot):
                if not message.author.display_name in active_users:
                    active_users[message.author.display_name] = 1
                else:
                    active_users[message.author.display_name] += 1
    for x, y in active_users.items(): 
            await ctx.send(f'{x}: {y}')

    for member in guild.members:                                                       #Removes inactive users.
        if (not role in member.roles and not member.bot 
                and not member.display_name in active_users):
            await ctx.send(f'Fuck you, {member.display_name}!')
            await member.kick()
        
#Run the bot.
client.run(token)
