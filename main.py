import discord
import os
import random
import giphy_client
import requests
from discord.ext import commands 
from keep_alive import keep_alive
from giphy_client.rest import ApiException
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

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

@client.command()
async def eightball(ctx):
    response = random.choice(eight_ball_responses)
    await ctx.channel.send("`" + response + "`")

@client.command()
async def coinflip(ctx):
    result = random.randint(1, 2)
    if result == 1:
        await ctx.channel.send("`Heads`")
    if result == 2:
        await ctx.channel.send("`Tails`")

@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

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
        
@client.command()
async def news(ctx):
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
  
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='gs-c-promo-body')
    unwanted = ['BBC World News TV', 'BBC World Service Radio',
                'News daily newsletter', 'Mobile app', 'Get in touch']
  
    count = 0

    for article in articles:
        article_title = article.find('h3').get_text(strip=True)
        if article_title not in unwanted and count < 10:
            article_link = article.find('a')['href'] if article.find('a') else 'No link available'
            article_date = article.find('time')['datetime']
            utc_time = datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            pst_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-8)))
            formatted_date = pst_time.strftime("%d %b %Y, %I:%M %p %Z")
            await ctx.channel.send(f"`{article_title}`\nArticle Link: bbc.com{article_link}\nPublished on: {formatted_date}")
            count += 1
            if count >= 10: #10 articles 
                break

@client.command()
async def commands(ctx):
    await ctx.channel.send("`;poll [user_input] - creates a poll\n;eightball - magic 8ball\n;coinflip - heads or tails\n;gif [user_input] - sends GIF\n;news - current top 10 BBC articles`")

keep_alive()
TOKEN = os.environ.get('SECRET_DISCORD_TOKEN')
client.run(TOKEN)
