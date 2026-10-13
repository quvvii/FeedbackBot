import aiosqlite


class MessageRelationsRepository:
    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def add_relation(
        self, user_id: int, user_message_id: int, topic_message_id: int
    ) -> None:
        await self.db.execute(
            """
            INSERT OR REPLACE INTO topic_message_relations 
            (user_id, user_message_id, topic_message_id)
            VALUES (?, ?, ?)
            """,
            (user_id, user_message_id, topic_message_id),
        )
        await self.db.commit()

    async def get_by_topic_message(
        self, topic_message_id: int
    ) -> aiosqlite.Row | None:
        cursor = await self.db.execute(
            """
            SELECT user_id, user_message_id 
            FROM topic_message_relations 
            WHERE topic_message_id = ?
            """,
            (topic_message_id,),
        )
        return await cursor.fetchone()

    async def get_by_user_message(
        self, user_id: int, user_message_id: int
    ) -> int | None:
        cursor = await self.db.execute(
            """
            SELECT topic_message_id 
            FROM topic_message_relations 
            WHERE user_id = ? AND user_message_id = ?
            """,
            (user_id, user_message_id),
        )
        row = await cursor.fetchone()
        return row["topic_message_id"] if row else None
