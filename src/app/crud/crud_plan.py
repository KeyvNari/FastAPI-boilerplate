from fastcrud import FastCRUD

from ..models.plan import Plan
from ..schemas.plan import PlanCreateInternal, PlanDelete, PlanRead, PlanUpdate, PlanUpdateInternal

CRUDPlan = FastCRUD[Plan, PlanCreateInternal, PlanUpdate, PlanUpdateInternal, PlanDelete, PlanRead]
crud_plans = CRUDPlan(Plan)
