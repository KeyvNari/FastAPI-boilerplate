from fastcrud import FastCRUD

from ..models.plan_feature import PlanFeature
from ..schemas.plan_feature import PlanFeatureCreateInternal, PlanFeatureDelete, PlanFeatureRead, PlanFeatureUpdate, PlanFeatureUpdateInternal

CRUDPlanFeature = FastCRUD[PlanFeature, PlanFeatureCreateInternal, PlanFeatureUpdate, PlanFeatureUpdateInternal, PlanFeatureDelete, PlanFeatureRead]
crud_plan_features = CRUDPlanFeature(PlanFeature)
