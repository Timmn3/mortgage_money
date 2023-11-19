from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Подать заявку", callback_data='Подать заявку'),
                                        InlineKeyboardButton(text="Редактировать заявку",
                                                             callback_data='Редактировать заявку'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Личный кабинет",
                                                             callback_data='Личный кабинет'),
                                        InlineKeyboardButton(text="Мой договор",
                                                             callback_data='Мой договор'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Вывод средств", callback_data='Вывод средств')
                                    ]
                                ])



