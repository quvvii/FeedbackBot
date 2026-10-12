import importlib
import pkgutil
from aiogram import Router, F
from aiogram.enums import ChatType

def collect_routers(package_name: str, package_path) -> Router:
    router = Router(name=package_name)

    router.message.filter(F.chat.type == ChatType.PRIVATE)

    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(f"{package_name}.{module_name}")
        if hasattr(module, "router"):
            router.include_router(module.router)
    return router

def get_handlers_router() -> Router:
    return collect_routers(__name__, __path__)
