import discord
import os
import pandas as pd
from bot_response import counter_argument
from sentiment_embedding import sentiment_model
dataframe = pd.read_pickle('Pickles/trolley.pkl')
os.environ['TOKEN'] = 'ODM5MDIzNzUzODc4NzAwMDQz.YJDnww.wGd1crfM07bfwthv9IQ7BscPehg'
client = discord.Client()
tb = sentiment_model()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        response = counter_argument(message.content, dataframe, tb)
        await message.channel.send(response[0])
        print(response[1])

client.run(os.environ['TOKEN'])