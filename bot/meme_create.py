from PIL import Image, ImageFont, ImageDraw
import random

def meme_overlap(meme_id, avatar_id, username="Roasted"):
    meme = Image.open(f"resources/memes/meme_{meme_id}.png")
    avatar = Image.open(f"resources/temp/avatar_{avatar_id}.png")

    if meme_id == "0":
        area = (55, 5, 130, 80)
        temp1 = meme.copy()
        temp2 = avatar.copy()
        temp2 = temp2.resize((75, 75), Image.ANTIALIAS)
        temp1.paste(temp2, area)

        helvetica = ImageFont.truetype("resources/fonts/arial.ttf", size=15)
        d = ImageDraw.Draw(temp1)

        location = (140, 20)
        text_color = (255, 255, 255)
        d.text(location, username, font=helvetica, fill=text_color)

        temp_meme_id = random.randint(0, 1000000)

        temp1.save(f"resources/temp/meme_{temp_meme_id}.png")

    elif meme_id == "1":
        area = (30, 10, 105, 85)
        temp1 = meme.copy()
        temp2 = avatar.copy()
        temp2 = temp2.resize((75, 75), Image.ANTIALIAS)
        temp1.paste(temp2, area)
        area = (30, 140, 105, 215)
        temp2 = temp2.resize((75, 75), Image.ANTIALIAS)
        temp1.paste(temp2, area)
        area = (80, 270, 200, 390)
        temp2 = temp2.resize((120, 120), Image.ANTIALIAS)
        temp1.paste(temp2, area)

        temp_meme_id = random.randint(0, 1000000)

        temp1.save(f"resources/temp/meme_{temp_meme_id}.png")

    return temp_meme_id
