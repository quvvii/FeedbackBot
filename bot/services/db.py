import aiosqlite


SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    username    TEXT,
    is_banned   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS user_to_admin_messages (
    admin_message_id INTEGER PRIMARY KEY,
    user_id          INTEGER NOT NULL,
    user_message_id  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS admin_to_user_messages (
    user_message_id  INTEGER NOT NULL,
    user_id          INTEGER NOT NULL,
    admin_message_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, user_message_id)
);
"""

async def init_db(db_path: str) -> aiosqlite.Connection:
    conn = await aiosqlite.connect(db_path)
    conn.row_factory = aiosqlite.Row
    await conn.executescript(SCHEMA)
    await conn.commit()
    return conn
