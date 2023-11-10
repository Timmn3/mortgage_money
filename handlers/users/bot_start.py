from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from bot_send.notify_admins import new_user_registration
from handlers.users.instruction import instruction
from handlers.users.menu import prognosis
from loader import dp
from utils.db_api import user_commands as commands
from utils.db_api.user_commands import change_balance, user_balance
from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(CommandStart())  # создаем message, который ловит команду /start
async def command_start(message: types.Message):
    args = message.get_args()  # например пользователь пишет /start 1233124 с айди которого пригласил
    new_args = await commands.check_args(args, message.from_user.id)

    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer('Бот работает!')
        elif user.status == 'buned':
            await message.answer('Ты забанен')
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                referral_id=int(new_args),
                                status='active',
                                balance=30,
                                bill_id='')

        # отправляем админам нового пользователя
        await new_user_registration(dp=dp, user_id=message.from_user.id, first_name=message.from_user.first_name,
                                    username=message.from_user.username)
        try:
            await change_balance(int(new_args), 10)  # добавляем 10 руб к балансу
            userbalance = await user_balance(int(new_args))
            await dp.bot.send_message(chat_id=int(new_args),
                                      text=f'По твоей ссылке зарегистрировался(-ась) <b>{message.from_user.first_name}</b>\n'
                                           f'Ваш баланс пополнился на 10 ₽ и составляет {userbalance}₽')
        except Exception:
            pass

        await message.answer(f'Добро пожаловать!')
        await message.answer(f'Ваш баланс: 30.0 ₽')
        # await message.answer(f'Подпишись на телеграм канал, что бы работали все функции бота:',
        #                      reply_markup=ikb_subsriber)
        await message.answer(instruction)
        await prognosis(message)


@rate_limit(limit=3)
@dp.message_handler(text="/profile")  # создаем message, который ловит команду /profile
async def get_unban(message: types.Message):  # создаем асинхронную функцию
    user = await commands.select_user(message.from_user.id)
    await message.answer(f'id - {user.user_id}\n'
                         f'first_name: {user.first_name}\n'
                         f'last_name: {user.last_name}\n'
                         f'username: {user.username}\n'
                         f'status: {user.status}')
