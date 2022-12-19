# charity_project_router
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services import invest

from ..validators import (check_charity_project_exists,
                          check_charity_project_full_amount_before_edit,
                          check_charity_project_invested_before_delete,
                          check_charity_project_not_closed,
                          check_project_name_duplicate)

router = APIRouter()


# @router.get(
#     '/test',
#     # response_model=list[CharityProjectDB],
#     # response_model_exclude_none=True,
# )
# async def get_test_invest(
#         session: AsyncSession = Depends(get_async_session),
# ):
#     """Тест инвестиций."""
#     # await invest(session)
#     projects = await invest(session)
#     return projects


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Создаёт благотворительный проект."""
    await check_project_name_duplicate(new_project.name, session)
    new_project = await charity_project_crud.create(new_project, session)
    await invest(session, new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть."""
    project = await check_charity_project_exists(project_id, session)
    check_charity_project_invested_before_delete(project)
    check_charity_project_not_closed(project)
    # check_charity_project_invested_before_delete(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной."""
    project = await check_charity_project_exists(
        project_id, session)

    check_charity_project_not_closed(project)

    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        check_charity_project_full_amount_before_edit(
            obj_in.full_amount, project)
        # project.invest()

    project = await charity_project_crud.update(
        project, obj_in, session)
    # project.invest()
    return project