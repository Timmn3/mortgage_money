from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.admin_commands import get_bonus_1, get_set_bonus_1, get_set_bonus_2
from utils.db_api.db_gino import db
from utils.db_api.shemas.users import Users
import json
import pandas as pd
from loader import dp


# добавление пользователя
async def add_user(user_id: int, who_invited: str, first_name: str, last_name: str, username: str, fio: str, city: str,
                   bonus_3: int, telephone: int, referral_id: str, my_referrals: str, bonus_1: int,
                   bonus_2: int, money: int, role: str, balance: int, status: str, level: str):
    try:
        user_data = Users(
            user_id=user_id,
            who_invited=who_invited,
            first_name=first_name,
            last_name=last_name,
            username=username,
            fio=fio,
            city=city,
            bonus_3=bonus_3,
            telephone=telephone,
            referral_id=referral_id,
            my_referrals=my_referrals,
            bonus_1=bonus_1,
            bonus_2=bonus_2,
            money=money,
            role=role,
            balance=balance,
            status=status,
            level=level

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
    current_referrals_str = user.my_referrals or "[]"
    current_referrals = json.loads(current_referrals_str)
    current_referrals.append(new_referral_id)
    updated_referrals_str = json.dumps(current_referrals)
    await user.update(my_referrals=updated_referrals_str).apply()


async def get_referral_id(user_id: int):
    """Получить Referral_id для данного user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.referral_id
        else:
            return None  # User not found
    except Exception as e:
        logger.error(f"Ошибка получения Referral_id для пользователя.: {e}")
        return None


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
                'telephone': user.telephone,
                'username': user.username
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


async def select_all_users_with_data():
    """Выбрать всех пользователей с данными"""
    users = await Users.query.gino.all()

    user_list = []
    for user in users:
        user_data = {
            'user_id': user.user_id,
            'Кто пригласил': user.who_invited,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'Фамилия Имя Отчество': user.fio,
            'Город': user.city,
            'Номер телефона': user.telephone,
            'Реферальная ссылка': user.referral_id,
            'Список пользователей зарегистрированных по реферальной ссылке': user.my_referrals,
            'Бонус 1': user.bonus_1,
            'Бонус 2': user.bonus_2,
            'Сумма на счету для вывода': user.money,
            'Статус (роль)': user.role,
            'Баланс (подписка)': user.balance,
            'status': user.status,
            'Количество рефералов по уровням': user.level,
            'Дата регистрации': user.created_at.strftime('%Y.%m.%d')

        }

        user_list.append(user_data)

    return user_list


async def find_user_by_referral_value(target_value):
    """Найдите user_id, где target_value присутствует в my_referrals.."""
    try:
        # Используйте условие фильтра, чтобы найти пользователей с целевым значением в my_referrals.
        users_with_value = await Users.query.where(Users.my_referrals.contains(target_value)).gino.all()

        # Проверить, что есть хотя бы один пользователь с целевым значением
        if users_with_value:
            # Извлечь user_id из списка результатов
            user_ids_with_value = [user.user_id for user in users_with_value]

            return user_ids_with_value[0]
        else:
            return None

    except Exception as e:
        # Обработать другие исключения, если необходимо
        print(f"Произошла ошибка: {e}")
        return None


async def save_count_levels(user_id, level):
    bonus_1 = await get_set_bonus_1()
    bonus_2 = await get_set_bonus_2()

    user_id_int = int(user_id)

    user = await Users.query.where(Users.user_id == user_id_int).gino.first()

    if user:
        current_levels = json.loads(user.level)
        current_levels[str(level)] += 1
        updated_levels = json.dumps(current_levels)
        await user.update(level=updated_levels).apply()

        if level == 1:
            await add_bonus_1(user_id_int, bonus_1)
        if level in [2, 3, 4, 5]:
            await add_bonus_1(user_id_int, bonus_2)
    else:
        print('Пользователь не найден')


async def print_user_levels(user_id: int):
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()

        if user:
            current_levels = json.loads(user.level)

            # Calculate total count for each level
            level_counts = {int(level): count for level, count in current_levels.items()}

            total_sum = sum(level_counts.values())

            # Create a list of dictionaries with level and total count
            level_list = [{'level': level, 'count': level_counts.get(level, 0)} for level in range(1, 6)]

            # Format the output
            output = '\n'.join([f'{level["level"]} уровень = {level["count"]}' for level in level_list])

            return output, total_sum

        else:
            return {'error': 'Пользователь не найден'}

    except Exception as e:
        return {'error': f"Ошибка при получении уровней: {e}"}


async def update_database_from_excel(admin_id, file_path):
    try:
        # Load Excel data into a pandas DataFrame
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            user_id = int(row['user_id'])
            who_invited = str(row['Кто пригласил']) if pd.notna(row['Кто пригласил']) else ''
            first_name = str(row['first_name']) if pd.notna(row['first_name']) else ''
            last_name = str(row['last_name']) if pd.notna(row['last_name']) else ''
            username = str(row['username']) if pd.notna(row['username']) else ''
            fio = str(row['Фамилия Имя Отчество']) if pd.notna(row['Фамилия Имя Отчество']) else ''
            city = str(row['Город']) if pd.notna(row['Город']) else ''
            telephone = int(row['Номер телефона']) if pd.notna(row['Номер телефона']) else 0
            referral_id = str(row['Реферальная ссылка']) if pd.notna(row['Реферальная ссылка']) else ''
            my_referrals = str(row['Список пользователей зарегистрированных по реферальной ссылке']) if pd.notna(
                row['Список пользователей зарегистрированных по реферальной ссылке']) else ''
            bonus_1 = int(row['Бонус 1']) if pd.notna(row['Бонус 1']) else 0
            bonus_2 = int(row['Бонус 2']) if pd.notna(row['Бонус 2']) else 0
            money = int(row['Сумма на счету для вывода']) if pd.notna(row['Сумма на счету для вывода']) else 0
            role = str(row['Статус (роль)']) if pd.notna(row['Статус (роль)']) else ''
            balance = int(row['Баланс (подписка)']) if pd.notna(row['Баланс (подписка)']) else 0
            status = str(row['status']) if pd.notna(row['status']) else ''
            level = str(row['Количество рефералов по уровням']) if pd.notna(
                row['Количество рефералов по уровням']) else ''

            # Проверьте, существует ли пользователь уже в базе данных
            existing_user = await Users.query.where(Users.user_id == user_id).gino.first()

            if existing_user:
                # Update existing user data
                await existing_user.update(
                    who_invited=who_invited,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    fio=fio,
                    city=city,
                    telephone=telephone,
                    referral_id=referral_id,
                    my_referrals=my_referrals,
                    bonus_1=bonus_1,
                    bonus_2=bonus_2,
                    money=money,
                    role=role,
                    balance=balance,
                    status=status,
                    level=level
                ).apply()

        await dp.bot.send_message(admin_id, "Обновление базы данных из Excel завершено")

    except Exception as e:
        await dp.bot.send_message(admin_id, f"Ошибка обновления базы данных из Excel: {e}")
        logger.error(f"Ошибка обновления базы данных из Excel: {e}")


async def get_usernames(user_ids_str):
    try:
        # Convert the input string to a list of integers
        user_ids = [int(user_id) for user_id in user_ids_str.strip('[]').split(', ')]

        usernames = []
        for user_id in user_ids:
            user = await Users.query.where(Users.user_id == user_id).gino.first()
            if user:
                usernames.append(f'@{user.username}')

        return ', '.join(usernames)
    except Exception as e:
        logger.error(f"Error getting usernames: {e}")
        return None


async def update_who_invited(user_id: int, new_who_invited: str):
    """Обновить значение who_invited для данного пользователя."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            await user.update(who_invited=new_who_invited).apply()
            return True
        else:
            return False  # User not found
    except Exception as e:
        logger.error(f"Ошибка обновления who_invited для пользователя.: {e}")
        return False


async def find_user_by_who_invited(inviter_username: str):
    """Найдите user_id, выполнив поиск в столбце who_invited.."""
    try:
        user = await Users.query.where(Users.who_invited == inviter_username).gino.first()
        if user:
            return user.user_id
        else:
            return None  # User not found for the given inviter_username
    except Exception as e:
        logger.error(f"Ошибка поиска пользователя по who_invited.: {e}")
        return None


async def get_who_invited(user_id):
    """Получить значение who_invited для заданного user_id."""
    try:
        if user_id:
            user_id_int = int(user_id)
            user = await Users.query.where(Users.user_id == user_id_int).gino.first()
            if user:
                return user.who_invited
            else:
                return None  # Пользователь не найден
        else:
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении значения who_invited для пользователя: {e}")
        return None


async def add_bonus_1(user_id: int, amount: int):
    """Добавить значение к bonus_1 для заданного user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            current_bonus_1 = user.bonus_1
            new_bonus_1 = current_bonus_1 + amount
            await user.update(bonus_1=new_bonus_1).apply()
            return True
        else:
            return False  # Пользователь не найден
    except Exception as e:
        logger.error(f"Ошибка при добавлении значения к bonus_1 для пользователя: {e}")
        return False


async def get_bonus_1_value(user_id: int):
    """Получить значение bonus_1 для заданного user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.bonus_1
        else:
            return None  # Пользователь не найден
    except Exception as e:
        logger.error(f"Ошибка при получении значения bonus_1 для пользователя: {e}")
        return None


async def reset_all_user_data():
    try:
        # Fetch all users from the database
        users = await Users.query.gino.all()

        # Iterate through each user and update the specified fields
        for user in users:
            await user.update(
                level='{"1":0,"2":0, "3":0,"4":0,"5":0}',
                bonus_1=0
            ).apply()

    except Exception as e:
        logger.error(f"Error resetting user data: {e}")


async def count_users_by_who_invited(who_invited_value):
    try:
        # Use a database query to count occurrences of who_invited_value in the database
        user_count = await db.select([db.func.count()]). \
            where(Users.who_invited == who_invited_value).gino.scalar()

        return user_count if user_count else 0

    except Exception as e:
        print(f"Error counting users by who_invited: {e}")
        return 0


async def get_user_id_and_who_invited_dict():
    try:
        # Fetch all users from the database
        users = await Users.query.gino.all()

        # Create a dictionary to store user_id and who_invited values
        user_id_and_who_invited_dict = {user.user_id: user.who_invited for user in users}

        return user_id_and_who_invited_dict

    except Exception as e:
        print(f"Error getting user_id and who_invited data: {e}")
        return {}


async def find_user_ids_by_who_invited(inviter_username: str):
    try:
        # Используйте запрос, чтобы найти пользователей с указанным значением who_invited.
        users_with_value = await Users.query.where(Users.who_invited == inviter_username).gino.all()

        # Extract user_id values from the result list
        user_ids_with_value = [user.user_id for user in users_with_value]

        return user_ids_with_value

    except Exception as e:
        print(f"Error finding user_ids by who_invited: {e}")
        return []


async def find_user_ids_by_nik(inviter_username: str):
    try:
        # Используйте запрос, чтобы найти пользователей с указанным значением who_invited.
        users_with_value = await Users.query.where(Users.who_invited == inviter_username).gino.all()

        # Extract user_id values from the result list
        user_ids_with_value = [user.username for user in users_with_value]

        return user_ids_with_value

    except Exception as e:
        print(f"Error finding user_ids by who_invited: {e}")
        return []


async def get_user_id_who_invited_dict():
    try:
        # Fetch all users from the database
        users = await Users.query.gino.all()

        # Create a dictionary with user_id as the key and who_invited as the value
        user_id_who_invited_dict = {int(user.user_id): int(user.who_invited) if user.who_invited.isdigit() else None for user in users}

        return user_id_who_invited_dict

    except Exception as e:
        print(f"Error getting user_id who_invited dictionary: {e}")
        return {}


async def get_user_id_by_username(username):
    try:
        # Search for the user with the specified username
        user = await Users.query.where(Users.username == username).gino.first()

        if user:
            return user.user_id
        else:
            return None  # User not found for the given username

    except Exception as e:
        print(f"Error getting user_id by username: {e}")
        return None


async def get_user_created_at(user_id: int):
    """Получить значение created_at для данного user_id."""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        if user:
            return user.created_at.strftime('%Y-%m-%d %H:%M')
        else:
            return None  # Пользователь не найден
    except Exception as e:
        logger.error(f"Ошибка получения created_at для пользователя: {e}")
        return None
