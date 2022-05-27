# Environment: .\env\Scripts\Activate.ps1
import discord # python -m pip install discord.py
import random
import re

props = {}

def load(sep='=', comment_char='#'):
  with open("./credentials.properties", "r") as f:
    for line in f:
      stripline = line.strip()
      if stripline and not stripline.startswith(comment_char):
        key_value = stripline.split(sep)
        key = key_value[0].strip()
        value = sep.join(key_value[1:]).strip().strip('"')
        props[key] = value

def roll(num):
  results = [random.randint(1, 20) for i in range (0, num)]
  successes = sum(1 for i in results if i > 10)
  print([results, successes])
  return successes

def parse(ch):
  # format d#1-#2: #1 is the number of rolls, #2 is the required number of successes
  parts = ch.split("-")
  # Get the number of dice
  num = int(parts[0][1:])
  successes = roll(num)
  if len(parts) > 1:
    successes -= int(parts[1])
  return successes

def check(msg):
  print(">>> " + msg)
  # Split the message into its parts
  parts = msg.split(" ")
  # Second part is the initiator of the action
  initiator = parse(parts[1])
  # Forth part is the opponent
  opponent = 0
  if len(parts) > 3:
    opponent = parse(parts[3])
  return initiator - opponent

# message = "!check d7"
# message = "!check d6-2"
# message = "!check d4-1 vs d6-2"
# print(check(message))

load()
# print(props)

# intents = discord.Intents.default()
# intents.message_content = True

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  # If the message pattern is not correct, send back a message to the user with the proper format.
  if message.content.startswith('!check'):
    msg = "Degree of success: "
    try:
      msg += str(check(message.content))
    except:
      msg = "Expected format: !check d#1-#2 vs d#3-#4\n - #1: initiator's skill, #2 initiator's difficulty\n - #3: opponent's skill, #2 opponent's difficulty\n ! Note that the opponent's stuff are optional!"
    await message.channel.send(msg)

client.run(props["clientSecret"])
