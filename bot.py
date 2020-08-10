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
    async with ctx.message.channel.typing():
        channel = ctx.message.channel                                                       #Fetches channel, guild from which the command has been issued,
        date = ctx.message.created_at - datetime.timedelta(30)                              #takes date 30 days prior, and the role immune to purge.
        guild = ctx.guild
        print(date)
        role = discord.utils.find(lambda i: i.id == 718782248345796688, guild.roles)
        active_users = dict()

        async for message in channel.history(limit = None, after = date):                   #Collects messages from the last 30 days, evaluates activity.
            if message.author in guild.members:
                if (not role in message.author.roles and not message.author.bot):
                    if not message.author.display_name in active_users:
                        active_users[message.author.display_name] = 1
                    else:
                        active_users[message.author.display_name] += 1

        intro = 'Here’s the total activity evaluation regarding the prior 30 days:'         #This creates the embed. It has 3 important string values; introduction,
        kick = 'Members kicked: '                                                           #activity evaluation (praise_list) and kick message.
        praise_list = ''

        for x, y in active_users.items():                                                   #Creates praise_list based on active_users dictionary.
            praise_list = praise_list + x + ': ' + str(y) + '\n'
        praise_list = praise_list[:-1]
        if praise_list == '':
            praise_list = '*This server is dying.*'

        embed = discord.Embed(color = 0x664656)
        embed.set_author(name = client.user.display_name, icon_url = client.user.avatar_url)
        embed.add_field(name = intro, value = praise_list, inline = False)
        embed.set_footer(text = 'Considers only non-role members. Stop sullying.')
        await ctx.send(embed = embed)

        for member in guild.members:                                                        #Kicks and creates kick message simultaneously.
            if (not role in member.roles and not member.bot
                    and not member.display_name in active_users):
                kick = kick + member.display_name + ', '
                await member.kick()
        kick = kick[:-2]
        kick += '.'
        if not kick == 'Members kicked.':
            await ctx.send(kick)
 
#Run the bot.
client.run(token)
