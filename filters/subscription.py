from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config
from keyboards.inline import ikb_subsriber
from loader import bot, dp


class IsSubsriber(BoundFilter):  # проверка подписки
    async def check(self, message: types.Message):
        for chat_id in config.chat_ids:
            sub = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            if sub.status != types.ChatMemberStatus.LEFT:  # если пользователь не вышел
                return True
        else:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f'Подпишись на телеграм канал, что бы работали все функции бота:',
                                      reply_markup=ikb_subsriber)
            return False
