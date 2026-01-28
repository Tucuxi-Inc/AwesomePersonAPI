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
    RoleProfile,
    RubricSource,
    Job,
    JobStatus,
    Candidate,
)
from app.data.traits import TRAITS
from app.data.default_rubrics import DEFAULT_RUBRICS
from app.data.role_templates import ROLE_TEMPLATES
from app.data.sample_jobs import SAMPLE_JOBS, SAMPLE_CANDIDATES


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
            rubric_source=RubricSource.RESEARCH_DEFAULT,
        )
        db.add(rubric)
        print(f"Created default rubric: {rubric.name}")

    db.commit()


def seed_role_templates(db: Session, trait_id_map: dict[str, uuid.UUID]) -> None:
    """Seed default role templates."""
    from sqlalchemy import select

    def convert_trait_name_to_id(trait_name: str) -> Optional[uuid.UUID]:
        """Convert trait name to ID, return None if not found."""
        # First try direct match
        if trait_name in trait_id_map:
            return trait_id_map[trait_name]
        # Try case-insensitive match
        for name, trait_id in trait_id_map.items():
            if name.lower() == trait_name.lower():
                return trait_id
        print(f"Warning: Trait not found: {trait_name}")
        return None

    for template_data in ROLE_TEMPLATES:
        # Check if role template already exists
        stmt = select(RoleProfile).where(
            RoleProfile.name == template_data["name"],
            RoleProfile.is_template == True,
        )
        existing = db.execute(stmt).scalar_one_or_none()

        if existing:
            print(f"Role template already exists: {template_data['name']}")
            continue

        # Convert trait names to IDs in critical_traits
        critical_traits = []
        for trait in template_data.get("critical_traits", []):
            trait_id = convert_trait_name_to_id(trait["trait_name"])
            if trait_id:
                critical_traits.append({
                    "trait_id": str(trait_id),
                    "level": trait["level"],
                    "weight": trait["weight"],
                    "rationale": trait.get("rationale", ""),
                })

        # Convert trait names to IDs in positive_traits
        positive_traits = []
        for trait in template_data.get("positive_traits", []):
            trait_id = convert_trait_name_to_id(trait["trait_name"])
            if trait_id:
                positive_traits.append({
                    "trait_id": str(trait_id),
                    "level": trait["level"],
                    "weight": trait["weight"],
                    "rationale": trait.get("rationale", ""),
                })

        # Convert trait names to IDs in counter_indicators
        counter_indicators = []
        for ci in template_data.get("counter_indicators", []):
            trait_id = convert_trait_name_to_id(ci["trait_name"])
            if trait_id:
                counter_indicators.append({
                    "trait_id": str(trait_id),
                    "threshold": ci["threshold"],
                    "reason": ci["reason"],
                })

        # Create role template
        role_template = RoleProfile(
            name=template_data["name"],
            description=template_data.get("description"),
            department=template_data.get("department"),
            level=template_data.get("level"),
            role_category=template_data["role_category"],
            critical_traits=critical_traits,
            positive_traits=positive_traits,
            counter_indicators=counter_indicators,
            valence_notes=template_data.get("valence_notes", {}),
            is_template=True,
            is_active=True,
        )
        db.add(role_template)
        print(f"Created role template: {role_template.name}")

    db.commit()


def seed_sample_jobs(db: Session, org_id: uuid.UUID) -> dict[str, uuid.UUID]:
    """Seed sample jobs for testing."""
    from sqlalchemy import select

    job_id_map = {}

    # Get role profiles to link jobs
    role_profile_map = {}
    stmt = select(RoleProfile).where(RoleProfile.is_template == True)
    profiles = db.execute(stmt).scalars().all()
    for profile in profiles:
        role_profile_map[profile.role_category] = profile.id

    for job_data in SAMPLE_JOBS:
        # Check if job already exists
        stmt = select(Job).where(
            Job.organization_id == org_id,
            Job.title == job_data["title"],
        )
        existing = db.execute(stmt).scalar_one_or_none()

        if existing:
            print(f"Job already exists: {job_data['title']}")
            job_id_map[job_data["title"]] = existing.id
            continue

        # Find matching role profile
        role_profile_id = role_profile_map.get(job_data["role_category"])

        job = Job(
            organization_id=org_id,
            title=job_data["title"],
            description=job_data["description"],
            department=job_data.get("department"),
            location=job_data.get("location"),
            employment_type=job_data.get("employment_type"),
            role_profile_id=role_profile_id,
            objective_requirements=job_data.get("objective_requirements", []),
            nice_to_haves=job_data.get("nice_to_haves", []),
            responsibilities=job_data.get("responsibilities", []),
            suggested_traits=job_data.get("suggested_traits", []),
            status=JobStatus.OPEN,
        )
        db.add(job)
        db.flush()
        job_id_map[job_data["title"]] = job.id
        print(f"Created job: {job.title}")

    db.commit()
    return job_id_map


def seed_sample_candidates(db: Session, org_id: uuid.UUID) -> dict[str, uuid.UUID]:
    """Seed sample candidates for testing."""
    from sqlalchemy import select

    candidate_id_map = {}

    for candidate_data in SAMPLE_CANDIDATES:
        # Check if candidate already exists
        stmt = select(Candidate).where(
            Candidate.organization_id == org_id,
            Candidate.email == candidate_data["email"],
        )
        existing = db.execute(stmt).scalar_one_or_none()

        if existing:
            print(f"Candidate already exists: {candidate_data['full_name']}")
            candidate_id_map[candidate_data["email"]] = existing.id
            continue

        candidate = Candidate(
            organization_id=org_id,
            email=candidate_data["email"],
            full_name=candidate_data["full_name"],
            phone=candidate_data.get("phone"),
            current_title=candidate_data.get("current_title"),
            current_company=candidate_data.get("current_company"),
            linkedin_url=candidate_data.get("linkedin_url"),
            years_experience=candidate_data.get("years_experience"),
            source=candidate_data.get("source"),
            referrer=candidate_data.get("referrer"),
            notes=candidate_data.get("notes"),
            tags=candidate_data.get("tags", []),
            status="NEW",
            is_active=True,
        )
        db.add(candidate)
        db.flush()
        candidate_id_map[candidate_data["email"]] = candidate.id
        print(f"Created candidate: {candidate.full_name}")

    db.commit()
    return candidate_id_map


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

        # Seed role templates
        print("\nSeeding role templates...")
        seed_role_templates(db, trait_id_map)

        # Seed sample jobs
        print("\nSeeding sample jobs...")
        job_id_map = seed_sample_jobs(db, org.id)
        print(f"Seeded {len(job_id_map)} jobs")

        # Seed sample candidates
        print("\nSeeding sample candidates...")
        candidate_id_map = seed_sample_candidates(db, org.id)
        print(f"Seeded {len(candidate_id_map)} candidates")

        print("\nDatabase initialization complete!")

    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
