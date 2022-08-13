import discord
import asyncio
from captcha.image import ImageCaptcha
import random
import string
import config

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  async def message(games):
    await client.wait_until_ready()
    while not client.is_closed():
        for game in games:
            await client.change_presence(status = discord.Status.idle, activity = discord.Game(game))
            await asyncio.sleep(10)
  await message(["discord-verify-bot", "디스코드봇으로 쉽게 유저를 인증해요!"])

@client.event
async def on_message(message):
    if message.content.startswith("!인증"):
      if message.channel.id == config.channel:
        randomstr = random.choice(string.ascii_lowercase)+random.choice(string.ascii_lowercase)+random.choice(string.ascii_lowercase)+random.choice(string.ascii_lowercase)+random.choice(string.ascii_lowercase)
        channel = message.channel
        Captcha = ImageCaptcha()
        name = str(f"{message.author.id}.png")
        Captcha.write(randomstr, name)
        embed = discord.Embed(title="[ 인증 ]", description=f"아래의 글자를 입력해주세요! 소문자입니다!", color=0x2f3136)
        await message.channel.send(embed=embed)
        await message.channel.send(file=discord.File(name))
        def check(m):
            return m.content == randomstr and m.channel == channel and m.author == message.author
        try:
          await client.wait_for('message', timeout=10.0, check=check)
        except asyncio.TimeoutError:
          embed = discord.Embed(title="[ 인증 ]", description="인증에 실패했습니다!", color=0x2f3136)
          await message.channel.send(embed=embed)
        else:
          role = discord.utils.get(message.guild.roles, name=config.role)
          await message.author.add_roles(role)
          embed = discord.Embed(title="[ 인증 ]", description="인증에 성공했습니다!", color=0x2f3136)
          await message.channel.send(embed=embed)
      else:
          embed = discord.Embed(title="[ 인증 ]", description="이미 인증이 된거같아요!", color=0x2f3136)
          await message.channel.send(embed=embed)

client.run(config.token)
