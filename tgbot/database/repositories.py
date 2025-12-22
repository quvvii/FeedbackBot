from tortoise.exceptions import DoesNotExist

from .models import User, MessageRelations
from .schemas import User as UserSchema, MessageRelations as MessageRelationsSchema


class UserRepository:
    async def get_user(self, user_id: int) -> User | None:
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None

    async def create_user(self, user_id: int, name: str) -> UserSchema:
        user = await self.get_user(user_id)

        if user is None:
            user = await User.create(id=user_id, name=name)

        return UserSchema.from_orm(user)

    async def update_user(self, user_id: int, is_banned: bool) -> None:
        await User.filter(id=user_id).update(is_banned=is_banned)

    async def total(self) -> int:
        return await User.all().count()

    async def total_banned(self) -> int:
        return await User.filter(is_banned=True).count()

class MessageRelationsRepository:
    async def get_relation(self, message_id: int) -> MessageRelationsSchema | None:
        try:
            msg = await MessageRelations.get(message_id=message_id)
            return MessageRelationsSchema.from_orm(msg)
        except DoesNotExist:
            return None

    async def create_relation(self, message_id: int, user_id: int) -> MessageRelationsSchema:
        msg = await MessageRelations.create(
            message_id=message_id,
            user_id=user_id
        )
        return MessageRelationsSchema.from_orm(msg)
