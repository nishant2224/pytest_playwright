"""Ownership tracking and safe teardown management for created test records."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from quality_demo.models import Enquiry


@dataclass
class OwnershipRecord:
    """Tracks state and identity of an entity created during test execution."""

    enquiry: Enquiry
    node_id: str
    scenario_id: str
    discovered_id: int | None = None
    status: str = "pending"
    cleanup_status_code: int | None = None
    cleanup_error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class OwnershipRegistry:
    """Manages owned test records and ensures safe isolation and cleanup tracking."""

    def __init__(self, artifact_root: Path, run_id: str, worker_label: str) -> None:
        self.artifact_root = artifact_root
        self.run_id = run_id
        self.worker_label = worker_label
        self._records: list[OwnershipRecord] = []

    def register(self, enquiry: Enquiry, node_id: str, scenario_id: str = "T04") -> OwnershipRecord:
        """Register expected ownership before submission."""
        record = OwnershipRecord(
            enquiry=enquiry,
            node_id=node_id,
            scenario_id=scenario_id,
        )
        self._records.append(record)
        return record

    @property
    def records(self) -> list[OwnershipRecord]:
        return list(self._records)

    def write_manifest(self, record: OwnershipRecord) -> Path:
        """Write manifest recording ownership state and cleanup outcome."""
        target_dir = self.artifact_root / "owned-records" / self.run_id / self.worker_label
        target_dir.mkdir(parents=True, exist_ok=True)
        safe_name = record.node_id.replace("::", "_").replace("/", "_").replace("\\", "_")
        manifest_path = target_dir / f"{safe_name}.json"

        data = {
            "node_id": record.node_id,
            "scenario_id": record.scenario_id,
            "subject": record.enquiry.subject,
            "guest_name": record.enquiry.name,
            "discovered_id": record.discovered_id,
            "status": record.status,
            "cleanup_status_code": record.cleanup_status_code,
            "cleanup_error": record.cleanup_error,
            "metadata": record.metadata,
        }
        manifest_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return manifest_path
