"""Failure evidence capture and reporting hooks."""

from pathlib import Path
from typing import Any


def capture_page_evidence(page: Any, label: str, artifact_root: Path, node_id: str) -> Path | None:
    """Capture failure screenshot for an open browser page and save to artifacts."""
    if not page or page.is_closed():
        return None

    safe_node = node_id.replace("::", "_").replace("/", "_").replace("\\", "_")
    output_dir = artifact_root / "evidence" / safe_node
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / f"{label}.png"

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
        # Try attaching to Allure if available
        try:
            import allure

            allure.attach.file(
                str(screenshot_path),
                name=f"Failure screenshot ({label})",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass
        return screenshot_path
    except Exception:
        return None
