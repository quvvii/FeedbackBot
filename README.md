# Telegram Feedback Bot
Fast and powerful telegram bot based on Aiogram 3 framework. 

## Features
- Supports all types of Telegram messages (text, photo, audio, etc.).
- Annoying user? Just ban him using `/ban` command.
- Have you changed your mind? Use `/unban` then.
- Local SQLite database with Tortoise ORM for easy interaction.
- Do you want to add something of your own? No problem, It has simple structure.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/quvvii/FeedbackBot.git
cd FeedbackBot
```

2. Create `.env` file in the project root with the following content:
```env
TELEGRAM_BOT_TOKEN= # YOUR BOT TOKEN FROM @BotFather
TELEGRAM_ADMIN_ID= # YOUR TELEGRAM ID FROM @myidbot
```

3. Build and run the image: 
```bash
docker compose up -d --build
```
*Note: The database file will be automatically created in the data/ folder in the root directory.*

## Usage
**Admin:**
- `/start` - Ping bot
- `[Reply to message]` - Answer the user's question
- `/ban [user_id/reply]` - Ban a user from using the bot
- `/unban [user_id/reply]` - Unban user

**User:**
Click start, write your message and just wait.

### Screenshots
Admin's view:

![admin](https://i.ibb.co/TB55jmL0/image-3.png)

User's view:

![user](https://i.ibb.co/rGxKcVMk/2025-12-23-211540.png)

## License
This project is licensed under the [MIT License](LICENSE).
