if __name__ == '__main__':
    from handlers import root_router
    from loader import bot, dp

    dp.include_router(router=root_router)
    dp.run_polling(bot)
