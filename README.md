# :robot: Discord queue bot

A Discord bot to handle 5-man queues at a specific time.

Features:
- Join the queue with $joinq or by reacting to bot messages
- Join the waitlist if the queue is full or if you don't need to play but are willing to
- Move the queue time with $moveq
- Call out Ekatana for hacking

## :file_folder: Project Structure
The project is broken up as follows:

- `.idea/`, `__pycache/`, `bot-env/`: Parts of the development environment. Unclear whether these should be on GitHub or ignored.
- `MyClient.py`: The juicy stuff. This is where our Discord bot is written. 
- `basic_bot.py`: An example bot to showcase the `discord.ext.commands` extension module.
