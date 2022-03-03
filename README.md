<h1><strong>WARNING:</h1></strong>
  <h1><strong>
  USE AT YOUR OWN RISK. DISCORD AS OF MAY 19TH HAVE OUTRIGHT BANNED USER-BOTS.
  THEY CAN TELL IF YOU ARE USING ONE WITH THE TYPE OF TOKEN YOU PARSE.
  USE THIS AT YOUR OWN RISK. ASSUME YOU WILL GET BANNED USING THIS PROGRAM.
  
  READ THE UPDATED GUIDELINES <a href=https://discord.com/guidelines>HERE</a>
</strong></h1>

# Discord Respond Bot
Uses GPT-3 to allow you to respond to messages without messaging anybody

Create a config.py file with two variables
```python
token = "discord api token"
api_key = "Open AI API key"
prompt = "about yourself using the \'Friend:\'\'Human:\' keywords. You are the Human"
# the prompt already has the filler
# 'This is a conversation between a Human and a Friend.'

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
