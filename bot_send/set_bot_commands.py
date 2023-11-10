from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт'),
        types.BotCommand('menu', 'Меню'),
        types.BotCommand('balance', 'Баланс'),
        types.BotCommand('ref', 'Реферальная ссылка'),
        types.BotCommand('instruction', 'Инструкция'),
        types.BotCommand('help', 'Техподдержка'),
    ])
