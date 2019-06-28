from PIL import Image, ImageFont, ImageDraw
import random
import logging

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] [%(asctime)s] - %(message)s")

def meme_overlap(meme_id, avatar_id, username):
    meme = Image.open(f"resources/memes/meme_{meme_id}.png")
    avatar = Image.open(f"resources/temp/avatar_{avatar_id}.png")

    d = ImageDraw.Draw(meme)

    logging.info(f"Starting meme_overlap({meme_id}, {avatar_id}, {username})")

    try:
        with open(f"resources/memes/meme_{meme_id}.cfg") as config:
            for liner in config:
                liner = liner.strip()

                if liner[:5] == "font=":
                    try:
                        line = liner[6:-1].split()
                        font = ImageFont.truetype(f"resources/fonts/{line[0]}.ttf", size=int(line[1]))
                        font_color = (int(line[2]), int(line[3]), int(line[4]))
                    except (IndexError, ValueError, OSError):
                        logging.error(f"Incorrect meme_{meme_id}.cfg setting: {liner}")
                elif liner[:8] == "textpos=":
                    try:
                        line = liner[9:-1].split()
                        d.text((int(line[0]), int(line[1])), username, font=font, fill=font_color)
                    except (IndexError, ValueError, NameError):
                        logging.error(f"Incorrect meme_{meme_id}.cfg setting: {liner}")
                elif liner[:10] == "avatarpos=":
                    try:
                        line = liner[11:-1].split()
                        avatar_temp = avatar.resize((int(line[2]) - int(line[0]), int(line[3]) - int(line[1])))
                        meme.paste(avatar_temp, (int(line[0]), int(line[1]), int(line[2]), int(line[3])))
                    except (IndexError, ValueError):
                        logging.error(f"Incorrect meme_{meme_id}.cfg setting: {liner}")
                elif liner:
                    logging.warning(f"Unexpected meme_{meme_id}.cfg setting: {liner}")
    except FileNotFoundError:
        logging.error(f"File 'resources/memes/meme_{meme_id}.cfg' doesn't exist")

    meme.save(f"resources/temp/meme_{meme_id}_{avatar_id}.png", compress_level=1)
