from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.shemas.proposal import Proposal
from typing import List


async def add_proposal(user_id: int, fio: str, variant_proposal: str, status_proposal: str,
                       approved_amount: int, loan_amount: int, photo_passport_1: str, photo_passport_2: str,
                       photo_snils: str, photo_from_1_credit_history_site: str, photo_from_2_credit_history_site: str):
    try:
        proposal_data = Proposal(
            user_id=user_id,
            fio=fio,
            variant_proposal=variant_proposal,
            status_proposal=status_proposal,
            approved_amount=approved_amount,
            loan_amount=loan_amount,
            photo_passport_1=photo_passport_1,
            photo_passport_2=photo_passport_2,
            photo_snils=photo_snils,
            photo_from_1_credit_history_site=photo_from_1_credit_history_site,
            photo_from_2_credit_history_site=photo_from_2_credit_history_site

        )
        await proposal_data.create()
    except UniqueViolationError:
        logger.error('Не удалось записать поле заявки')

    # выбрать все данные


async def select_by_user_id(user_id: int) -> List[Proposal]:
    """ Выбрать все предложения для определенного user_id"""
    proposals = await Proposal.query.where(Proposal.user_id == user_id).gino.all()
    return proposals


async def fill_the_table_proposal():
    await add_proposal(user_id=0, fio='', variant_proposal='', status_proposal='',
                       approved_amount=0, loan_amount=0, photo_passport_1='', photo_passport_2='', photo_snils='',
                       photo_from_1_credit_history_site='', photo_from_2_credit_history_site='')


async def update_fio_by_user_id(user_id: int, new_fio: str):
    """Изменить поле FIO для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()
    if proposal:
        await proposal.update(fio=new_fio).apply()
    else:
        logger.warning(f'Предложение с user_id {user_id} не найдено или не существует')


async def update_photo_passport_1_by_user_id(user_id: int, new_photo_passport_1: str):
    """Обновить поле photo_passport_1 для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()
    if proposal:
        await proposal.update(photo_passport_1=new_photo_passport_1).apply()
    else:
        logger.warning(f'Предложение с user_id {user_id} не найдено')


async def update_photo_passport_2_by_user_id(user_id: int, new_photo_passport_2: str):
    """Обновить поле photo_passport_2 для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()
    if proposal:
        await proposal.update(photo_passport_2=new_photo_passport_2).apply()
    else:
        logger.warning(f'Предложение с user_id {user_id} не найдено')


async def update_photo_snils_by_user_id(user_id: int, new_photo_snils: str):
    """Обновить поле photo_snils для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()
    if proposal:
        await proposal.update(photo_snils=new_photo_snils).apply()
    else:
        logger.warning(f'Предложение с user_id {user_id} не найдено')


async def update_photo_from_1_credit_history_site_by_user_id(user_id: int, new_photo_from_1_credit_history_site: str):
    """Обновить поле photo_from_1_credit_history_site для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()
    if proposal:
        await proposal.update(photo_from_1_credit_history_site=new_photo_from_1_credit_history_site).apply()
    else:
        logger.warning(f'Предложение с user_id {user_id} не найдено')


async def update_photo_from_2_credit_history_site_by_user_id(user_id: int, new_photo_from_2_credit_history_site: str):
    """Обновить поле photo_from_2_credit_history_site для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()
    if proposal:
        await proposal.update(photo_from_2_credit_history_site=new_photo_from_2_credit_history_site).apply()
    else:
        logger.warning(f'Предложение с user_id {user_id} не найдено')


async def get_proposal_data(user_id: int) -> dict:
    """ Получить данные последнего предложения для определенного user_id"""
    proposal = await Proposal.query.where(Proposal.user_id == user_id).order_by(Proposal.id.desc()).gino.first()

    if proposal:
        # Extract specific fields from the proposal
        proposal_data = {
            'id': proposal.id,
            'variant_proposal': proposal.variant_proposal,
            'fio': proposal.fio,
            'photo_passport_1': proposal.photo_passport_1,
            'photo_passport_2': proposal.photo_passport_2,
            'photo_snils': proposal.photo_snils,
            'photo_from_1_credit_history_site': proposal.photo_from_1_credit_history_site,
            'photo_from_2_credit_history_site': proposal.photo_from_2_credit_history_site,
        }
        return proposal_data
    else:
        return None


async def update_status_by_id(proposal_id: int, new_status: str):
    """Обновите поле status_proposal для предложения с заданным идентификатором."""
    proposal = await Proposal.query.where(Proposal.id == proposal_id).gino.first()

    if proposal:
        await proposal.update(status_proposal=new_status).apply()
    else:
        logger.warning(f'Proposal with id {proposal_id} not found or does not exist')


async def get_proposals_by_status(target_status: str) -> List[Proposal]:
    """Получить все предложения с определенным статусом_предложение."""
    proposals = await Proposal.query.where(Proposal.status_proposal == target_status).gino.all()
    return proposals


async def get_all_proposals() -> List[Proposal]:
    """Получить все предложения."""
    proposals = await Proposal.query.gino.all()
    return proposals
