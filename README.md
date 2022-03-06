# Discord Respond Bot
Uses GPT-3 to allow you to talk to a version of yourself using GPT-3

Edit the config.cfg
```txt
[keys]
openai = Open AI API key
discord = discord api token

[bot]
name = name the bot
prompt = about yourself using the 'Friend:' '{Bot Name}:' keywords. Use the bot name you have choosen
```
```python
# the prompt already has the filler
# 'This is a conversation between a Human and Friends.'

# what you really need to do is add info about yourself then add
# example text for what you would say
'''
The Human is [adjectives that describe you]

Friend: Hey whats up?
Human: I dont know the ceiling in my room? thats a dum question
Friend: Do you like baseball?
Human: God no, but i like esports
'''
```
