from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import get_start_link

from bot_send.notify_admins import new_user_registration
from handlers.users.greeting import greeting
from keyboards.inline.ikb_subsriber import generate_subscription_keyboard
from loader import dp, bot
from utils.db_api import users_commands as commands
from utils.db_api.admin_commands import get_greeting_document_ids, get_greeting_text
from utils.db_api.users_commands import update_my_referrals
from loguru import logger


@dp.message_handler(CommandStart())  # создаем message, который ловит команду /start
async def command_start(message: types.Message):
    args = message.get_args()  # например пользователь пишет /start 1233124 с айди которого пригласил
    new_args = await commands.check_args(args, message.from_user.id)
    user = await commands.select_user(message.from_user.id)
    ref_link = await get_start_link(payload=message.from_user.id)
    if user:
        if user.status == 'active':
            await message.answer('Бот работает!')
        elif user.status == 'buned':
            await message.answer('Ты забанен')
    else:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                fio='',
                                city='',
                                timezone=3,
                                telephone=0,
                                referral_id=ref_link,
                                my_referrals='',
                                bonus_1=0,
                                bonus_2=0,
                                money=0,
                                role='',
                                balance=0,
                                status='active'
                                )

        # отправляем админам нового пользователя
        await new_user_registration(dp=dp, user_id=message.from_user.id, first_name=message.from_user.first_name,
                                    username=message.from_user.username)

        if new_args != '0':
            # Обновление my_referrals при поступлении нового реферала
            await update_my_referrals(int(new_args), message.from_user.id)
            await dp.bot.send_message(chat_id=int(new_args),
                                      text=f'По твоей ссылке зарегистрировался(-ась) '
                                           f'<b>{message.from_user.first_name}</b>, при одобрении ему(ей) заявки, '
                                           f'Вам начислится бонус')

        subscription_keyboard = await generate_subscription_keyboard()

        # Отправьте сообщение с инструкциями по подписке и клавиатурой.
        await message.answer(
            f'Подпишись на телеграм канал(ы), что бы работали все функции бота:',
            reply_markup=subscription_keyboard
        )

        # приветствие
        await greeting(message)

        documents_ids = await get_greeting_document_ids()

        if documents_ids:
            await message.answer(f'Ознакомьтесь с документами:')

            for document_id in documents_ids:
                if document_id:
                    await message.answer(document_id)

            keyboard = types.InlineKeyboardMarkup()
            button_text = "Ознакомлен"
            callback_data = "acknowledge"
            keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

            await message.answer("Если вы ознакомились с документами, нажмите кнопку:", reply_markup=keyboard)

            @dp.callback_query_handler(lambda callback_query: callback_query.data == 'acknowledge')
            async def acknowledge_documents(callback_query: types.CallbackQuery):
                user_id = callback_query.from_user.id

                await bot.send_message(user_id,
                                       'Отлично! Теперь вы можете начать работу! Для создания заявки нажмите /menu')
