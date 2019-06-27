#id 593316048942399507
#prem 67584
# https://discordapp.com/oauth2/authorize?client_id=593316048942399507&scope=bot&premissions=67584

import discord
import sqlite3
import urllib.request
import random
from meme_create import meme_overlap

with open("../RoastMeMeBotData.txt") as data:    ## For token
    token = data.read().rstrip()                 ## security

conn = sqlite3.connect("data/roasts.db")
c = conn.cursor()

client = discord.Client()

@client.event
async def on_ready():
    print(f"[INF] Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.content.lower() == "#help":
        embed = discord.Embed(title="Help Menu")
        embed.add_field(name="#help", value="Shows this menu", inline=False)
        embed.add_field(name="#roastmeme", value="Roasts you", inline=False)
        embed.add_field(name="#roast [username]", value="Roasts [username], but you have to roast yourself 2 times for each roast you preform on another user", inline=False)
        embed.add_field(name="#roasts", value="Shows you how many times you've roasted yourself (decreases by 2 each time you use the 3rd command - '#roast [username]')", inline=False)
        await message.channel.send(embed=embed)
    elif message.content.lower() == "#roastmeme":
        c.execute(f"SELECT * FROM roasts WHERE id={message.author.id}")
        fetched = c.fetchone()
        if fetched:
            c.execute(f"UPDATE roasts SET roasts = :roasts WHERE id={message.author.id}", {"roasts": fetched[1] + 1})
        else:
            c.execute(f"INSERT INTO roasts VALUES (?, ?)", (message.author.id, 1))
        conn.commit()

        idd = random.randint(0, 1000000)
        memerand = random.randint(0, 1)

        opener = urllib.request.URLopener()
        opener.addheader("User-Agent", "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0")
        opener.retrieve(str(message.author.avatar_url).replace(".webp", ".png"), f"resources/temp/avatar_{idd}.png")

        memeid = meme_overlap(str(memerand), idd, message.author.name)

        await message.channel.send(files=[discord.File(f"resources/temp/meme_{memeid}.png")])
    elif message.content.lower() == "#roasts":
        c.execute(f"SELECT * FROM roasts WHERE id={message.author.id}")
        fetched = c.fetchone()

        if not fetched:
            c.execute(f"INSERT INTO roasts VALUES (?, ?)", (message.author.id, 0))
            fetched = (None, 0)
            conn.commit()

        embed=discord.Embed(title="Roasts", description=f"You, {message.author.name}, have {fetched[1]} self-roasts stored")
        await message.channel.send(embed=embed)
    elif len(message.content.split()) == 2 and message.content.split()[0].lower() == "#roast" and message.content.split()[1][:2] == "<@" and message.content.split()[1][-1] == ">":
        c.execute(f"SELECT * FROM roasts WHERE id={message.author.id}")
        fetched = c.fetchone()
        if fetched:
            if fetched[1] < 2:
                embed=discord.Embed(title="Roasts", description=f"You, {message.author.name}, don't have enough self-roasts stored (you need at least 2 and you have {fetched[1]})")
                await message.channel.send(embed=embed)
            else:
                c.execute(f"UPDATE roasts SET roasts = :roasts WHERE id={message.author.id}", {"roasts": fetched[1] - 2})
                conn.commit()

                idd = random.randint(0, 1000000)
                memerand = random.randint(0, 1)

                opener = urllib.request.URLopener()
                opener.addheader("User-Agent", "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0")
                opener.retrieve(str(message.mentions[0].avatar_url).replace(".webp", ".png"), f"resources/temp/avatar_{idd}.png")

                memeid = meme_overlap(str(memerand), idd, message.mentions[0].name)

                await message.channel.send(files=[discord.File(f"resources/temp/meme_{memeid}.png")])
        else:
            c.execute(f"INSERT INTO roasts VALUES (?, ?)", (message.author.id, 0))
            conn.commit()
            embed=discord.Embed(title="Roasts", description=f"You, {message.author.name}, don't have enough self-roasts stored (you need at least 2 and you have 0)")
            await message.channel.send(embed=embed)

client.run(token)
