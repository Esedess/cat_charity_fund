# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
# from app.crud.meeting_room import meeting_room_crud
# from app.crud.reservation import reservation_crud
# from app.models.meeting_room import MeetingRoom
# from app.models.reservation import Reservation
from app.models import CharityProject


async def check_project_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_project_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservations)
#         )


# async def check_reservation_before_edit(
#         reservation_id: int,
#         session: AsyncSession,
#         user: User,
# ) -> Reservation:
#     reservation = await reservation_crud.get(
#         obj_id=reservation_id, session=session
#     )
#     if not reservation:
#         raise HTTPException(status_code=404, detail='Бронь не найдена!')
#     if reservation.user_id != user.id and not user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     return reservation