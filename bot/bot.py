import discord
import sqlite3
import urllib.request
import random
from meme_create import meme_overlap
import logging
import os
import os.path
import fnmatch

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] [%(asctime)s] - %(message)s")

prefix = "rt#"
cache = "disable"

with open("bot/bot.cfg") as data:
    for line in data:
        line = line.strip()
        if line[:7] == "prefix=":
            try:
                prefix = line[8:-1]
            except IndexError:
                logging.error(f"Incorrect bot.cfg setting: {line}")
        elif line[:6] == "cache=":
            try:
                cache = line[7:-1]
            except IndexError:
                loggin.error(f"Incorrect bot.cfg setting: {line}")
        elif line:
            logging.warning(f"Unexpected bot.cfg setting: {line}")


conn = sqlite3.connect("data/roasts.db")
c = conn.cursor()

client = discord.Client()

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.content.lower() == f"{prefix}help":
        logging.info(f"{message.author.name} ran '{message.content.lower()}' at server {message.guild.name} channel #{message.channel.name}")

        embed = discord.Embed(title="Help Menu")
        embed.add_field(name=f"{prefix}help", value="Shows this menu", inline=False)
        embed.add_field(name=f"{prefix}roastmeme", value="Roasts you", inline=False)
        embed.add_field(name=f"{prefix}roast [username]", value="Roasts [username], but you have to roast yourself 2 times for each roast you preform on another user", inline=False)
        embed.add_field(name=f"{prefix}roasts", value="Shows you how many times you've roasted yourself (decreases by 2 each time you use the 3rd command - '#roast [username]')", inline=False)
        await message.channel.send(embed=embed)
    elif message.content.lower() == f"{prefix}roastmeme":
        logging.info(f"{message.author.name} ran '{message.content.lower()}' at server {message.guild.name} channel #{message.channel.name}")

        c.execute(f"SELECT * FROM roasts WHERE id={message.author.id}")
        fetched = c.fetchone()
        if fetched:
            c.execute(f"UPDATE roasts SET roasts = :roasts WHERE id={message.author.id}", {"roasts": fetched[1] + 1})
        else:
            c.execute(f"INSERT INTO roasts VALUES (?, ?)", (message.author.id, 1))
        conn.commit()

        memerand = random.randint(0, len(fnmatch.filter(os.listdir("resources/memes/"), "*.png")) - 1)

        if not os.path.isfile(f"resources/temp/avatar_{message.author.id}.png"):
            opener = urllib.request.URLopener()
            opener.addheader("User-Agent", "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0")
            opener.retrieve(str(message.author.avatar_url).replace(".webp", ".png"), f"resources/temp/avatar_{message.author.id}.png")
            logging.info(f"Retrieved {message.author.name}'s avatar")
        if not os.path.isfile(f"resources/temp/meme_{memerand}_{message.author.id}.png"):
            meme_overlap(str(memerand), message.author.id, message.author.name)
            logging.info(f"Overlapped meme_{memerand} for {message.author.name}")

        await message.channel.send(file=discord.File(f"resources/temp/meme_{memerand}_{message.author.id}.png"))
        if cache != "enable":
            os.remove(f"resources/temp/meme_{memerand}_{message.author.id}.png")
            os.remove(f"resources/temp/avatar_{message.author.id}.png")

    elif message.content.lower() == f"{prefix}roasts":
        logging.info(f"{message.author.name} ran '{message.content.lower()}' at server {message.guild.name} channel #{message.channel.name}")

        c.execute(f"SELECT * FROM roasts WHERE id={message.author.id}")
        fetched = c.fetchone()

        if not fetched:
            c.execute(f"INSERT INTO roasts VALUES (?, ?)", (message.author.id, 0))
            fetched = (None, 0)
            conn.commit()

        embed=discord.Embed(title="Roasts", description=f"You, {message.author.name}, have {fetched[1]} self-roasts stored")
        await message.channel.send(embed=embed)
    elif len(message.content.split()) == 2 and message.content.split()[0].lower() == f"{prefix}roast" and message.content.split()[1][:2] == "<@" and message.content.split()[1][-1] == ">":
        logging.info(f"{message.author.name} ran '{message.content.lower()}' at server {message.guild.name} channel #{message.channel.name}")

        c.execute(f"SELECT * FROM roasts WHERE id={message.author.id}")
        fetched = c.fetchone()
        if fetched:
            if fetched[1] < 2:
                embed=discord.Embed(title="Roasts", description=f"You, {message.author.name}, don't have enough self-roasts stored (you need at least 2 and you have {fetched[1]})")
                await message.channel.send(embed=embed)
            else:
                c.execute(f"UPDATE roasts SET roasts = :roasts WHERE id={message.author.id}", {"roasts": fetched[1] - 2})
                conn.commit()

                try:
                    message.mentions[0]

                    memerand = random.randint(0, len(fnmatch.filter(os.listdir("resources/memes/"), "*.png")) - 1)

                    if not os.path.isfile(f"resources/temp/avatar_{message.mentions[0].id}.png"):
                        opener = urllib.request.URLopener()
                        opener.addheader("User-Agent", "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0")
                        opener.retrieve(str(message.mentions[0].avatar_url).replace(".webp", ".png"), f"resources/temp/avatar_{message.mentions[0].id}.png")
                        logging.info(f"Retrieved {message.author.name}'s avatar")
                    if not os.path.isfile(f"resources/temp/meme_{memerand}_{message.mentions[0].id}.png"):
                        meme_overlap(str(memerand), message.mentions[0].id, message.mentions[0].name)
                        logging.info(f"Overlapped meme_{memerand} for {message.mentions[0].name}")

                    await message.channel.send(file=discord.File(f"resources/temp/meme_{memerand}_{message.mentions[0].id}.png"))
                    if cache != "enable":
                        os.remove(f"resources/temp/meme_{memerand}_{message.mentions[0].id}.png")
                        os.remove(f"resources/temp/avatar_{message.mentions[0].id}.png")

                except IndexError:
                    embed=discord.Embed(title="Error", description=f"You, {message.author.name}, tried to roast a non-existing user, please try again")
                    await message.channel.send(embed=embed)
        else:
            c.execute(f"INSERT INTO roasts VALUES (?, ?)", (message.author.id, 0))
            conn.commit()
            embed=discord.Embed(title="Roasts", description=f"You, {message.author.name}, don't have enough self-roasts stored (you need at least 2 and you have 0)")
            await message.channel.send(embed=embed)
    elif message.content[:len(prefix) + 6] == f"{prefix}roast ":
        logging.info(f"{message.author.name} ran '{message.content.lower()}' at server {message.guild.name} channel #{message.channel.name}")

        embed=discord.Embed(title="Error", description=f"You, {message.author.name}, tried to roast a non-existing user, please try again")
        await message.channel.send(embed=embed)

client.run("NTkzMzE2MDQ4OTQyMzk5NTA3.XRRO1g.kRsI0p2jVO2mHZlreOVL3Y4xYw4")
