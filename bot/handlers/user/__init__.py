from aiogram import Router, F
from bot.handlers import collect_routers
from bot.config import settings

router = Router(name="user")
router.message.filter(F.from_user.id != settings.owner_id)

router.include_router(collect_routers(__name__, __path__))