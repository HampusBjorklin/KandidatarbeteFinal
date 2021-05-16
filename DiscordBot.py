import discord
import os
import pandas as pd
from bot_response import counter_argument
import random
dataframe = pd.read_pickle('Pickles/trolley.pkl')
os.environ['TOKEN'] = 'ODM5MDIzNzUzODc4NzAwMDQz.YJDnww.wGd1crfM07bfwthv9IQ7BscPehg'
question = ["I'd rather not answer direct questions", 'My ability to answer direct question is quite compromised',
            'Answers to direct questions are easier found on google']

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    await client.get_channel(826075188671283250).send(f"""Hello {member.name}! I'm TrolleyBot, I try my best to discuss moral dilemmas
    with people on the internet. My favorite dilemma is the trolley problem – is it moral to divert a train onto a track where it will kill one person to save five others? – 
    If you want to debate me, start your message with '!' (Example: !You should pull the lever because...)  """
)

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith('!'):
        user_input = message.content[1:]
        if '?' in message.content:
            ran = random.randint(0, 2)
            await message.channel.send(question[ran] + message.author.mention)
        else:
            response = counter_argument(user_input, dataframe)
            await message.channel.send(response[0] + message.author.mention)
            if '(No pro/con arg)' in response[1]:
                emoji = '\U0001f44d'
                await message.add_reaction(emoji)
            print(response[1])

client.run(os.environ['TOKEN'])