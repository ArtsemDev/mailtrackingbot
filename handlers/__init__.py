from aiogram import Router

from .users import users_router

root_router = Router(name='root')
root_router.include_router(router=users_router)

__all__ = ('root_router',)
