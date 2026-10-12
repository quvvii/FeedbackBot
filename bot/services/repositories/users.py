import aiosqlite


class UsersRepository:
    def __init__(self, db: aiosqlite.Connection) -> None:
        self._db = db

    async def upsert_user(
        self,
        user_id: int,
        name: str,
        username: str | None = None,
    ) -> None:
        await self._db.execute(
            """
            INSERT INTO users (user_id, name, username)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                username = excluded.username,
                updated_at = datetime('now')
            """,
            (user_id, name, username),
        )
        await self._db.commit()

    async def get_user(self, user_id: int) -> aiosqlite.Row | None:
        cursor = await self._db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        )
        return await cursor.fetchone()

    async def set_ban_status(self, user_id: int, is_banned: bool) -> None:
        await self._db.execute(
            """
            UPDATE users
            SET is_banned = ?,
                updated_at = datetime('now')
            WHERE user_id = ?
            """,
            (int(is_banned), user_id),
        )
        await self._db.commit()

    async def total(self) -> int:
        cursor = await self._db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def total_banned(self) -> int:
        cursor = await self._db.execute(
            "SELECT COUNT(*) FROM users WHERE is_banned = 1"
        )
        row = await cursor.fetchone()
        return row[0] if row else 0
