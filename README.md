# Telegram Feedback Bot

A clean, lightweight feedback bot built with **Aiogram 3** and **aiosqlite**.

Every user gets their own topic in your private chat with the bot, so conversations stay separated and nothing gets lost in a single chat.

## Features
- **Topic per user:** The first message creates a topic in your private chat with an info card and a Ban button.
- **All media types supported:** Messages are copied as-is: text, media, voice messages, video notes, stickers.
- **Bi-directional replies:** Each user message goes to their topic, and anything you write in that topic goes back to the user.
- **Bi-directional reaction sync:** Syncs standard reactions between user and admin without self-reaction conflicts.
- **User management:** A Ban button on the ticket card, `/ban` and `/unban` inside a topic, and `/close` for finished tickets.
- **Fast runtime:** Built with async SQLite and managed with `uv`.

## Quick Start

### 1. Clone & Configure
```bash
git clone https://github.com/quvvii/FeedbackBot.git
cd FeedbackBot
cp .env.example .env
```

Set up your `.env`:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
OWNER_ID=123456789
TZ_OFFSET=3
DB_PATH=data/bot.db
LOG_LEVEL=INFO
# PROXY_URL=http://user:pass@host:port
```

Topics are created in the private chat between you and the bot, so `OWNER_ID` is your user ID, not a group ID.

Topics must be enabled for the bot in BotFather first. Open the [@BotFather](https://t.me/BotFather) web app, pick your bot, go to **Bot Settings**, turn on **Threaded Mode** and choose **Disallow Users to Create New Threads**. Without this, `createForumTopic` returns an error and users only see "Couldn't deliver your message".

### 2. Run with Docker Compose
```bash
docker compose up -d --build
```
*Database and logs will be stored in `./data` and `./logs` directories.*

---

### Local Setup (without Docker)
Requires Python 3.12+ and uv:

```bash
uv sync
uv run python -m bot.main
```

If the `logs/` directory is missing, the bot logs to the console only. The database folder is created automatically.

## Usage

### Admin
- `/start` - Health check: uptime, user stats, and network latency.
- **Write in a ticket topic** - Anything except commands is sent to that user, and replies are linked both ways.
- **React in a ticket topic** - Syncs your reaction to the user's message; the user's reaction syncs back to the topic.
- **Ban button** - On the pinned ticket card, bans or unbans that user.
- `/ban` - Bans the user of the current topic.
- `/unban` - Unbans the user of the current topic.
- `/close` (also `/del`, `/delete`) - Deletes the current topic; the user's next message opens a new one.

Ban, unban and close only work inside a ticket topic. In the General topic (thread id `1`) they reply with an error instead.

### User
- Send `/start` and then any message. The first one opens your ticket, the rest are forwarded to it.
- Reply to an admin message to keep the thread; reactions are synced too.
- Banned users get no reply until unbanned.

## Project Structure
```text
bot/
├── config.py           # Configuration & validation
├── logger.py           # Logging setup
├── main.py             # Dispatcher entrypoint
├── keyboards/          # Inline keyboards
├── handlers/
│   ├── admin/          # Admin replies, bans, ticket closing, health check
│   └── user/           # Messages, start, reaction sync
├── middlewares/        # Logging, user management, repo injection
└── services/
    ├── db.py           # SQLite connection, schema, PRAGMAs
    ├── repo.py         # Repositories container
    ├── uptime.py       # Uptime calculation
    └── repositories/   # Users and message relation queries
```

## License
This project is licensed under the [MIT License](LICENSE).
