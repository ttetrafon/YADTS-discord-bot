# Environment: .\env\Scripts\Activate.ps1
import discord # python -m pip install discord.py
import random
import re
import traceback

props = {}

def load(sep='=', comment_char='#'):
  with open("./credentials.properties", "r") as f:
    for line in f:
      stripLine = line.strip()
      if stripLine and not stripLine.startswith(comment_char):
        key_value = stripLine.split(sep)
        key = key_value[0].strip()
        value = sep.join(key_value[1:]).strip().strip('"')
        props[key] = value

def roll(num):
  results = [random.randint(1, 20) for i in range (0, num)]
  results.sort()
  successes = sum(1 for i in results if i > 10)
  return [results, successes]

def parse(ch):
  # format d#1-#2: #1 is the number of rolls, #2 is the required number of successes
  parts = ch.split("-")
  # Get the number of dice
  num = int(parts[0][1:])
  results = roll(num)
  print(results)
  description = results[0]
  successes = results[1]
  if len(parts) > 1:
    successes -= int(parts[1])
  return [description, successes]

def check(msg):
  print(">>> " + msg)
  # Split the message into its parts
  parts = msg.split(" ")
  # Second part is the initiator of the action
  initiator = parse(parts[1])
  result = initiator[1]
  print("result (1):")
  print(result)
  description = "[" + ", ".join(map(str, initiator[0])) + "]"
  # Forth part is the opponent
  if len(parts) > 3:
    opponent = parse(parts[3])
    result = result - opponent[1]
    print("result (2):")
    print(result)
    description = description + " vs [" + ", ".join(map(str, opponent[0])) + "]"
  return str(result) + "\n> " + description

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
    msg = "Result: "
    try:
      msg += str(check(message.content))
    except:
      traceback.print_exc()
      msg = "Expected format: !check d#1-#2 vs d#3-#4\n - #1: initiator's skill, #2 initiator's difficulty\n - #3: opponent's skill, #2 opponent's difficulty\n ! Note that the opponent's stuff (vs) are optional!"
    await message.channel.send(msg)

client.run(props["clientSecret"])
