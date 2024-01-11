import discord
import os
import random
import giphy_client
from discord.ext import commands 
from keep_alive import keep_alive
from giphy_client.rest import ApiException
import requests
from bs4 import BeautifulSoup
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=";", help_command=None, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status, activity=discord.Game("type ;help"))
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

# Initial news prompt
@client.command()
async def news(ctx):
    message = await ctx.send('What category would you like to see? \n :computer:  Technology \n :earth_americas:  Politics \n :star:  Celebrities \n :flag_kr:  K-Pop')
    
    tech = '💻'
    politics = '🌎'
    celebrity = '⭐'
    kpop = '🇰🇷'

    await message.add_reaction(tech)
    await message.add_reaction(politics)
    await message.add_reaction(celebrity)
    await message.add_reaction(kpop)

    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) in [tech, politics, celebrity, kpop]

    member = ctx.author

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)

            if str(reaction.emoji) == tech:
                await technews(ctx)
            elif str(reaction.emoji) == politics:
                await politicsnews(ctx)
            elif str(reaction.emoji) == celebrity:
                await celebritynews(ctx)
            elif str(reaction.emoji) == kpop:
                await kpopnews(ctx)
        except asyncio.TimeoutError:
            break

# Tech news command
@client.command()
async def technews(ctx):
    link = 'https://www.cnbc.com/technology/'
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    headlines = soup.find_all("a", class_='Card-title')
    links = [headline['href'] for headline in headlines]
    headline_texts = [headline.text.strip() for headline in headlines]

    time_news = soup.find_all("span", class_='Card-time')
    for i in range(3):
        await ctx.channel.send(f"__`Article headline {i+1}:`__ " + headline_texts[i] + "\n__`Link:`__ " + links[i] + "\n__`Time:`__ " + time_news[i].text.strip())

# Politic news command
@client.command()
async def politicsnews(ctx):
    link = 'https://www.cnbc.com/politics/'
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    headlines = soup.find_all("a", class_='Card-title')
    links = [headline['href'] for headline in headlines]
    headline_texts = [headline.text.strip() for headline in headlines]

    time_news = soup.find_all("span", class_='Card-time')
    for i in range(3):
        await ctx.channel.send(f"__`Article headline {i+1}:`__ " + headline_texts[i] + "\n__`Link:`__ " + links[i] + "\n__`Time:`__ " + time_news[i].text.strip())

# Social media trend news command
@client.command()
async def celebritynews(ctx):
    link = 'https://www.usmagazine.com/tag/exclusive/'
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    headlines = soup.find_all("a", class_='content-card-link')
    links = [headline['href'] for headline in headlines]
    headline_texts = [headline.find('div', class_='content-card-title').text.strip() for headline in headlines]

    for i in range(3):
        await ctx.channel.send(f"__`Article headline {i+1}:`__ " + headline_texts[i] + "\n__`Link:`__ " + links[i])

# Kpop news command
@client.command()
async def kpopnews(ctx):
    link = 'https://www.scmp.com/k-pop/news'
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    headlines = soup.find_all("a", class_='article__link')
    links = [headline['href'] for headline in headlines]
    headline_texts = [headline.text.strip() for headline in headlines]
    for i in range(3):
        await ctx.channel.send(f"__`Article headline {i+1}:`__ " + headline_texts[i] + "\n__`Link:`__ " + links[i])

# Help command
@client.command()
async def help(context):
    await context.channel.send("`;poll [user_input] - creates a poll\n;eightball - magic 8ball\n;coinflip - heads or tails\n;gif [user_input] - sends GIF\n;news - news articles`")

keep_alive()
TOKEN = os.environ.get('SECRET_DISCORD_TOKEN')
client.run(TOKEN)
