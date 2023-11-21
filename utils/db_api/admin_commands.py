from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.shemas.admin import AdminBD


# добавление
async def add_admin(greeting_text: str, greeting_video: str, greeting_photo: str,
                    channel_list: str, chat_ids_list: str, documents_id: str, technical_support: str, tariff: int,
                    set_bonus_1: int, set_bonus_2: int, variants_proposal: str,
                    newsletter_text: str,
                    newsletter_period: int, newsletter_whom: str):
    try:
        admin_data = AdminBD(
            greeting_text=greeting_text,
            greeting_video=greeting_video,
            greeting_photo=greeting_photo,
            channel_list=channel_list,
            chat_ids_list=chat_ids_list,
            documents_id=documents_id,
            technical_support=technical_support,
            tariff=tariff,
            set_bonus_1=set_bonus_1,
            set_bonus_2=set_bonus_2,
            variants_proposal=variants_proposal,
            newsletter_text=newsletter_text,
            newsletter_period=newsletter_period,
            newsletter_whom=newsletter_whom
        )
        await admin_data.create()
    except UniqueViolationError:
        logger.error(f'Запись в admin не удалась')


async def is_data():
    if await AdminBD.query.where(AdminBD.id == 1).gino.first():
        return True
    else:
        return False


# добавление функции сохранения greeting_video
async def save_greeting_video_id(greeting_video: str):
    """ Сохранение id видео"""
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    await admin.update(greeting_video=greeting_video).apply()


# добавление функции сохранения greeting_foto
async def save_greeting_photo_id(greeting_photo: str):
    """ Сохранение id фото"""
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    await admin.update(greeting_photo=greeting_photo).apply()


async def get_greeting_video_id():
    """ Получение id видео"""
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.greeting_video


async def get_greeting_foto_id():
    """ Получение id фото"""
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.greeting_photo


async def get_greeting_text():
    """ Получение текста приветствия """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.greeting_text


async def get_bonus_1():
    """ Получение значения set_bonus_1"""
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.set_bonus_1


async def get_channel_list():
    """ Получение списка каналов """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.channel_list.split(', ')


async def get_chat_ids_list():
    """ Получение списка chat_ids """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.chat_ids_list


async def add_channel_to_channel_list(channel: str):
    """ Добавление канала в список каналов """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    current_channel_list = admin.channel_list or []
    current_channel_list.append(channel)
    await admin.update(channel_list=current_channel_list).apply()


async def add_chat_id_to_chat_ids_list(chat_id: str):
    """ Добавление chat_id в список chat_ids """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    current_chat_ids_list = admin.chat_ids_list or []
    current_chat_ids_list.append(chat_id)
    await admin.update(chat_ids_list=current_chat_ids_list).apply()


async def save_greeting_document_id(document_id: str):
    """ Сохранение id документа """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    current_documents_id = admin.documents_id or ''  # Инициализировать как пустую строку, если это None
    current_documents_id += document_id + ','  # Добавить новый идентификатор и запятую (или другой разделитель)
    await admin.update(documents_id=current_documents_id).apply()


async def get_greeting_document_ids():
    """ Получение списка id документов """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    document_ids_str = admin.documents_id or ""
    return document_ids_str.split(',') if document_ids_str else []


async def get_newsletter_text():
    """ Получение текст рассылки"""
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.newsletter_text


async def replace_newsletter_period(new_period: int):
    """ Замена значения newsletter_period """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    await admin.update(newsletter_period=new_period).apply()


async def get_newsletter_period():
    """ Получение значения newsletter_period """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.newsletter_period


async def get_set_bonus_1():
    """ Получение значения set_bonus_1 """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.set_bonus_1


async def set_set_bonus_1(new_value: int):
    """ Установка значения set_bonus_1 """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    await admin.update(set_bonus_1=new_value).apply()


async def get_set_bonus_2():
    """ Получение значения set_bonus_1 """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.set_bonus_2


async def set_set_bonus_2(new_value: int):
    """ Установка значения set_bonus_2 """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    await admin.update(set_bonus_2=new_value).apply()


async def get_tariff():
    """ Получение значения tariff """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.tariff


async def set_tariff(new_value: int):
    """ Установка значения tariff """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    await admin.update(tariff=new_value).apply()


async def get_variants_proposal():
    """ Получение списка вариантов заявок """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    return admin.variants_proposal.split(', ')


async def set_variants_proposal(new_variants: list):
    """ Установка списка вариантов заявок """
    admin = await AdminBD.query.where(AdminBD.id == 1).gino.first()
    new_variants_str = ', '.join(new_variants)
    await admin.update(variants_proposal=new_variants_str).apply()


async def fill_the_table_admin():
    await add_admin(greeting_text='Добро пожаловать! Этот бот поможет Вам создать заявку по ипотеке',
                    greeting_video='',
                    greeting_photo='AgACAgIAAxkBAAID22VZLU14BKb9qHlmWyCAs7mwcoQyAAI40TEbbHbJSmDPI1c-d13DAQADAgADeQADMwQ',
                    channel_list='https://t.me/teamcapital_channel',
                    chat_ids_list='-1002111771031',
                    documents_id='https://t.me/TeamCapital_bot/oferta',
                    technical_support='WinnRusso',
                    tariff=0,
                    set_bonus_1=1000,
                    set_bonus_2=200,
                    variants_proposal='ипотека, автокредит',
                    newsletter_text='',
                    newsletter_period=0,
                    newsletter_whom='')
