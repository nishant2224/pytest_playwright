"""Test data factories generating isolated fictional entities."""

import random
import uuid

from faker import Faker

from quality_demo.models import Enquiry

_fake = Faker()


def build_enquiry(
    scenario_id: str = "T04",
    run_id: str | None = None,
    worker_label: str = "main",
) -> Enquiry:
    """Create a unique, typed, immutable Enquiry instance.

    Incorporates run, worker, and scenario identifiers into the subject
    to guarantee isolation on shared environments.
    """
    if run_id is None:
        run_id = uuid.uuid4().hex[:6]
    else:
        run_id = run_id[:6]

    suffix = f"{random.randint(1000, 9999):04d}"
    subject_tag = f"qp-{run_id}-{worker_label}-{scenario_id}-{suffix}"
    subject = f"Enquiry {subject_tag}"

    name = _fake.name()
    email = f"guest.{suffix}@example.com"
    # Ensure phone is exactly 12 numeric digits (valid per 11-21 constraint)
    phone = f"07{random.randint(1000000000, 9999999999)}"
    description = (
        "Automated test inquiry regarding booking availability "
        f"and pricing details for {subject_tag}."
    )

    return Enquiry(
        name=name,
        email=email,
        phone=phone,
        subject=subject,
        description=description,
    )
