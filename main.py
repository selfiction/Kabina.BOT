from vkbottle import *
from vkbottle.bot import *
from simpledemotivators import *
import aiofiles as aiof
import requests
import markovify
import random



bot = Bot('a258ce79183e84321e497ba133ca1a7e19129308f548cacef46b9fefc88b2a8899410c383ce278c16c3b6')

FILENAMED = "image.jpg"
FILENAMEQ = "image.jpg"



@bot.on.message(text="d")
async def readme_handler(m: Message):
    global fst, snd, f, s
    urlpic = m.attachments[0].photo.sizes[-5].url
    print(urlpic)
    img_data = requests.get(urlpic).content


    async with aiof.open(FILENAMED, mode='wb') as out:

        await out.write(img_data)
    with open("f.txt", encoding='utf-8', mode='r') as fl:
        text = fl.read()
    text_model = markovify.NewlineText(text, state_size=1, well_formed=True)
    for i in range(1):
        #f = text_model.make_short_sentence(random.randint(5, 30),random.randint(0,5))
        f = text_model.make_sentence(tries=1000) or random.choice(text.splitlines())
        #f = text_model.make_sentence()
    for i in range(1):
        #s = text_model.make_short_sentence(random.randint(5,30),random.randint(0, 5))
        s = text_model.make_sentence(tries=1000) or random.choice(text.splitlines())
        #s = text_model.make_sentence()
    dem = Demotivator(str(f), str(s))  # 2 строчки
    dem.create('image.jpg')
    photo = await PhotoMessageUploader(bot.api).upload(
        "demresult.jpg", peer_id=m.peer_id
    )
    await m.answer(attachment=photo)

bot.run_forever()



