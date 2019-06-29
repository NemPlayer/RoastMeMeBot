# RoastMeMe Discord bot
RoastMeMe is a Discord bot made for the first Discord Hack Week event. The category RoastMeMe targets is 'shitpost'.

The invitation URL for the bot: https://discordapp.com/oauth2/authorize?client_id=593316048942399507&scope=bot&premissions=67584

### Description
RoastMeMe makes roasting yourself and other users on the server possible trough memes. To keep the roasting fair, anyone who would like to roast another user has to roast themselves 2 times. This brings meaning and will to roasting. The avatar of the user that's being roasted gets placed on the meme, as configured for each meme, together with the user's name - that way the memes feel like actual meme roasts and not just a meme. The memes are contained within the 'resources/memes' (or 'resources\\memes' if you're using Windows) folder. Each meme has a corresponding 'cfg' file, which is used to configure the fonts and placements of user avatars and text in the meme. This makes it easier to add/edit memes (look at the 'Adding/Editing resources' for more information on the topic). Storing data about how many 'roasts' a user has collected is done trough SQLite 3, so that any maintenance of the bot doesn't result in the loss of 'roasts'.

### Commands
RoastMeMe has 4 commands so that the main functionality of the bot becomes as simple to use as possible.
The commands are not including the prefix (by default 'rt#', can be changed in 'bot/bot.cfg' (or 'bot\\bot.cfg' if you're using Windows)):
- *help*, shows the help menu
- *roastmeme*, roasts the user who wrote the command
- *roast @[username]*, roasts the tagged user
- *roasts*, shows you how many times you've roasted yourself (decreases by 2 each time you use the 3rd command - *roast @[username]*)

### Setup
In order to setup the RoastMeMe Discord bot if you want to host it yourself, follow the instructions below in order:
1. Install Python 3
2. Download the RoastMeMeBot GitHub repository
3. Extract it from the ZIP file
4. Enter into the 'RoastMeMeBot-master/bot/bot.cfg' (or 'RoastMeMeBot-master\\bot\\bot.cfg' if you're using Windows) using any text editor and replace the `token="TOKEN"` with `token="[your_token]"` (e.g. `token="a1B2c3D4e5F6g.ABCD123.abcd123-abc123DEF456"`)
5. Open the terminal
6. Navigate until your current working directory is 'RoastMeMeBot-master'
7. Run `pip3 install -r requirements.txt` in order to install all dependencies
8. Run `python3 data/db.py` (or `python3 data\db.py` if you're using Windows) in order to setup the database
9. Run `python3 bot/bot.py` (or `python3 bot\bot.py` if you're using Windows) in order to get the Discord bot to start up
10. Everything should now work and your bot should operate as RoastMeMeBot

The minimal needed premissions code for the bot: 67584.

### CFG File Syntax
CFG files have a unique syntax (which is white-space sensitive). The only data-type that exists is a string. There are certain variables you can change which have to contain the exact string format that was made for them.
The CFG files syntax goes as follows:
`[variable]="[value]"`
Firstly, variables, there's 2 that exists for 'bot.cfg' and 3 that exist for 'meme_[id].cfg' files.
'bot.cfg' files contain the variables 'prefix' and 'token':
1. 'prefix' changes the prefix to be exactly the same as the value (e.g. if the command `prefix="!!"` is written the prefix would be '!!', so you would run `!!help` instead of the default `rt#help`)
2. 'token' changes the token of the bot

'meme_[id].cfg' files contain the variables 'font', 'textpos' and 'avatarpos' which directly influence the 'meme_[id].png' files (referred to as 'memes' in the text below):
1. 'font' variable sets the font to have a specific font-family (hast to be truetype), size and color. The string's format goes as follows: `font="[font_name] [size] [R] [G] [B]"` where: - '[font_name]' is the name of a font for future text - the font has to be inside of 'resources/fonts/' (or 'resources\\fonts\\' if you're using Windows) not including the file extension (so 'arial.ttf' would be written as 'arial') - '[size]' is the size of the future text - '[R]' is the amount of color red in future text - '[G]' is the amount of color green in future text - '[B]' is the amount of color blue in future text - By 'future text' im referring to any text placed using 'textpos' until the next 'font' variable. For example:
```python3
// Below is the first 'font' variable which makes text white
font="arial 15 255 255 255"
// The 2 'textpos' commands place white text onto the meme
textpos="12 12"
textpos="4215 15"

// Below is the second 'font' variable which rewrites the original 'font' variable and makes text black now
font="arial 15 0 0 0"
// The 2 'textpos' commands place black text onto the meme
textpos="16 16"
textpos="16 16"
```

2. 'textpos' variable places the username of the user getting roasted onto the meme (referred to as just text earlier). The string's format goes as follows: `textpos="[x] [y]"` where: - '[x]' is the x-position of the starting point of the username (from top-right which is 0) - '[y]' is the y-position of the starting point of the username (from top-right which is 0).

3. 'avatarpos' variable places the avatar of the user getting roasted onto the meme. The string's format goes as follows: `avatarpos="[start_x] [start_y] [end_x] [end_y]"` where: - '[start_x]' is the x-position of the starting point of the avatar (from top-right which is 0) - '[start_y]' is the y-position of the starting point of the avatar (from top-right which is 0) - '[end_x]' is the x-position of the ending point of the avatar (from top-right) - '[end_y]' is the y-position of the ending point of the avatar (from top-right).

It's recommended that you look into already existing CFG files in order to have easier time grasping the syntax.

### Adding/Editing resources
Resources which can be Added:
1. Fonts - can be added by placing a TrueType font inside of the 'resources/fonts/' directory (or 'resources\\fonts\\' if you're using Windows)
2. Memes - can be added by placing a PNG image inside of the 'resources/memes/' directory (or 'resources\\memes\\' if you're using Windows) together with the CFG file with the same name (both of which need to be in the format of 'meme_[id]' where 'id' is 1 bigger than the previous largest value or in other words - the id's need to be in ascending order without skipping - e.g. you can't have 'meme_1.png' and then 'meme_3.png', but you have to have them in order so 'meme_1.png' and then 'meme_2.png' - together with CFG files of the same name of course - and so on).

Resources which can be Edited:
1. Fonts - by changing or replacing them
2. Memes - by changing or replacing their PNG or CFG file
