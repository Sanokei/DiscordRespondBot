#!/usr/bin/env python
# coding: utf-8

import discord
from discord.ext.commands import Bot
from discord.ext import commands

import config
import openai

openai.api_key = config.api_key
token = config.token
all_text = config.prompt
#login
bot = discord.Client()
bot = commands.Bot(command_prefix='~at ')
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print('------')


@bot.event
async def on_message(message):
    global all_text
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        text = message.content.replace(bot.user.mention, '')
        all_text += "\n" + text
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"This is a conversation between a Human and a Friend.\n{all_text}\nFriend:{text}\nHuman:",
            temperature=1,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[" Friend:"," Human:"]
        )
        await message.reply(response.choices[0].text)
        
bot.run(config.token)