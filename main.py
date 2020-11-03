import discord

if __name__ == '__main__':

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)


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

            await message.channel.send(f"```Online: {online}.\nIdle: {idle}.\nOffline: {offline}```")

    token = input("Token: ")
    client.run(token)
