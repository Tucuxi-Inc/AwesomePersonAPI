"""Database initialization and seeding script."""

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SyncSessionLocal
from app.models import (
    Organization,
    User,
    Trait,
    TraitValenceMapping,
    ScoringRubric,
)
from app.data.traits import TRAITS
from app.data.default_rubrics import DEFAULT_RUBRICS


def create_superuser(db: Session) -> User:
    """Create default superuser if not exists."""
    from sqlalchemy import select

    stmt = select(User).where(User.email == "admin@apapi.dev")
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        print("Superuser already exists")
        return existing

    superuser = User(
        email="admin@apapi.dev",
        hashed_password=get_password_hash("changeme123"),
        full_name="System Administrator",
        role="ADMIN",
        is_superuser=True,
        is_active=True,
    )
    db.add(superuser)
    db.commit()
    db.refresh(superuser)
    print(f"Created superuser: {superuser.email}")
    return superuser


def create_demo_organization(db: Session) -> Organization:
    """Create demo organization if not exists."""
    from sqlalchemy import select

    stmt = select(Organization).where(Organization.slug == "demo")
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        print("Demo organization already exists")
        return existing

    org = Organization(
        name="Demo Organization",
        slug="demo",
        description="Demo organization for testing and development",
        industry="Technology",
        size="11-50",
        is_active=True,
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    print(f"Created organization: {org.name}")
    return org


def seed_traits(db: Session) -> dict[str, uuid.UUID]:
    """Seed all 24 traits from taxonomy."""
    from sqlalchemy import select

    trait_id_map = {}

    for trait_data in TRAITS:
        # Check if trait already exists
        stmt = select(Trait).where(Trait.name == trait_data["name"])
        existing = db.execute(stmt).scalar_one_or_none()

        if existing:
            print(f"Trait already exists: {trait_data['name']}")
            trait_id_map[trait_data["name"]] = existing.id
            continue

        # Create trait
        trait = Trait(
            name=trait_data["name"],
            category=trait_data["category"],
            definition=trait_data["definition"],
            spectrum_low_label=trait_data["spectrum_low_label"],
            spectrum_high_label=trait_data["spectrum_high_label"],
            behavioral_markers_low=trait_data["behavioral_markers_low"],
            behavioral_markers_high=trait_data["behavioral_markers_high"],
            counter_indicator_for=trait_data["counter_indicator_for"],
            display_order=trait_data["display_order"],
        )
        db.add(trait)
        db.flush()  # Get the ID

        # Create valence mappings
        for vm_data in trait_data.get("valence_mappings", []):
            valence_mapping = TraitValenceMapping(
                trait_id=trait.id,
                role_category=vm_data["role_category"],
                valence=vm_data["valence"],
                optimal_range_min=vm_data["optimal_range_min"],
                optimal_range_max=vm_data["optimal_range_max"],
                rationale=vm_data["rationale"],
            )
            db.add(valence_mapping)

        trait_id_map[trait_data["name"]] = trait.id
        print(f"Created trait: {trait.name}")

    db.commit()
    return trait_id_map


def seed_default_rubrics(db: Session, trait_id_map: dict[str, uuid.UUID]) -> None:
    """Seed default rubrics for core traits."""
    from sqlalchemy import select

    for rubric_data in DEFAULT_RUBRICS:
        trait_name = rubric_data["trait_name"]

        # Get trait ID
        trait_id = trait_id_map.get(trait_name)
        if not trait_id:
            # Try to find by name
            stmt = select(Trait).where(Trait.name == trait_name)
            trait = db.execute(stmt).scalar_one_or_none()
            if not trait:
                print(f"Trait not found for rubric: {trait_name}")
                continue
            trait_id = trait.id

        # Check if rubric already exists
        stmt = select(ScoringRubric).where(
            ScoringRubric.trait_id == trait_id,
            ScoringRubric.is_default == True,
        )
        existing = db.execute(stmt).scalar_one_or_none()

        if existing:
            print(f"Default rubric already exists for: {trait_name}")
            continue

        # Create rubric
        rubric = ScoringRubric(
            trait_id=trait_id,
            name=rubric_data["name"],
            description=rubric_data["description"],
            behavioral_anchors=rubric_data["behavioral_anchors"],
            primary_probes=rubric_data["primary_probes"],
            follow_up_probes=rubric_data["follow_up_probes"],
            star_indicators=rubric_data.get("star_indicators"),
            is_default=True,
            is_active=True,
        )
        db.add(rubric)
        print(f"Created default rubric: {rubric.name}")

    db.commit()


def init_db() -> None:
    """Initialize database with seed data."""
    print("Starting database initialization...")

    db = SyncSessionLocal()
    try:
        # Create superuser
        superuser = create_superuser(db)

        # Create demo organization
        org = create_demo_organization(db)

        # Update superuser with organization
        if superuser.organization_id is None:
            superuser.organization_id = org.id
            db.commit()

        # Seed traits
        print("\nSeeding traits...")
        trait_id_map = seed_traits(db)
        print(f"Seeded {len(trait_id_map)} traits")

        # Seed default rubrics
        print("\nSeeding default rubrics...")
        seed_default_rubrics(db, trait_id_map)

        print("\nDatabase initialization complete!")

    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
