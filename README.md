# :robot: Discord queue bot

A Discord bot to handle 5-man queues at a specific time.


## :rocket: Quick Start
1. Clone this repository and enter it:
```bash
git clone https://github.com/franklin-yang/discord-q-bot.git
cd discord-q-bot
```

2. Follow the steps in the following links to acquire a bot token and add the bot to your Discord server:
- https://discordpy.readthedocs.io/en/latest/quickstart.html#a-minimal-bot
- https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro

3. Create a file called `myToken.py` and store your token from the previous step as a string in that file:
```python3
TOKEN = 'TOKEN_GOES_HERE'
```

3. Install the necessary Python dependencies:
```bash
pip3 install -r requirements.txt
```

4. Run the bot:
```bash
python3 MyClient.py
```


## :gift: Features:
- Create a new queue with $newq @ hh:mm
- Join the queue with $joinq or by reacting to bot messages
- Join the waitlist if the queue is full or if you don't need to play but are willing to
- Move the queue time with $moveq
- Call out Ekatana for hacking


## :file_folder: Project Structure
The project is broken up as follows:

- `.idea/`, `__pycache/`, `bot-env/`: Parts of the development environment. Unclear whether these should be on GitHub or ignored.
- `MyClient.py`: The juicy stuff. This is where our Discord bot is written. 
- `basic_bot.py`: An example bot to showcase the `discord.ext.commands` extension module.
