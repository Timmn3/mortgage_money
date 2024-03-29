from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from keyboards.inline.ikb_subsriber import generate_subscription_keyboard
from utils.db_api.admin_commands import get_chat_ids_list

from loader import bot


class IsSubscriber(BoundFilter):  # проверка подписки
    async def check(self, message: types.Message):
        chat_ids = await get_chat_ids_list()
        chat_dict = chat_ids.split(",")
        for chat_id in chat_dict:
            sub = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            if sub.status != types.ChatMemberStatus.LEFT:  # если пользователь не вышел
                return True

            else:
                subscription_keyboard = await generate_subscription_keyboard()

                # Отправьте сообщение с инструкциями по подписке и клавиатурой.
                await message.answer(
                    f'Подпишись на телеграм канал(ы), что бы работали все функции бота:',
                    reply_markup=subscription_keyboard
                )
                return False


async def subscriber(user_id):  # проверка подписки
    chat_ids = await get_chat_ids_list()
    chat_dict = chat_ids.split(",")
    for chat_id in chat_dict:
        sub = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if sub.status != types.ChatMemberStatus.LEFT:  # если пользователь не вышел
            return True

        else:
            subscription_keyboard = await generate_subscription_keyboard()

            # Отправьте сообщение с инструкциями по подписке и клавиатурой.
            await bot.send_message(chat_id=user_id,
                                   text=f'Подпишись на телеграм канал(ы), что бы работали все функции бота:',
                                   reply_markup=subscription_keyboard
                                   )
            return False
