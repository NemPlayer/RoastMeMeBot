import discord
import sqlite3
import requests
import random
from meme_create import meme_overlap
import logging
import os
import os.path
import fnmatch
import io
from PIL import Image

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] [%(asctime)s] - %(message)s")

prefix = "rt#"

with open("bot/bot.cfg") as data:
    for line in data:
        line = line.strip()
        if line[:7] == "prefix=":
            try:
                prefix = line[8:-1]
            except IndexError:
                logging.error(f"Incorrect bot.cfg setting: {line}")
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

        response = requests.get(str(message.author.avatar_url).replace(".webp", ".png"))
        img = Image.open(io.BytesIO(response.content))
        logging.info(f"Retrieved {message.author.name}'s avatar")
        meme = meme_overlap(str(memerand), img, message.author.name)
        logging.info(f"Overlapped meme_{memerand} for {message.author.name}")

        await message.channel.send(file=discord.File(io.BytesIO(meme), filename="meme.png"))

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
                    response = requests.get(str(message.mentions[0].avatar_url).replace(".webp", ".png"))
                    img = Image.open(io.BytesIO(response.content))
                    logging.info(f"Retrieved {message.mentions[0].name}'s avatar")
                    meme = meme_overlap(str(memerand), img, message.mentions[0].name)
                    logging.info(f"Overlapped meme_{memerand} for {message.mentions[0].name}")

                    await message.channel.send(file=discord.File(io.BytesIO(meme), filename="meme.png"))

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

client.run("TOKEN")
