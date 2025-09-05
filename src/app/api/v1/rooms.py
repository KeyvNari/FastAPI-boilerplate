from typing import Annotated, Any, cast

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import NotFoundException
from ...core.utils.cache import cache
from ...crud.crud_rooms import crud_room
from ...schemas.room import RoomCreate, RoomCreateInternal, RoomRead, RoomUpdate

router = APIRouter(tags=["rooms"])


@router.post("/room", response_model=RoomRead, status_code=201)
async def write_room(
    request: Request,
    room: RoomCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> RoomRead:
    room_internal_dict = room.model_dump()
    room_internal_dict["created_by_user_id"] = current_user["id"]

    room_internal = RoomCreateInternal(**room_internal_dict)
    created_room = await crud_room.create(db=db, object=room_internal)

    room_read = await crud_room.get(db=db, id=created_room.id, schema_to_select=RoomRead)
    if room_read is None:
        raise NotFoundException("Created room not found")

    return cast(RoomRead, room_read)


@router.get("/rooms", response_model=PaginatedListResponse[RoomRead])
@cache(
    key_prefix="{current_user_id}_rooms:page_{page}:items_per_page:{items_per_page}",
    resource_id_name="current_user_id",
    expiration=60,
)
async def read_rooms(
    request: Request,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    rooms_data = await crud_room.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        created_by_user_id=current_user["id"],
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=rooms_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/room/{id}", response_model=RoomRead)
@cache(key_prefix="{current_user_id}_room_cache", resource_id_name="id")
async def read_room(
    request: Request, 
    id: int, 
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> RoomRead:
    db_room = await crud_room.get(
        db=db, id=id, created_by_user_id=current_user["id"], is_deleted=False, schema_to_select=RoomRead
    )
    if db_room is None:
        raise NotFoundException("Room not found")

    return cast(RoomRead, db_room)


@router.patch("/room/{id}")
@cache("{current_user_id}_room_cache", resource_id_name="id", pattern_to_invalidate_extra=["{current_user_id}_rooms:*"])
async def patch_room(
    request: Request,
    id: int,
    values: RoomUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_room = await crud_room.get(db=db, id=id, created_by_user_id=current_user["id"], is_deleted=False, schema_to_select=RoomRead)
    if db_room is None:
        raise NotFoundException("Room not found")

    await crud_room.update(db=db, object=values, id=id)
    return {"message": "Room updated"}


@router.delete("/room/{id}")
@cache("{current_user_id}_room_cache", resource_id_name="id", to_invalidate_extra={"{current_user_id}_rooms": "{current_user_id}"})
async def erase_room(
    request: Request,
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_room = await crud_room.get(db=db, id=id, created_by_user_id=current_user["id"], is_deleted=False, schema_to_select=RoomRead)
    if db_room is None:
        raise NotFoundException("Room not found")

    await crud_room.delete(db=db, id=id)

    return {"message": "Room deleted"}


@router.delete("/db_room/{id}", dependencies=[Depends(get_current_superuser)])
@cache("{current_user_id}_room_cache", resource_id_name="id", to_invalidate_extra={"{current_user_id}_rooms": "{current_user_id}"})
async def erase_db_room(
    request: Request, 
    id: int, 
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_room = await crud_room.get(db=db, id=id, is_deleted=False, schema_to_select=RoomRead)
    if db_room is None:
        raise NotFoundException("Room not found")

    await crud_room.db_delete(db=db, id=id)
    return {"message": "Room deleted from the database"}
