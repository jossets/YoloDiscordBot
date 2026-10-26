#!/usr/bin/python3 


import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import urllib.request
import base64


#load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if ((TOKEN is None) or (len(TOKEN)<=0)):
    print("TOKEN null\n", flush=True)
    exit()
#print("Token: "+TOKEN, flush=True)

def register(discordid, code):
    print("Registering "+discordid+" "+code)
    discordidb64 = (base64.b64encode(bytes(discordid, 'utf-8'))).decode('ascii')
    codeb64 = (base64.b64encode(bytes(code, 'utf-8'))).decode('ascii')
    url = "https://zenzenvibe.org/setLinkCode.php?LinkCode="+codeb64+"&DiscordId="+discordidb64
    print(url)
    f = urllib.request.urlopen(url)
    resp = f.read()
    return resp.decode('ascii')


def achievements(discordid):
    print("Achievements "+discordid)
    discordidb64 = (base64.b64encode(bytes(discordid, 'utf-8'))).decode('ascii')
    url = "https://zenzenvibe.org/getAchievements.php?DiscordId="+discordidb64
    print(url)
    f = urllib.request.urlopen(url)
    resp = f.read()
    return resp.decode('ascii')

async def print_members_list():
    for guild in client.guilds:
        print(guild.id)
        members = await guild.chunk()
        for member in members:
            print(member)
            print(member.roles)
        print ("Count: "+str(len(members)))

async def getIdFromName(name):
    for guild in client.guilds:
        members = await guild.chunk()
        for member in members:
            if (member.name == name):
                print("Found ")
                print(member)
                return str(member)
    return "NotFound"


intents = discord.Intents(messages=True, guilds=True)
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!')

#@bot.command(pass_context=True)
#async def addrole(ctx, rolename):
#    user = ctx.message.author
#    role = discord.utils.get(user.server.roles, name=rolename) 
#    await client.add_roles(user, role)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!', flush=True)
    return
    

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        print(f'\nMsg from {message.author} [{message.content}]', flush=True)

        if message.content.startswith("!help"):
            response = """Command:
            - !link XXXXXXXX
            - !myachievements
            - !updaterole
            - !achievements   DISCORDUSERNAME#ID
            """
            await message.channel.send(response)

        if message.content.startswith("!link"):
            fields = message.content.strip().split()
            if (len(fields)<=1):
                response = "Usage: !link XXXXXXXX"
                await message.channel.send(response)
                return
            code = fields[1] #message.content[6:].strip()

            cleancode = ''.join([c for c in code if c.isalnum()])
            response = "Registering "+cleancode
            await message.channel.send(response)
            status = register('{}'.format(message.author), cleancode)
            response = status
            await message.channel.send(response)

        if message.content.startswith("!myachievements"):
            status = achievements('{}'.format(message.author))
            response = status
            await message.channel.send(response)

        if message.content.startswith("!updaterole") or message.content.startswith("!u"):
            status = achievements('{}'.format(message.author))
            achievement_name = "ACHIEVEMENT_ALLFLAGS"+": DONE"
            role_name = "Bikini 100%"
            if achievement_name in status:
                user = message.author     
                print(user)      
                member = await client.fetch_user(message.author.id)
                print(member)
                botmember = await client.fetch_user(client.user.id)
                role = discord.utils.get(user.guild.roles, name=role_name) 
                print(role)
                print(message.author.roles)
                authorroles = [y.name.lower() for y in message.author.roles]
                print(authorroles)
                if role_name.lower()  in authorroles:
                    response = "Deja dans le role "+role_name
                    await message.channel.send(response)
                else:
                    await user.add_roles(role)
                    response = "Félicitation: Nouveau role : "+role_name
                    await message.channel.send(response)
            else:
                response = "Achievement 100% not found\nRetry in few minutes."
                await message.channel.send(response)   
            

        if message.content.startswith("!achievements"):
            fields = message.content.strip().split(' ')
            if (len(fields)<=1):
                target = message.author
            else:
                targetname = message.content[13:].strip()
                if targetname.find("#") !=-1:
                    target = targetname
                else:
                    target = await getIdFromName(targetname)
            print("target: "+str(target), flush=True)
            status = achievements(str(target))
            response = "Steam achievements list ["+target+"]: \n"+status
            await message.channel.send(response)

        if message.content.startswith('!members'):
            for guild in client.guilds:
                print("======")
                print("Server: "+str(guild), flush=True)
                for member in guild.members:
                    print("- "+str(member.id)+" "+str(member.name)+" "+str(member)) 
                
            await message.channel.send("Ok")
    except:
        pass

print("Yolo Bot starting\n", flush=True)
client.run(TOKEN)
print("Yolo Bot exit\n", flush=True)
