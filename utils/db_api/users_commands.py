from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.admin_commands import get_bonus_1
from utils.db_api.db_gino import db
from utils.db_api.shemas.users import Users


# добавление пользователя
async def add_user(user_id: int, first_name: str, last_name: str, username: str, fio: str, city: str,
                   timezone: int, telephone: int, referral_id: str, my_referrals: str, bonus_1: int,
                   bonus_2: int, money: int, role: str, balance: int, status: str):
    try:
        user_data = Users(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            fio=fio,
            city=city,
            timezone=timezone,
            telephone=telephone,
            referral_id=referral_id,
            my_referrals=my_referrals,
            bonus_1=bonus_1,
            bonus_2=bonus_2,
            money=money,
            role=role,
            balance=balance,
            status=status

        )
        await user_data.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')


async def check_user_status(user_id: int):
    """Проверьте статус пользователя по user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.status
        else:
            return False
    except ValueError:
        logger.error("Ошибка при проверке статуса пользователя")


async def count_users():
    """Подсчитайте количество пользователей"""
    user_count = await db.func.count(Users.user_id).gino.scalar()
    return user_count


async def select_user(user_id):
    """ Выбрать пользователя"""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        return user
    except ValueError:
        logger.error("Ошибка выбора пользователя")
        return False


async def bonus_for_referral(user_id):
    """ Добавляем бонус пользователю, при регистрации по его реферальной ссылке"""
    user = await select_user(user_id)
    percent = await get_bonus_1()
    new_bonus = user.bonus_1 + percent
    await user.update(bonus_1=new_bonus).apply()


async def update_my_referrals(user_id: int, new_referral_id: int):
    """ Обновление my_referrals при поступлении нового реферала"""
    user = await select_user(user_id)
    current_referrals = user.my_referrals or []  # Используйте пустой список, если my_referrals имеет значение None
    current_referrals.append(new_referral_id)
    await user.update(my_referrals=current_referrals).apply()


async def get_user_referrals(user_id: int):
    """Получить список рефералов пользователя по user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.my_referrals or []  # Return my_referrals if it exists, otherwise return an empty list
        else:
            return None  # User not found
    except Exception as e:
        logger.error(f"Ошибка при получении списка рефералов пользователя: {e}")
        return None


async def select_all_users():
    """Выбрать всех пользователей"""
    users = await Users.query.gino.all()
    return users


async def update_user_data(user_id, data):
    await Users.update.values(
        fio=data['fio'],
        city=data['city'],
        telephone=int(data['phone']),
    ).where(Users.user_id == user_id).gino.status()


async def update_user_fio(user_id: int, new_fio: str):
    """Обновление полного имени пользователя по user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            await user.update(fio=new_fio).apply()
            return True
        else:
            return False  # User not found
    except Exception as e:
        logger.error(f"Ошибка обновления полного имени пользователя.: {e}")
        return False


async def update_user_city(user_id: int, new_city: str):
    """Обновление города пользователя по user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            await user.update(city=new_city).apply()
            return True
        else:
            return False  # User not found
    except Exception as e:
        logger.error(f"Ошибка обновления города пользователя.: {e}")
        return False


async def update_user_telephone(user_id: int, new_telephone: int):
    """Обновление номера телефона пользователя по user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            await user.update(telephone=new_telephone).apply()
            return True
        else:
            return False  # User not found
    except Exception as e:
        logger.error(f"Error updating user's telephone: {e}")
        return False


async def get_user_city_and_telephone(user_id: int):
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            user_data = {
                'city': user.city,
                'telephone': user.telephone
            }
            return user_data
        else:
            return None  # User not found
    except Exception as e:
        logger.error(f"Ошибка при получении города и телефона пользователя.: {e}")
        return None


async def get_user_balance(user_id: int):
    """Получить баланс пользователя по user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.balance
        else:
            return None  # User not found
    except Exception as e:
        logger.error(f"Ошибка при получении баланса пользователя: {e}")
        return None


# функция для проверки аргументов переданных при регистрации
async def check_args(args, user_id: int):
    if args == '':  # если в аргумент передана пустая строка
        args = '0'
        return args

    elif not args.isnumeric():  # если не только цифры, а и буквы
        args = '0'
        return args

    elif args.isnumeric():  # если только цифры
        if int(args) == user_id:  # если аргумент является id пользователя
            args = '0'
            return args
        # получаем из БД пользователя у которого user_id такой же, как и переданный аргумент
        elif await select_user(user_id=int(args)) is None:  # если его нет
            args = '0'
            return args

        else:  # если аргумент прошел все проверки
            args = str(args)
            return args

    else:  # если что-то пошло не так
        args = '0'
        return args


async def get_all_user_ids():
    """Получите все идентификаторы пользователей."""
    try:
        user_ids = await db.select([Users.user_id]).gino.all()
        return [user_id[0] for user_id in user_ids]  # Extract user_id from the result list
    except Exception as e:
        logger.error(f"Ошибка получения всех идентификаторов пользователей.: {e}")
        return []


async def change_user_role(user_id: int, new_role: str):
    """Изменение роли пользователя."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            await user.update(role=new_role).apply()
            return True
        else:
            return False  # User not found
    except Exception as e:
        logger.error(f"Ошибка обновления роли пользователя.: {e}")


async def get_user_role(user_id: int):
    """Получить роль."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.role
        else:
            return None  # User not found
    except Exception as e:
        logger.error(f"Ошибка получения роли пользователя: {e}")
        return None
