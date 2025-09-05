from typing import Annotated, Any, cast

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ...core.utils.cache import cache
from ...crud.crud_timer import crud_timer
from ...crud.crud_users import crud_users
from ...schemas.timer import TimerCreate, TimerCreateInternal, TimerRead, TimerUpdate
from ...schemas.user import UserRead

router = APIRouter(tags=["timers"])


@router.post("/timer", response_model=TimerRead, status_code=201)
async def create_timer(
    request: Request,
    timer: TimerCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> TimerRead:
    timer_internal_dict = timer.model_dump()
    timer_internal_dict["created_by_user_id"] = current_user["id"]

    timer_internal = TimerCreateInternal(**timer_internal_dict)
    created_timer = await crud_timer.create(db=db, object=timer_internal)

    timer_read = await crud_timer.get(db=db, id=created_timer.id, schema_to_select=TimerRead)
    if timer_read is None:
        raise NotFoundException("Created timer not found")

    return cast(TimerRead, timer_read)


@router.get("/timers", response_model=PaginatedListResponse[TimerRead])
@cache(
    key_prefix="user_{current_user_id}_timers:page_{page}:items_per_page:{items_per_page}",
    resource_id_name="current_user_id",
    expiration=60,
)
async def read_timers(
    request: Request,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    timers_data = await crud_timer.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        created_by_user_id=current_user["id"],
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=timers_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/timer/{timer_id}", response_model=TimerRead)
@cache(key_prefix="user_{current_user_id}_timer_{timer_id}", resource_id_name="timer_id")
async def read_timer(
    request: Request, timer_id: int, current_user: Annotated[dict, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(async_get_db)]
) -> TimerRead:
    db_timer = await crud_timer.get(
        db=db, id=timer_id, created_by_user_id=current_user["id"], is_deleted=False, schema_to_select=TimerRead
    )
    if db_timer is None:
        raise NotFoundException("Timer not found")

    return cast(TimerRead, db_timer)


@router.patch("/timer/{timer_id}")
@cache("user_{current_user_id}_timer_{timer_id}", resource_id_name="timer_id", pattern_to_invalidate_extra=["user_{current_user_id}_timers:*"])
async def update_timer(
    request: Request,
    timer_id: int,
    values: TimerUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_timer = await crud_timer.get(db=db, id=timer_id, is_deleted=False, schema_to_select=TimerRead)
    if db_timer is None:
        raise NotFoundException("Timer not found")

    # Check if current user owns the timer
    if db_timer.created_by_user_id != current_user["id"]:
        raise ForbiddenException()

    await crud_timer.update(db=db, object=values, id=timer_id)
    return {"message": "Timer updated"}


@router.delete("/timer/{timer_id}")
@cache("user_{current_user_id}_timer_{timer_id}", resource_id_name="timer_id", to_invalidate_extra={"user_{current_user_id}_timers": "{current_user_id}"})
async def delete_timer(
    request: Request,
    timer_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_timer = await crud_timer.get(db=db, id=timer_id, is_deleted=False, schema_to_select=TimerRead)
    if db_timer is None:
        raise NotFoundException("Timer not found")

    # Check if current user owns the timer
    if db_timer.created_by_user_id != current_user["id"]:
        raise ForbiddenException()

    await crud_timer.delete(db=db, id=timer_id)

    return {"message": "Timer deleted"}


@router.delete("/timer/db/{timer_id}", dependencies=[Depends(get_current_superuser)])
@cache("user_{current_user_id}_timer_{timer_id}", resource_id_name="timer_id", to_invalidate_extra={"user_{current_user_id}_timers": "user_{current_user_id}"})
async def erase_timer_from_db(
    request: Request, timer_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_timer = await crud_timer.get(db=db, id=timer_id, is_deleted=False, schema_to_select=TimerRead)
    if db_timer is None:
        raise NotFoundException("Timer not found")

    await crud_timer.db_delete(db=db, id=timer_id)
    return {"message": "Timer deleted from the database"}
