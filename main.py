import discord
import os
import random
import giphy_client
from discord.ext import commands 
from keep_alive import keep_alive
from giphy_client.rest import ApiException
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=";", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status, activity=discord.Game("type ;commands"))
    print(f"Bot is now online {client.user}")

eight_ball_responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.", 
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
]

#8ball command
@client.command()
async def eightball(ctx):
    response = random.choice(eight_ball_responses)
    await ctx.channel.send("`" + response + "`")

#Coinflip command
@client.command()
async def coinflip(ctx):
    result = random.randint(1, 2)
    if result == 1:
        await ctx.channel.send("`Heads`")
    if result == 2:
        await ctx.channel.send("`Tails`")

#Poll command
@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

#GIF command
@client.command()
async def gif(ctx,*,q="GIF"):

    api_key = 'HJ3CAg2TP3Gr7LGMv9MPQwWYmveIyOan'
    api_instance = giphy_client.DefaultApi()

    try:
        api_response=api_instance.gifs_search_get(api_key,q,limit=100,rating='r')
        lst = list(api_response.data)
        giff = random.choice(lst)
        await ctx.channel.send("From Giphy:")
        await ctx.channel.send(f"https://giphy.com/gifs/{giff.id}")

    except ApiException as e:
        print("ApiException when calling Api.")

# News command
@client.command()
async def news(ctx):
    link = 'https://www.cnbc.com/world/?region=world'
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    headlines = soup.find_all("a", class_='LatestNews-headline')
    links = [headline['href'] for headline in headlines]
    headline_texts = [headline.text.strip() for headline in headlines]
    
    time_news = soup.find_all("span", class_='LatestNews-wrapper')
    for i in range(10):
        await ctx.channel.send(f"Article headline {i+1}: {headline_texts[i]}\nLink: {links[i]}\nTime: {time_news[i].text.strip()}")

@client.command()
async def commands(ctx):
    await ctx.channel.send("`;poll [user_input] - creates a poll\n;eightball - magic 8ball\n;coinflip - heads or tails\n;gif [user_input] - sends GIF\n;news - 10 latest CNBC articles`")

keep_alive()
TOKEN = os.environ.get('SECRET_DISCORD_TOKEN')
client.run(TOKEN)
