import asyncio
import logging
from typing import List, Dict, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.db.database import local_session
from app.models.plan import Plan
from app.models.plan_feature import PlanFeature
from app.schemas.plan import PlanCreateInternal
from app.schemas.plan_feature import PlanFeatureCreateInternal
from app.crud.crud_plan import crud_plans
from app.crud.crud_plan_feature import crud_plan_features

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Default plan data - modify these as needed
DEFAULT_PLANS = [
    {
        "name": "Free",
        "price_cents": 0,
        "interval": "month",
        "description": "Basic features for getting started",
        "currency": "EUR",
    },
    {
        "name": "Pro",
        "price_cents": 2990,
        "interval": "month",
        "description": "Advanced features for professionals",
        "currency": "EUR",
    },
    {
        "name": "Enterprise",
        "price_cents": 9990,
        "interval": "month",
        "description": "Full suite with premium support",
        "currency": "EUR",
    },
]

# Default plan features - modify these as needed
DEFAULT_PLAN_FEATURES = {
    "Free": [
        {"feature_key": "max_rooms", "value": "1"},
        {"feature_key": "max_timers", "value": "4"},
        {"feature_key": "max_connected_devices", "value": "4"},
        {"feature_key": "can_customize_display", "value": "true"},
        {"feature_key": "can_save_display", "value": "false"},
    ],
    "Pro": [
        {"feature_key": "max_rooms", "value": "25"},
        {"feature_key": "max_participants", "value": "100"},
        {"feature_key": "storage_gb", "value": "100"},
        {"feature_key": "support", "value": "priority"},
        {"feature_key": "advanced_analytics", "value": "true"},
    ],
    "Enterprise": [
        {"feature_key": "max_rooms", "value": "unlimited"},
        {"feature_key": "max_participants", "value": "unlimited"},
        {"feature_key": "storage_gb", "value": "1000"},
        {"feature_key": "support", "value": "24_7_dedicated"},
        {"feature_key": "advanced_analytics", "value": "true"},
        {"feature_key": "custom_integrations", "value": "true"},
    ],
}


async def setup_plans_and_features(session: AsyncSession) -> None:
    """Setup plans and their features with upsert logic."""
    try:
        logger.info("Starting plans and features setup...")

        # Setup plans
        for plan_data in DEFAULT_PLANS:
            plan_name = plan_data["name"]
            logger.info(f"Processing plan: {plan_name}")

            try:
                # Check if plan exists
                query = select(Plan).where(Plan.name == plan_name)
                result = await session.execute(query)
                existing_plan = result.scalar_one_or_none()

                if existing_plan is None:
                    # Create new plan
                    try:
                        plan_create_data = PlanCreateInternal(**plan_data)
                        new_plan = await crud_plans.create(session, plan_create_data, commit=False)
                        # Flush to get the auto-generated ID
                        await session.flush()
                        logger.info(f"Created plan '{plan_name}'")
                        current_plan = new_plan
                    except IntegrityError as e:
                        # Handle race condition - plan might have been created by another process
                        await session.rollback()
                        logger.warning(f"Plan '{plan_name}' already exists (race condition): {e}")
                        # Re-fetch the existing plan
                        result = await session.execute(query)
                        current_plan = result.scalar_one()
                        logger.info(f"Using existing plan '{plan_name}'")
                else:
                    # Update existing plan (only update fields that can change)
                    plan_update_data = {k: v for k, v in plan_data.items() if k != "name"}
                    try:
                        await crud_plans.update(session, {"id": existing_plan.id}, plan_update_data, commit=False)
                        logger.info(f"Updated plan '{plan_name}'")
                        current_plan = existing_plan
                    except Exception as e:
                        logger.warning(f"Failed to update plan '{plan_name}': {e}")
                        current_plan = existing_plan

                # Setup features for this plan
                features_for_plan = DEFAULT_PLAN_FEATURES.get(plan_name, [])
                await setup_plan_features(session, current_plan.id, features_for_plan)

            except Exception as e:
                logger.error(f"Error processing plan '{plan_name}': {e}")
                # Continue with next plan instead of failing completely
                continue

        await session.commit()
        logger.info("Plans and features setup completed successfully")

    except Exception as e:
        await session.rollback()
        logger.error(f"Error setting up plans and features: {e}")
        raise


async def setup_plan_features(session: AsyncSession, plan_id: int, features: List[Dict[str, str]]) -> None:
    """Setup features for a specific plan with upsert logic."""
    for feature_data in features:
        feature_key = feature_data["feature_key"]
        logger.info(f"Processing feature '{feature_key}' for plan {plan_id}")

        try:
            # Check if feature exists for this plan
            query = select(PlanFeature).where(
                PlanFeature.plan_id == plan_id,
                PlanFeature.feature_key == feature_key
            )
            result = await session.execute(query)
            existing_feature = result.scalar_one_or_none()

            if existing_feature is None:
                # Create new feature
                try:
                    feature_create_data = PlanFeatureCreateInternal(
                        plan_id=plan_id,
                        feature_key=feature_key,
                        value=feature_data["value"]
                    )
                    await crud_plan_features.create(session, feature_create_data, commit=False)
                    logger.info(f"Created feature '{feature_key}' for plan {plan_id}")
                except IntegrityError as e:
                    # Handle race condition - feature might have been created by another process
                    logger.warning(f"Feature '{feature_key}' for plan {plan_id} already exists (race condition): {e}")
                    # Re-fetch the existing feature and update it
                    result = await session.execute(query)
                    existing_feature = result.scalar_one_or_none()
                    if existing_feature:
                        await crud_plan_features.update(
                            session,
                            {"id": existing_feature.id},
                            {"value": feature_data["value"]},
                            commit=False
                        )
                        logger.info(f"Updated feature '{feature_key}' for plan {plan_id} (after race condition)")
            else:
                # Update existing feature
                try:
                    await crud_plan_features.update(
                        session,
                        {"id": existing_feature.id},
                        {"value": feature_data["value"]},
                        commit=False
                    )
                    logger.info(f"Updated feature '{feature_key}' for plan {plan_id}")
                except Exception as e:
                    logger.warning(f"Failed to update feature '{feature_key}' for plan {plan_id}: {e}")

        except Exception as e:
            logger.error(f"Error processing feature '{feature_key}' for plan {plan_id}: {e}")
            # Continue with next feature instead of failing completely
            continue


async def main():
    """Main function to run the setup script."""
    try:
        async with local_session() as session:
            await setup_plans_and_features(session)
    except Exception as e:
        logger.error(f"Setup script failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())