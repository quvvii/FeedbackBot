from pathlib import Path

import aiosqlite


SCHEMA = """
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER UNIQUE NOT NULL,
    full_name   TEXT NOT NULL,
    username    TEXT,
    topic_id    INTEGER UNIQUE,
    is_banned   INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS topic_message_relations (
    user_id          INTEGER NOT NULL,
    user_message_id  INTEGER NOT NULL,
    topic_message_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, user_message_id)
);

CREATE INDEX IF NOT EXISTS idx_topic_messages 
ON topic_message_relations(topic_message_id);
"""

async def init_db(db_path: str) -> aiosqlite.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = await aiosqlite.connect(db_path)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA foreign_keys = ON")
    await conn.execute("PRAGMA busy_timeout = 5000")
    await conn.executescript(SCHEMA)
    await conn.commit()
    return conn
