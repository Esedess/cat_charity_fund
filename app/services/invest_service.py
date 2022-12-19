from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import User
from app.models import Donation
from app.models import CharityProject
from fastapi import HTTPException
from typing import List, Union


async def get_all_unfunded_projects(session: AsyncSession) -> List[CharityProject]:
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False
        ).order_by(CharityProject.create_date.desc())
    )
    return projects.scalars().all()
    # return projects.scalars().first()


async def get_all_not_distributed_donations(session: AsyncSession) -> List[Donation]:
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False
        ).order_by(Donation.create_date)
    )
    return donations.scalars().all()
    # return donations.scalars().first()


def do_invest(proj: CharityProject, donat: Donation) -> None:
    if proj.not_invested() >= donat.not_invested():
        investition = donat.not_invested()
        proj.invest(investition)
        donat.invest(investition)
    elif proj.not_invested() < donat.not_invested():
        investition = proj.not_invested()
        proj.invest(investition)
        donat.invest(investition)


async def invest(session: AsyncSession, new_obj: Union[CharityProject, Donation]) -> None:
    print('Инвестируем во всю!')

    projects = await get_all_unfunded_projects(session)
    donations = await get_all_not_distributed_donations(session)
    # db_obj.scalars().first()

    if not projects:
        return
        # raise HTTPException(
        #     status_code=404,
        #     detail='Некуда инвестировать!'
        # )
    if not donations:
        return
        # raise HTTPException(
        #     status_code=404,
        #     detail='Нечего инвестировать!'
        # )

    projects_iter = iter(projects)
    donations_iter = iter(donations)
    project = next(projects_iter)
    donation = next(donations_iter)
    while project and donation:

        do_invest(project, donation)
        # if project.not_invested() >= donation.not_invested():
        #     investition = donation.not_invested()
        #     project.invest(investition)
        #     donation.invest(investition)
        # elif project.not_invested() < donation.not_invested():
        #     investition = project.not_invested()
        #     project.invest(investition)
        #     donation.invest(investition)

        if project.fully_invested:
            session.add(project)
            try:
                project = next(projects_iter)
            except StopIteration:
                project = None
        if donation.fully_invested:
            session.add(donation)
            try:
                donation = next(donations_iter)
            except StopIteration:
                donation = None
    # print(projects[1].name)
    # print(projects.not_invested())
    # projects.invest(500)
    # print(projects.not_invested())

    # session.add(projects)
    # session.add(donations)
    await session.commit()
    # await session.refresh(projects)
    await session.refresh(new_obj)
    # print(donations)
    return projects
