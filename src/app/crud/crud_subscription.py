from fastcrud import FastCRUD

from ..models.subscription import Subscription
from ..schemas.subscription import (
    SubscriptionCreate,
    SubscriptionRead,
    SubscriptionUpdate,
    SubscriptionUpdateInternal,
)

CRUDSubscription = FastCRUD[
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionUpdateInternal,
    None,  # No delete schema for subscriptions
    SubscriptionRead,
]
crud_subscriptions = CRUDSubscription(Subscription)
