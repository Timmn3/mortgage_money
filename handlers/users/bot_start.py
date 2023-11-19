from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import get_start_link

from bot_send.notify_admins import new_user_registration
from filters import IsSubscriber
from handlers.users.greeting import greeting
from handlers.users.levels import set_levels
from keyboards.inline import ikb_rules_contracts
from keyboards.inline.ikb_subsriber import generate_subscription_keyboard
from loader import dp, bot
from utils.db_api import users_commands as commands
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.admin_commands import get_greeting_document_ids
from utils.db_api.users_commands import update_my_referrals
from loguru import logger


text_start = ('👍Вы регистрируетесь в проекте <b>Team Capital</b> - надежные и доходные инвестиции в загородную'
              'недвижимость.\n\n'
              '<b>СХЕМА НАДЕЖНАЯ и БЕЗ РИСКОВ </b>\n\n'
              '1️⃣ Помогаем с Ипотекой или Кредитом\n'
              '👉Платим за Вас 20% первоначальный взнос при необходимости.\n'
              '👉Оплачиваем услуги подбора вариантов Ипотеки.\n'
              '👉Справки, формы, письма.\n'
              '👉Все необходимые документы.\n'
              '\n2️⃣ Погашаем платежи за год.\n'
              '👉Платим по Ипотечным платежам за клиента.\n'
              '👉Через год получаете прибыль 10% от суммы Ипотеки\n'
              '\n<b>ЛЮБОЙ РЕГИОН</b>\n\n'
              '✅ С вас ЛЮБАЯ кредитная история, с нас высокий и надежный доход. \n'
              '\nЗаполни  <b>ЗАЯВКУ </b> в этом боте.'
              '\n<b>Партнерская программа</b> без вложений.\n'
              'Отправляй друзьям и знакомым свою <b>реферальную ссылку.</b>\n\n'
              'Для запуска бота подпишитесь на канал и подтвердите подписку.')


@dp.message_handler(CommandStart())  # создаем message, который ловит команду /start
async def command_start(message: types.Message):
    await message.answer(text_start)
    user_id = message.from_user.id
    args = message.get_args()  # например пользователь пишет /start 1233124 с айди которого пригласил
    new_args = await commands.check_args(args, user_id)
    user = await commands.select_user(user_id)
    ref_link = await get_start_link(payload=user_id)
    if user:
        if user.status == 'active':
            await message.answer('Бот работает!')
        elif user.status == 'buned':
            await message.answer('Ты забанен')
    else:
        await commands.add_user(user_id=user_id,
                                id_proposal='',
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
        await new_user_registration(dp=dp, user_id=user_id, first_name=message.from_user.first_name,
                                    username=message.from_user.username)

        if new_args != '0':

            await set_levels(int(new_args))

            # Обновление my_referrals при поступлении нового реферала
            await update_my_referrals(int(new_args), int(user_id))

            await dp.bot.send_message(chat_id=int(new_args),
                                      text=(
                                          f'По твоей ссылке зарегистрировался(-ась) '
                                          f'<b>{message.from_user.first_name}</b>, '
                                          f'🟢 У тебя новая регистрация в 1 линии Deloonline, твой "Ожидаемый бонус" 1000 ₽\n\n'
                                          f'При одобрении заявки пользователя, этот бонус превратится в реальный "БОНУС ЗА ЗАЯВКИ"\n\n'
                                          f'При совершении этим пользователем сделки, Бот начислит тебе реальный "БОНУС ЗА ИПОТЕКУ"'
                                      )
                                      )

        subscription_keyboard = await generate_subscription_keyboard()

        # Отправьте сообщение с инструкциями по подписке и клавиатурой.
        await message.answer(
            f'Подпишись на телеграм канал(ы), что бы работали все функции бота:',
            reply_markup=subscription_keyboard
        )

        await message.answer('Проверить подписку', reply_markup=ikb_subscribed)


out_text = ('Отлично! Теперь вы можете начать работу! Для создания заявки нажмите /menu\n'
            '\nПравила заполнения заявки:\n'
            'Для начала! \n'
            '1. Заполнить заявку и получить отчет на 2-х сайтах  по проверке кредитной истории: \n'
            'https://person.nbki.ru/login\nи\nhttps://credistory.ru\nНажимаете кнопку "проверить"\n'
            'Появляется два варианта авторизации: через Сбербанк Онлайн или Госуслуги, выбираете наиболее удобный для '
            'Вас вариант.\n'
            'Появляются на выбор платная и бесплатная (пролистайте ниже) проверка кредитной истории, выбираете '
            'бесплатный вариант. Если ранее уже исчерпали лимит бесплатных проверок кредитной истории, то '
            'выбираете платную услугу.\n'
            'Появляется окно поиска кредитной истории, когда кредитная история будет '
            'найдена, нажимаете на кнопку "На главную".\n'
            'Появляется кнопка "Скачать кредитную историю", нажимаете, скачиваете документ и отправляете при заполнении '
            'заявки в бота.\nФотографии можно сделать через этого бота.\n2. Приготовить ПАСПОРТ РФ '
            '(скан, фото 1 и 2 страницы)\n'
            '3. Приготовить СНИЛС или водительские права: (фото или скан)')

ikb_subscribed = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Подписался", callback_data='subscribed'),
    ],
])


@dp.callback_query_handler(text='subscribed')
async def accept_reg(call: types.CallbackQuery):
    # приветствие
    await greeting(call.message)

    documents_ids = await get_greeting_document_ids()

    if documents_ids:
        await call.message.answer('Внимательно ознакомьтесь с договорами, правилами и иными документами '
                                  'по проекту:', reply_markup=ikb_rules_contracts)

        # for document_id in documents_ids:
        #     if document_id:
                # await call.message.answer(document_id)

        keyboard = types.InlineKeyboardMarkup()
        button_text = "Ознакомлен"
        callback_data = "acknowledge"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

        await call.message.answer("Если вы ознакомились с документами, нажмите кнопку:", reply_markup=keyboard)

        @dp.callback_query_handler(lambda callback_query: callback_query.data == 'acknowledge')
        async def acknowledge_documents(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            await call.message.answer_photo(
                'AgACAgIAAxkBAAID2mVZLRuxG34vvUqPS8mu0zs4bQgdAAKU1TEbrV7JSqHRsFEEfgpiAQADAgADeQADMwQ'
                )
            await bot.send_message(user_id,
                                   out_text)
