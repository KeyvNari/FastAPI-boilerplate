from fastcrud import FastCRUD

from ..models.display import Display
from ..schemas.display import DisplayCreateInternal, DisplayDelete, DisplayRead, DisplayUpdate, DisplayUpdateInternal

CRUDDisplay = FastCRUD[Display, DisplayCreateInternal, DisplayUpdate, DisplayUpdateInternal, DisplayDelete, DisplayRead]
crud_display = CRUDDisplay(Display)
