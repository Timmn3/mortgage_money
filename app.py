from loader import scheduler
from scheduler.by_time import schedule_jobs, schedule_balance
from utils.db_api.start_stop_commands import add_start_stop


async def on_startup(dpr):
    from loguru import logger
    logger.add("file.log", format="{time} {level} {message}", level="DEBUG", rotation="50 MB", compression="zip")

    from loader import db
    from utils.db_api.db_gino import on_startup
    # print('Подключение к PostgreSQL')
    await on_startup(db)

    # print('Удаление базы данных')
    # await db.gino.drop_all()

    # print('создание таблиц')
    await db.gino.create_all()
    logger.info('Бот запущен')

    # импортирует функцию, которая отправляет сообщение о запуске бота всем администраторам
    from bot_send.notify_admins import on_startup_notufy
    await on_startup_notufy(dpr)

    # импортирует функцию, которая устанавливает команды бота
    from bot_send.set_bot_commands import set_default_commands
    await set_default_commands(dpr)

    # парсим
    # from parser.parse_last import parse_last  # последнийй тираж
    # await parse_last()

    # from parser.parse_all import add_in_bd_all  # все тиражи
    # from parser.parse_all import parse_all
    # await add_in_bd_all(parse_all())

    # print('\n Парсим 50 последних тиражей...')
    # print('')
    # print('Закончили парсить: Ok - добавлено, N - не добавлено\n')

    # запускаем парсинг по времени
    await schedule_jobs()
    # отправка сообщения о балансе ниже 100 р
    schedule_balance()


if __name__ == '__main__':
    from aiogram import executor  # импортируем executor для запуска поллинга
    from handlers import dp  # из хендлеров импортируем dp

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)


