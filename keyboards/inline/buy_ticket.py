from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

link = 'https://www.stoloto.ru/4x20/game?'

ikb_buy_ticket = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text=f"Купить билет «Столото 4 из 20»", url=link)
                                          ]
                                      ])
