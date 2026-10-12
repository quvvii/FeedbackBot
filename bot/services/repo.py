from dataclasses import dataclass
import aiosqlite

from bot.services.repositories.users import UsersRepository
from bot.services.repositories.message_relations import MessageRelationsRepository

@dataclass
class Repo:
    users: UsersRepository
    message_relations: MessageRelationsRepository

def build_repo(db: aiosqlite.Connection) -> Repo:
    return Repo(
        users=UsersRepository(db),
        message_relations=MessageRelationsRepository(db),
    )
