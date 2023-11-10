from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import url_chat

ikb_subsriber = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Телеграм канал',
                                                                       url=url_chat)
                                              ]
                                          ])