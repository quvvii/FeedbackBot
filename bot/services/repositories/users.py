import aiosqlite


class UsersRepository:
    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def get_or_create(
        self, user_id: int, full_name: str, username: str | None
    ) -> aiosqlite.Row:
        cursor = await self.db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row:
            return row

        await self.db.execute(
            """
            INSERT OR IGNORE INTO users (user_id, full_name, username)
            VALUES (?, ?, ?)
            """,
            (user_id, full_name, username),
        )
        await self.db.commit()

        cursor = await self.db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        )
        return await cursor.fetchone()

    async def set_topic_id(self, user_id: int, topic_id: int) -> None:
        await self.db.execute(
            "UPDATE users SET topic_id = ? WHERE user_id = ?",
            (topic_id, user_id),
        )
        await self.db.commit()

    async def get_by_topic_id(self, topic_id: int) -> aiosqlite.Row | None:
        cursor = await self.db.execute(
            "SELECT * FROM users WHERE topic_id = ?",
            (topic_id,),
        )
        return await cursor.fetchone()

    async def set_banned(self, user_id: int, is_banned: bool) -> None:
        await self.db.execute(
            "UPDATE users SET is_banned = ? WHERE user_id = ?",
            (1 if is_banned else 0, user_id),
        )
        await self.db.commit()

    async def get_by_user_id(self, user_id: int) -> aiosqlite.Row | None:
        cursor = await self.db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        )
        return await cursor.fetchone()

    async def clear_topic_id(self, topic_id: int) -> None:
        await self.db.execute(
            "UPDATE users SET topic_id = NULL WHERE topic_id = ?",
            (topic_id,),
        )
        await self.db.commit()

    async def total(self) -> int:
        cursor = await self.db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def total_banned(self) -> int:
        cursor = await self.db.execute(
            "SELECT COUNT(*) FROM users WHERE is_banned = 1"
        )
        row = await cursor.fetchone()
        return row[0] if row else 0
