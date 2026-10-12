import aiosqlite


class MessageRelationsRepository:
    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def add_user_message(
        self, admin_message_id: int, user_id: int, user_message_id: int
    ) -> None:
        await self.db.execute(
            """
            INSERT OR REPLACE INTO user_to_admin_messages 
            (admin_message_id, user_id, user_message_id)
            VALUES (?, ?, ?)
            """,
            (admin_message_id, user_id, user_message_id),
        )
        await self.db.commit()

    async def add_admin_reply(
        self, admin_message_id: int, user_id: int, user_message_id: int
    ) -> None:
        await self.db.execute(
            """
            INSERT OR REPLACE INTO admin_to_user_messages 
            (user_message_id, user_id, admin_message_id)
            VALUES (?, ?, ?)
            """,
            (user_message_id, user_id, admin_message_id),
        )
        await self.db.commit()

    async def get_user_target(self, admin_message_id: int) -> aiosqlite.Row | None:
        cursor = await self.db.execute(
            """
            SELECT user_id, user_message_id 
            FROM user_to_admin_messages 
            WHERE admin_message_id = ?
            """,
            (admin_message_id,),
        )
        return await cursor.fetchone()

    async def get_admin_target(self, user_id: int, user_message_id: int) -> int | None:
        cursor = await self.db.execute(
            """
            SELECT admin_message_id 
            FROM admin_to_user_messages 
            WHERE user_id = ? AND user_message_id = ?
            """,
            (user_id, user_message_id),
        )
        row = await cursor.fetchone()
        return row["admin_message_id"] if row else None

    async def get_user_id_by_message(self, message_id: int) -> int | None:
        row = await self.get_user_target(message_id)
        return row["user_id"] if row else None
