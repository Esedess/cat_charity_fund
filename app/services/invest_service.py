from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_all_unfunded_projects_or_donations(
    session: AsyncSession,
    model: Union[CharityProject, Donation],
) -> Union[List[CharityProject], List[Donation]]:
    """
    Возвращает список не проинвестированных объектов.
    Сортируется по дате создания.
    """
    unfunded = await session.execute(
        select(model).where(
            model.fully_invested == 0
        ).order_by(model.create_date)
    )
    return unfunded.scalars().all()


def do_invest(proj: CharityProject, donat: Donation) -> None:
    """
    Расчитывает инвестиции и подготавливает объекты к записи в БД.
    """
    if proj.not_invested() >= donat.not_invested():
        investition = donat.not_invested()
        proj.invest(investition)
        donat.invest(investition)
    elif proj.not_invested() < donat.not_invested():
        investition = proj.not_invested()
        proj.invest(investition)
        donat.invest(investition)


def fully_invested_check(
    session: AsyncSession,
    obj: Union[CharityProject, Donation],
    objects_iter: iter
) -> Union[None, Union[CharityProject, Donation]]:
    """
    Проверяет полностью ли проинвестирован объект.
    Если да - добавляет измененный объект в сессию и возвращает следующий
    итератор или None.
    Если нет - возвращает объект обратно.
    """
    if obj.fully_invested:
        session.add(obj)
        try:
            return next(objects_iter)
        except StopIteration:
            return None
    return obj


async def invest(session: AsyncSession, new_obj: Union[CharityProject, Donation] = None) -> None:
    """
    Общая логика процесса инвестирования.
    Изменяет объекты в БД.
    """
    projects = await get_all_unfunded_projects_or_donations(session, CharityProject)
    donations = await get_all_unfunded_projects_or_donations(session, Donation)

    if not projects or not donations:
        return

    projects_iter = iter(projects)
    donations_iter = iter(donations)
    project = next(projects_iter)
    donation = next(donations_iter)
    while project and donation:

        do_invest(project, donation)

        project = fully_invested_check(session, project, projects_iter)
        donation = fully_invested_check(session, donation, donations_iter)

    await session.commit()
    if new_obj:
        await session.refresh(new_obj)
