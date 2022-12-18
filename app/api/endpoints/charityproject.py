# charity_project_router
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.services import invest
from app.core.db import get_async_session
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
# from app.crud.meeting_room import meeting_room_crud
from app.crud.charityproject import charity_project_crud
# from app.models.meeting_room import MeetingRoom
from app.models import CharityProject
# from app.schemas.meeting_room import (
#     MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
# )
from app.schemas.charityproject import CharityProjectCreate, CharityProjectUpdate, CharityProjectDB
# from app.schemas.reservation import ReservationDB
# from ..validators import check_meeting_room_exists, check_name_duplicate
from ..validators import check_charity_project_exists, check_project_name_duplicate
# Добавьте импорт зависимости, определяющей,
# что текущий пользователь - суперюзер.
from app.core.user import current_superuser

router = APIRouter()


@router.get(
    '/test',
    # response_model=list[CharityProjectDB],
    # response_model_exclude_none=True,
)
async def get_test_invest(
        session: AsyncSession = Depends(get_async_session),
):
    """Тест инвестиций."""
    projects = await invest(session)
    return projects


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    # response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    # Замените вызов функции на вызов метода.
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
    # dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # Добавляем докстринг для большей информативности.
    """
    Только для суперюзеров.

    Создаёт благотворительный проект.
    """
    await check_project_name_duplicate(new_project.name, session)
    # Замените вызов функции на вызов метода.
    new_project = await charity_project_crud.create(new_project, session)
    await invest(session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # Добавляем докстринг для большей информативности.
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """
    project = await check_charity_project_exists(project_id, session)
    # Замените вызов функции на вызов метода.
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Добавляем докстринг для большей информативности.
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)

    # Замените вызов функции на вызов метода.
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project