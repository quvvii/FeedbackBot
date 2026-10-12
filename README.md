# Telegram Feedback Bot

A clean, lightweight feedback bot built with **Aiogram 3** and **aiosqlite**.

Provides an easy bridge between your users and support admin with zero ORM bloat.

## Features
- **All media types supported:** Seamless copying of text, media, voice messages, video notes, and stickers.
- **Bi-directional reaction sync:** Syncs standard reactions between user and admin without self-reaction conflicts.
- **User management:** Simple `/ban` and `/unban` commands (via reply or user ID).
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

## Usage

### Admin
- `/start` - Health check: uptime, user stats, and network latency.
- **Reply to any message** - Sends the response directly to the user.
- **React to user messages** - Syncs reaction to the user chat.
- `/ban [reply/user_id]` - Ban user from submitting messages.
- `/unban [reply/user_id]` - Unban user.

### User
- Send `/start` and message the bot. All messages are forwarded directly to the owner.
- React to admin replies to leave instant feedback.

## Project Structure
```text
bot/
├── config.py           # Configuration & validation
├── logger.py           # Logging setup
├── main.py             # Dispatcher entrypoint
├── handlers/
│   ├── admin/          # Admin replies, bans, health check
│   └── user/           # Messages, start, reaction sync
├── middlewares/        # Throttling, logging, user management
└── services/
    ├── db.py           # SQLite connection & schema init
    ├── repo.py         # Repositories container
    ├── uptime.py       # Uptime calculation
    └── repositories/   # User and message relation queries
```

## Screenshots
![admin start](https://i.ibb.co/zVdzvzpZ/1.png)

![admin preview](https://i.ibb.co/g0LfNRB/2.png)

![user preview](https://i.ibb.co/YFJnKc9W/3.png)

## License
This project is licensed under the [MIT License](LICENSE).