"""Administrator credentials resolution with safe representation."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Credentials:
    """Immutable administrator credentials."""

    username: str
    password: str

    def __repr__(self) -> str:
        return f"Credentials(username={self.username!r}, password='***')"

    def __str__(self) -> str:
        return f"Credentials(username={self.username!r}, password='***')"

    @classmethod
    def resolve(cls, root_dir: Path | None = None) -> "Credentials":
        """Resolve administrator credentials from environment or public defaults.

        Loads .env if present without overwriting existing process variables.
        """
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent.parent

        env_file = root_dir / ".env"
        if env_file.is_file():
            load_dotenv(dotenv_path=env_file, override=False)

        username = os.getenv("RBP_ADMIN_USERNAME", "admin")
        password = os.getenv("RBP_ADMIN_PASSWORD", "password")
        return cls(username=username, password=password)
