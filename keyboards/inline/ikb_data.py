from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_personal_data = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Фамилия, Имя, Отчество", callback_data='personal_info'),
        InlineKeyboardButton(text="Город", callback_data='city'),
    ],
    [
        InlineKeyboardButton(text="Телефон", callback_data='phone'),
        InlineKeyboardButton(text="Фото 1 страницы паспорта", callback_data='passport_page1'),
    ],
    [
        InlineKeyboardButton(text="Фото 2 страницы паспорта", callback_data='passport_page2'),
        InlineKeyboardButton(text="Фото СНИЛС или фото водительских прав", callback_data='snils_or_license'),
    ],
    [
        InlineKeyboardButton(text="Фото с сайта кредитных историй", callback_data='credit_history_site1'),
        InlineKeyboardButton(text="Фото с другого сайта кредитных историй", callback_data='credit_history_site2'),
    ],
])