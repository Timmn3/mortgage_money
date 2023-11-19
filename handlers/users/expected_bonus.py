from aiogram import types
from loader import dp



@dp.message_handler(text="/expected_bonus")  # создаем хэндлер
async def command_ref(message: types.Message):  # создаем асинхронную функцию
    await message.answer(
        f'<b>ОЖИДАЕМЫЙ БОНУС</b> - это условное значение и показатель размера бонуса, при условии, что все 100% регистраций подадут заявку на Ипотеку и заявка перейдет в статус ПРИНЯТА.\n'
        f'Регистрация 1 уровень = 1000 ₽\n'
        f'Регистрация 2 уровень = 200 ₽\n'
        f'Регистрация 3 уровень = 200 ₽\n'
        f'Регистрация 4 уровень = 200 ₽\n'
        f'Регистрация 5 уровень = 200 ₽\n\n'
        f'Этот показатель и показатель реального бонуса позволит отслеживать реальную статистику эффективности твоей команды.\n\n'
        f'<b>БОНУС ЗА ЗАЯВКИ</b> - начисляется в момент верификации заявки и переходе в статус ПРИНЯТА\n'
        f'Принятая заявка 1 уровень = 1000 ₽\n'
        f'Принятая заявка 2 уровень = 200 ₽\n'
        f'Принятая заявка 3 уровень = 200 ₽\n'
        f'Принятая заявка 4 уровень = 200 ₽\n'
        f'Принятая заявка 5 уровень = 200 ₽\n\n'
        f'<b>БОНУС ЗА ИПОТЕКУ</b> - начисляется в момент одобрения ипотеки и получения денег клиентом/застройщиком.\n\n'
        f'1% от выданной суммы учитывается как 100% и рассчитывается бонус:\n'
        f'Принятая заявка 1 уровень = 50%\n'
        f'Принятая заявка 2 уровень = 10%\n'
        f'Принятая заявка 3 уровень = 10%\n'
        f'Принятая заявка 4 уровень = 10%\n'
        f'Принятая заявка 5 уровень = 10%'
    )
