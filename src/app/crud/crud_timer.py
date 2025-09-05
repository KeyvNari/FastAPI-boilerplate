from fastcrud import FastCRUD

from ..models.timer import Timer
from ..schemas.timer import TimerCreateInternal, TimerDelete, TimerRead, TimerUpdate, TimerUpdateInternal

CRUDTimer = FastCRUD[Timer, TimerCreateInternal, TimerUpdate, TimerUpdateInternal, TimerDelete, TimerRead]
crud_timer = CRUDTimer(Timer)
