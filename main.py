import asyncio
import os
import time
import random
import uuid
from discord import *
from discord.ext import commands
from config import settings
from simpledemotivators import Demotivator
import markovify



bot = commands.Bot(command_prefix=settings['prefix'], intents = Intents.all())

client = Client()


#@bot.command()
#async def markov(ctx):



@bot.command()
async def copy(ctx):
    with open("file.txt", "w", encoding='utf-8') as f:
        async for message in ctx.history(limit=2000):
            f.write(message.content + "\n")

@bot.command()
async def members(ctx):
    for guild in bot.guilds:
        list = []
        for member in guild.members:
            list.append(member.name)

        str_mem = '\n'.join(list)
        await ctx.send(f"юзеры:\n{str_mem}")



@bot.command(aliases=["ch-nickname"])
async def nick(ctx, user: Member, nickname):
  await user.edit(nick=nickname)

@bot.command()
async def bothelp(ctx):
    await ctx.send("команды:\n.d[фото, текст](демотиватор)\n.m-c[@юзер](кол-во сообщений юзера)\n.ch-nickname[юзер, старый, новый](смена никнейма юзеру)")


async def background_task():
    await client.wait_until_ready()
    channel = client.get_channel(830053430151610390)
    time = 5
    await asyncio.sleep(time)
    with open("file.txt", encoding='utf-8', mode='r') as f:
        text = f.read()

    text_model = markovify.NewlineText(text, state_size=1)

    for i in range(1):
        await channel.send(text_model.make_short_sentence(40))
@bot.command()
async def привет(ctx):
    await ctx.send(f'привет, безмамный. лучше отъебись')


@bot.command()
async def d(ctx):

    global snd, fst
    imageName = str(uuid.uuid4()) + '.png'

    await ctx.message.attachments[0].save(imageName)
    os.rename(imageName, "demotivator.png")
    with open("file.txt", encoding='utf-8', mode='r') as f:
        text = f.read()

    text_model = markovify.NewlineText(text, state_size=1)
    for i in range(1):
       fst = text_model.make_short_sentence(random.randint(15, 30))
    for i in range(1):
       snd = text_model.make_short_sentence(random.randint(15, 30))
    dem = Demotivator(str(fst), str(snd))

    time.sleep(0.5)
    dem.create('demotivator.png')
    with open('demresult.jpg', 'rb') as f:
        picture = File(f)
        await ctx.send(file=picture)
    os.remove('demotivator.png')



@bot.command(aliases=["m-c"])
async def messages(ctx, user: Member):
    channel = ctx.message.channel
    counter = 0
    async for message in channel.history():
        if message.author == user:
            counter += 1
    await ctx.send(f'{user} отправил {counter} сообщений.')


bot.loop.create_task(background_task())
bot.run(settings['token'])
