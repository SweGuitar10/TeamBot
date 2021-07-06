from asyncio.windows_events import NULL
import discord
import random

TOKEN = 'ODYxNzM2MjkzMzMwOTc2ODA5.YOOIdg.YDYfaWkYRdSGFk-IwvvL2GNKyDw'
bot_channel_name = 'team-bot-channel'
channel = NULL
client = discord.Client()

start_randomizing = False
random_message_id = NULL
msg = NULL

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_connect():
    print('We have connected as {0.user}'.format(client))
# TODO: Create a channel for the bot on connection to server
#   channel = await client.guilds[0].create_text_channel()


@client.event
async def on_message(message):
    global msg
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    start_message = f'React to this message to get ranomized into a team!\nType $teams_stop when everyone has reacted!'
    
    print(f'{username}: {user_message} ({channel})')
    cmd_start = '$teams_start'
    cmd_stop = '$teams_stop'
    cmd_setup = '$setup'
    cmd_cmd = '$commands'
    cmd_about = '$about'

    if message.author == client.user:
        if user_message == start_message:
            random_message_id = message.id
            print(random_message_id)
            await message.add_reaction("👍")
        else: 
            return

    if message.channel.name == bot_channel_name: # don't check for channel if you want to ignore specific channels
        if user_message.lower() == cmd_start:
            msg = await message.channel.send(start_message)
            print(msg.content)
        
        if user_message.lower() == cmd_stop:
            cache_msg = discord.utils.get(client.cached_messages, id=msg.id)
            users = await cache_msg.reactions[0].users().flatten() #List of users
            users.pop(0) #Remove bot from list of users that reacted
            size = len(users)
            team_1 = []
            team_2 = []

            random.shuffle(users)
            middle_index = size // 2
            team_1 = users[:middle_index]
            team_2 = users[middle_index:]
            
            team_1_msg = ''
            team_2_msg = ''

            for user in team_1:
                team_1_msg += f'\n{user.name}'
            for user in team_2:
                team_2_msg += f'\n{user.name}'
            await message.channel.send(f'The following teams have been made: \nTeam 1: {team_1_msg}\nTeam 2: {team_2_msg}')
        if user_message.lower() == cmd_setup:
            await message.channel.send(f'To start using the bot, create a channel with the name: {bot_channel_name}')
        if user_message.lower() == cmd_cmd:
            await message.channel.send(f'{cmd_start} - Start team splitting\n{cmd_stop} - Stop team splitting\n{cmd_setup} - Instructions for bot-setup\n{cmd_about} - Informatoin about the bot')
        if user_message.lower() == cmd_about:
            await message.channel.send(f'A bot that randomizes teams, it takes all users that react to the message with the given reaction and splits them into two teams.\nAuthor Kurt Areskoug, 2021')
      
            
client.run(TOKEN)