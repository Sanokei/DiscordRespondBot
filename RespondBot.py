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
last_four_responses = []
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
    global all_text
    with open("convo.txt", "w+") as f:
        f.write(all_text)
    await ctx.send(file=discord.File("convo.txt"))

@bot.event
async def on_message(message):
    global all_text
    global last_four_responses
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        t = message.content.replace(bot.user.mention, '')
        if(">" in t and "<" in t and "@" in t):
            text = t.split(">")[1]
        else:
            text = t
        all_text += "\nFriend:" + text
        last_four_responses.append("Friend: "+text)
        if(len(last_four_responses) > 4):
            last_four_responses.pop(0)
        a = ""
        for i in last_four_responses:
            a += i + "\n"
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"This is a conversation between an AI named Human and a Friend.\n{config.prompt}\n{a}\nFriend:{text}\nHuman:",
            temperature=0.9,
            max_tokens=300,
            top_p=0.5,
            frequency_penalty=0.3,
            presence_penalty=0.5,
            stop=["Friend:","Human:"]
        )
        all_text += "\nHuman:" + response.choices[0].text.replace("\n","")
        last_four_responses.append("Human:"+response.choices[0].text.replace("\n",""))
        await message.reply(response.choices[0].text)
    else:
        await bot.process_commands(message)  
bot.run(config.token)