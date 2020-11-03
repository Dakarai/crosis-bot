import discord

if __name__ == '__main__':

    client = discord.Client()


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


    token = input("Token: ")
    client.run(token)
