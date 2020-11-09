import discord
import asyncio
import time
import pymongo

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

if __name__ == '__main__':

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    token = open("token.txt", "r").read()
    mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017')

    def community_report(guild):
        online = 0
        idle = 0
        offline = 0
        for m in guild.members:
            if str(m.status) == "online":
                online += 1
            if str(m.status) == "offline":
                offline += 1
            else:
                idle += 1
        return online, idle, offline


    def log_message(message):
        global mongo_db
        mongo_db['messages'].insert_one({
            '_id':  message.id,
            #'tts':  message.tts,
            #'type': message.type,
            'author': message.author.name,
            'author_id': message.author.id,
            'content': message.content,
            #'embeds': message.embeds,
            'channel': message.channel.name,
            #'mentions_everyone': message.mention_everyone,
            #'mentions': message.mentions,
            #'channel_mentions': message.channel_mentions,
            #'role_mentions': message.role_mentions,
            #'attachments': message.attachments,
            'guild': message.guild.name,
            #'posted_time': message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        })


    async def user_metrics_background_task():
        await client.wait_until_ready()
        global cur_guild

        while not client.is_closed():
            try:
                online, idle, offline = community_report(cur_guild)
                with open('user_metrics.csv', 'a') as f:
                    f.write(f'{int(time.time())},{online},{idle},{offline}\n')

                plt.clf()
                df = pd.read_csv('user_metrics.csv', names=['time', 'online', 'idle', 'offline'])
                df['date'] = pd.to_datetime(df['time'], unit='s', utc=True)
                df['total'] = df['online'] + df['offline'] + df['idle']
                df.drop('time', 1, inplace=True)
                df.set_index('date', inplace=True)
                df['online'].plot()
                df['idle'].plot()
                df['offline'].plot()
                plt.legend()
                plt.savefig('online.png')

                await asyncio.sleep(5)

            except Exception as e:
                print(str(e))
                await asyncio.sleep(5)


    @client.event
    async def on_ready():
        global cur_guild, mongo_db
        cur_guild = client.get_guild(135136943179563008)
        print(f'We have logged in as {client.user}')
        print(f'Logged into {client.get_guild(135136943179563008)}')

        mongo_db = mongo_client[str(cur_guild.id)]
        print(f'We have connected to database {mongo_db}')

    @client.event
    async def on_message(message):
        global cur_guild
        print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
        log_message(message)
        # await message.add_reaction(client.get_emoji(370365085576724482))

        if 'crosisbot.member_count' == message.content.lower():
            await message.channel.send(f'```{cur_guild.member_count}```')

        elif 'crosisbot.community_report' == message.content.lower():
            online, idle, offline = community_report(cur_guild)
            await message.channel.send(f"```Online: {online}\nIdle: {idle}\nOffline: {offline}```")

            file = discord.File('online.png', filename='online.png')
            await message.channel.send(file=file)

        elif 'crosisbot.ping' == message.content.lower():
            await message.channel.send(f'{message.author.mention} <:Krappa:370365085576724482>')

        elif 'crosisbot.emojis' == message.content.lower():
            if message.author.id != 117928787747799049:
                await message.channel.send('This is only available to bot administrators.')
            else:
                for emoji in cur_guild.emojis:
                    print(emoji.name, emoji.id, emoji.require_colons)

        elif 'crosisbot.message_count' == message.content.lower():
            counter = 0
            async for history_message in message.channel.history(limit=None):  # don't actually use None
                if message.author == history_message.author:
                    counter += 1
            await message.channel.send(f'{message.author.mention} has published {counter} messages in this channel'
                                       f'<:yikes:325990368879312897>')

        elif 'crosisbot.message_backfill' in message.content.lower():
            if message.author.id != 117928787747799049:
                await message.channel.send('This is only available to bot administrators.')
            else:
                limit_to_backfill = None
                temp = message.content.lower().split()
                if len(temp) == 2:
                    if temp[1].isdigit() and int(temp[1]) > 0:
                        limit_to_backfill = int(temp[1])
                async for history_message in message.channel.history(limit=limit_to_backfill):
                    try:
                        log_message(history_message)
                    except Exception as e:
                        print(e)


    client.loop.create_task(user_metrics_background_task())
    client.run(token)
