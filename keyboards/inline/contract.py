from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

ikb_contracts = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Переход на описание", web_app=WebAppInfo(url="https://t.me/TeamCapital_bot/oferta"))
        ],
    ]
)

