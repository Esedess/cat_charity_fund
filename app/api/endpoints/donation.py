from typing import Dict, List, Set, Tuple


from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session

from app.crud.donation import donation_crud

from app.models import Donation
from app.services import invest
from app.schemas.donation import DonationCreate, DonationDB, DonationMiniDB

from app.core.user import current_superuser, current_user
from app.models import User

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_include={'user_id'},
    # response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    # Замените вызов функции на вызов метода.
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationMiniDB,
    # response_model_exclude={'user_id'},
    # response_model_include={'user_id'},
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        # Получаем текущего пользователя и сохраняем в переменную user.
        user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    # await check_meeting_room_exists(
    #     reservation.meetingroom_id, session
    # )
    # await check_reservation_intersections(
    #     # Так как валидатор принимает **kwargs, 
    #     # аргументы должны быть переданы с указанием ключей.
    #     **reservation.dict(), session=session
    # )
    new_donation = await donation_crud.create(
        # reservation, session
        # Передаём объект пользователя в метод создания объекта бронирования.
        donation, session, user
    )
    await invest(session, new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationMiniDB],
    # Добавляем множество с полями, которые надо исключить из ответа.
    response_model_exclude={'user_id'},
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    user_donations = await donation_crud.get_by_user(session, user)
    return user_donations