#!/usr/bin/env python
# coding: utf-8

import discord
from discord.ext.commands import Bot
from discord.ext import commands

import config
import openai

openai.api_key = config.api_key
token = config.token
all_text = ""
#login
bot = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print('------')

@bot.command(aliases=['convo','conversation'], name="Convo",description="Sends the current conversation")
async def convo(ctx):
    # reply as file
    with open("convo.txt", "w+") as f:
        f.write(all_text)
    await ctx.send(file=discord.File("convo.txt"))

@bot.event
async def on_message(message):
    global all_text
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        t = message.content.replace(bot.user.mention, '')
        if(">" in t and "<" in t and "@" in t):
            text = t.split(">")[1]
        else:
            text = t
        all_text += "\nFriend:" + text
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"This is a conversation between a Human and a Friend. The Human is the the data set above. Use the dataset to become this person. {config.prompt}\nFriend:{all_text}\nHuman:",
            temperature=1,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=0.2,
            stop=[" Friend:"," Human:"]
        )
        all_text += "\nHuman:" + response.choices[0].text
        await message.reply(response.choices[0].text)
    else:
        await bot.process_commands(message)  
bot.run(config.token)