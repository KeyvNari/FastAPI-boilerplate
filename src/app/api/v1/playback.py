from fastapi import APIRouter, HTTPException

from app.core.utils.cache import redis_client

router = APIRouter(prefix="/playback", tags=["playback"])


@router.get("/status/{room_id}")
async def get_playback_status(room_id: str):
    """Get current playback status for a room"""
    status = await redis_client.get_playback_status(room_id)
    if status is None:
        raise HTTPException(status_code=404, detail="No playback status found")
    return {"room_id": room_id, "status": status}


@router.post("/status/{room_id}")
async def set_playback_status(room_id: str, status: dict):
    """Set current playback status for a room"""
    await redis_client.set_playback_status(room_id, status)
    return {"message": "Playback status updated", "room_id": room_id}


@router.delete("/status/{room_id}")
async def delete_playback_status(room_id: str):
    """Delete playback status for a room"""
    await redis_client.delete_playback_status(room_id)
    return {"message": "Playback status deleted", "room_id": room_id}


@router.post("/event/{room_id}")
async def publish_room_event(room_id: str, event: dict):
    """Publish an event to a room channel"""
    await redis_client.publish_room_event(room_id, event)
    return {"message": "Event published", "room_id": room_id}


@router.post("/data/{room_id}/{key}")
async def set_room_data(room_id: str, key: str, data: dict):
    """Store arbitrary data for a room"""
    await redis_client.set_room_data(room_id, key, data)
    return {"message": "Room data stored", "room_id": room_id, "key": key}


@router.get("/data/{room_id}/{key}")
async def get_room_data(room_id: str, key: str):
    """Get arbitrary data for a room"""
    data = await redis_client.get_room_data(room_id, key)
    if data is None:
        raise HTTPException(status_code=404, detail="Room data not found")
    return {"room_id": room_id, "key": key, "data": data}


@router.get("/keys/{room_id}")
async def get_room_keys(room_id: str):
    """Get all keys for a room"""
    keys = await redis_client.get_room_keys(room_id)
    return {"room_id": room_id, "keys": keys}
