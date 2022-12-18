from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, ScalarSelect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import User
from app.models import Donation
from app.models import CharityProject
from fastapi import HTTPException


async def invest(session: AsyncSession,):
    print('Инвестируем во всю!')

    project_obj = await session.execute(
        select(CharityProject.id).where(
            CharityProject.fully_invested == False
        ).order_by(CharityProject.create_date)
    )
    if project_obj is None:
        raise HTTPException(
            status_code=404,
            detail='Некуда инвестировать!'
        )
    donation_obj = await session.execute(
        select(Donation.id).where(
            Donation.fully_invested == False
        )
    )
    if donation_obj is None:
        raise HTTPException(
            status_code=404,
            detail='Нечего инвестировать!'
        )
    # db_obj.scalars().first()

    projects = project_obj.scalars().all()
    donations = donation_obj.scalars().all()
    if not projects:
        raise HTTPException(
            status_code=422,
            detail='Некуда инвестировать!'
        )
    if not donations:
        raise HTTPException(
            status_code=404,
            detail='Нечего инвестировать!'
        )
    # print(projects[1].name)

    # print(donations)
    return projects
