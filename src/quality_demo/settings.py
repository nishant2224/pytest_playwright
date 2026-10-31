"""Target environment settings loaded from TOML configuration."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings for target platform and timeouts."""

    base_url: str
    navigation_timeout_ms: int
    browser_timeout_ms: int
    http_timeout_seconds: float
    artifact_dir: Path

    @classmethod
    def load(cls, target: str = "demo", root_dir: Path | None = None) -> "Settings":
        """Load and validate settings for the specified target environment.

        Reads config/<target>.toml relative to the repository root.
        """
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent.parent

        config_path = root_dir / "config" / f"{target}.toml"
        if not config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with config_path.open("rb") as f:
            data = tomllib.load(f)

        allowed_keys = {
            "base_url",
            "navigation_timeout_ms",
            "browser_timeout_ms",
            "http_timeout_seconds",
            "artifact_dir",
        }
        unknown_keys = set(data.keys()) - allowed_keys
        if unknown_keys:
            raise ValueError(f"Unknown configuration keys in {config_path}: {unknown_keys}")

        base_url = data.get("base_url")
        if not base_url or not isinstance(base_url, str):
            raise ValueError("Configuration 'base_url' must be a non-empty string.")

        parsed_url = urlparse(base_url)
        if not (parsed_url.scheme in ("http", "https") and parsed_url.netloc):
            raise ValueError(f"Configuration 'base_url' is invalid: {base_url}")

        nav_timeout = int(data.get("navigation_timeout_ms", 30000))
        browser_timeout = int(data.get("browser_timeout_ms", 10000))
        http_timeout = float(data.get("http_timeout_seconds", 15.0))

        if nav_timeout <= 0 or browser_timeout <= 0 or http_timeout <= 0:
            raise ValueError("All timeout values must be positive numbers.")

        artifact_dir_str = data.get("artifact_dir", "artifacts")
        artifact_path = Path(artifact_dir_str)
        if not artifact_path.is_absolute():
            artifact_path = root_dir / artifact_path

        return cls(
            base_url=base_url.rstrip("/"),
            navigation_timeout_ms=nav_timeout,
            browser_timeout_ms=browser_timeout,
            http_timeout_seconds=http_timeout,
            artifact_dir=artifact_path,
        )
