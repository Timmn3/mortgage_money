from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Подать заявку", callback_data='Подать заявку'),
                                        InlineKeyboardButton(text="Редактировать заявку",
                                                             callback_data='Редактировать заявку'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Партнерская программа",
                                                             callback_data='Партнерская программа'),
                                        InlineKeyboardButton(text="Мои бонусы",
                                                             callback_data='Мои бонусы'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Договор",
                                                             callback_data='Договор'),
                                        InlineKeyboardButton(text="Вывод средств", callback_data='Вывод средств')
                                    ]
                                ])



