#!/usr/bin/env python
# coding: utf-8

import discord

import config
import openai
openai.api_key = config.api_key
token = config.token
class Client(discord.Client):
    async def on_connect(self):
        print(f"""
            Client has successfully logged in as {client.user.name}#{client.user.discriminator}
            Your discord ID is {client.user.id}
        """)
    
    async def on_message(self, message):
        if message.author != client.user:
            return
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"This is a conversation between a Human and a Friend.\n{config.prompt}\nFriend:{message.content}\nHuman:",
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Friend:"," Human:"]
        )
        await message.channel.send(response.choices[0].text)
        
client = Client()
try:
    client.run(token, bot = False)
except discord.LoginFailure:
    print("ERROR: Client failed to log in. [Invalid token]")
except discord.HTTPException:
    print("ERROR: Client failed to log in. [Unknown Error]")