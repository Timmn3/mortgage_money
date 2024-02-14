from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт'),
        types.BotCommand('private_office', 'Личный кабинет'),
        types.BotCommand('rules_contracts', 'Правила и договоры'),
        types.BotCommand('ref', 'Реферальная ссылка'),
        types.BotCommand('expected_bonus', 'Описание бонусов'),
        types.BotCommand('instruction', 'Инструкция'),
        types.BotCommand('help', 'Техподдержка'),
    ])
