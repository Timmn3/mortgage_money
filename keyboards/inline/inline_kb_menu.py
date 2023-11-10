from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Поиск комбинации", callback_data='Поиск комбинации'),
                                        InlineKeyboardButton(text="Количество тиражей в базе",
                                                             callback_data='Количество тиражей'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Просмотреть выпавшие комбинации в тираже №",
                                                             callback_data='Проверить тираж №')
                                    ],
                                    [
                                        InlineKeyboardButton(text="Посмотреть другой прогноз", callback_data='Прогноз')
                                    ]
                                ])


