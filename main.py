import discord

if __name__ == '__main__':

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    token = open("token.txt", "r").read()


    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        print(f'Logged into {client.get_guild(135136943179563008)}')


    @client.event
    async def on_message(message):
        print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
        guild = client.get_guild(135136943179563008)

        if 'crosisbot.member_count' == message.content.lower():
            await message.channel.send(f'```{guild.member_count}```')

        elif 'crosisbot.community_report' == message.content.lower():
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
            await message.channel.send(f"```Online: {online}\nIdle: {idle}\nOffline: {offline}```")

        elif 'crosisbot.ping' == message.content.lower():
            await message.channel.send(f'{message.author.mention} <:Krappa:370365085576724482>')

        elif 'crosisbot.emojis' == message.content.lower():
            if message.author.id != 117928787747799049:
                await message.channel.send('This is only available to bot administrators.')
            else:
                for emoji in guild.emojis:
                    print(emoji.name, emoji.id, emoji.require_colons)

        elif 'crosisbot.message_count' == message.content.lower():
            counter = 0
            async for history_message in message.channel.history(limit=None): #don't actually use None
                if message.author == history_message.author:
                    counter += 1
            await message.channel.send(f'{message.author.mention} has published {counter} messages in this channel'
                                       f'<:yikes:325990368879312897>')

    client.run(token)
