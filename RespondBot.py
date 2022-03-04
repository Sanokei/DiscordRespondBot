#!/usr/bin/env python
# coding: utf-8

from profanity_filter import ProfanityFilter
from configparser import ConfigParser
from nextcord.ext import commands
from spacy.lang.en import English
import openai
import random
import re

client = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
pf = ProfanityFilter()
message_history = {}
username_history = []
npl = English()
sbd = npl.create_pipe("sentencizer")
npl.add_pipe(sbd)

config = ConfigParser()
config.read('config.cfg')

openai.api_key = config['keys']['openai']
token = config['keys']['discord']
bot_name = config['bot']['name']
prompt = config['bot']['prompt']

def scroll_array(new, channel):
    #Adds the new message to the beginning and removes the last message from the array
    global message_history
    history = get_history_by_channel(channel)
    history.insert(0,new)
    history.pop()
    message_history[channel] = history

def remove_empty_strings(array: list):
    #Removes empty strings from the array
    temp = array.copy()
    while "" in temp:
        temp.remove("")
    return temp

def get_formatted_chat(message, ctx):
    output = ""
    history = remove_empty_strings(get_history_by_channel(ctx.channel.id))
    
    #Change between bot and user
    for i in range(len(history)):
        if i%2 == 0:
            output = f"\n{bot_name}: {history[i]}" + output
        else:
            output = "\n" + history[i] + output
            
    if not message == "":
        output += f"\n{ctx.author.name}: {message}\n{bot_name}: "
        
    return output

def get_history_by_channel(channel):
    global message_history
    if not channel in message_history:
        message_history[channel] = [""]*10
    return message_history[channel]
    
def replace_ats(message):
    t = message.content.replace(client.user.mention, '')
    match = re.search(r'<@!*&*[0-9]+>', t)
    if not match == None:
        temp = t.split(">")
        text = ">".join(temp[1:])
    else:
        text = t
    return text
    
@client.event
async def on_connect():
    print(f"""
        Client has successfully logged in as {client.user.name}#{client.user.discriminator}
        Your discord ID is {client.user.id}
    """)
    username_history.append(bot_name)
    
@client.command()
async def history(ctx):
    message = get_formatted_chat("", ctx)
    if message == "":
        message = "No memories yet"
    await ctx.send(f"```{message}```")
    
@client.command()
async def reset(ctx):
    global message_history
    message_history[ctx.channel.id] = [""] * len(get_history_by_channel(ctx.channel.id))
    await ctx.send("Memories reset")
    
@client.command()
async def memory(ctx, *, limit):
    global message_history
    difference = int(limit) - len(get_history_by_channel(ctx.channel.id))
    if difference > 0:
        for i in range(difference):
            message_history[ctx.channel.id].append("")
    elif difference < 0:
        message_history[ctx.channel.id] = message_history[ctx.channel.id][:int(limit)]
    
    await ctx.send(f"Memory limit set to {len(message_history[ctx.channel.id])}")
    
@client.event
async def on_message(ctx):
    message = pf.censor(replace_ats(ctx))
    
    if ctx.author.bot:
        return
    if not client.user.mentioned_in(ctx):
        await client.process_commands(ctx)  
        return
    
    #Fake Typing Effect
    async with ctx.channel.typing():
        global username_history
        print(f"{ctx.author.name}#{ctx.author.discriminator} said: {message}")
        
        if not ctx.author.name in username_history:
            username_history.append(ctx.author.name)
        
        temperature = random.uniform(0.8, 1.0)
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"The following is a conversation with a group of friends. {prompt}\n{get_formatted_chat(message, ctx)}",
            temperature=temperature,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=username_history
        )
        
        doc = npl(response.choices[0].text)
        sents = [sent.string.strip() for sent in doc.sents]
        
        scroll_array(f"{ctx.author.name}: {message}", ctx.channel.id)
        scroll_array(sents[0], ctx.channel.id)
        
    await ctx.reply(response.choices[0].text)
    
client.run(token)
