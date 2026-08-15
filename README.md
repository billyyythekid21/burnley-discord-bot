# burnley.

A fun and interactive Discord bot and associated website built with Python and discord.py.

## Features

- **Fun**: 8-ball, chat responses, memes, and more!
- **Games**: Built-in games including chess
- **Music**: Music playback in voice channels
- **Calculator**: In-chat calculator
- **Wikipedia**: Wikipedia searches within chats
- **Google AI**: AI-powered responses to any queries
- **Moderation**: Server moderation tools
- **Leveling**: XP and level tracking

## Project Structure

```
burnley/
├── burnley.py          # burnley entry point
├── cogs/               # Feature modules (loaded dynamically)
│   ├── calculator.py
│   ├── chess.py
│   ├── commoncog.py
│   ├── fun.py
│   ├── games.py
│   ├── googleai.py
│   ├── help.py
│   ├── moderation.py
│   ├── music.py
│   └── wikipedia.py
├── docs/               # Associated website
└── leveldata.json      # Persistent and basic leveling data
```

## Setup

1. Install dependencies:
   ```bash
   pip install discord.py
   ```

2. Place your Discord bot token in `../tokens/discordtoken.txt`.

3. Run the bot:
   ```bash
   python burnley.py
   ```

The default command prefix is `$`.
Slash commands can also be used using `/` in Discord.