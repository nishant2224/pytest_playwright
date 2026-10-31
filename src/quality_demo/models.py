"""Domain models representing data exchanged across platform interfaces."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Enquiry:
    """Immutable guest enquiry submitted to the platform.

    Valid constraints per Restful Booker Platform specification:
    - subject: 5-100 characters
    - phone: 11-21 characters
    - description: 20-2000 characters
    """

    name: str
    email: str
    phone: str
    subject: str
    description: str

    def __post_init__(self) -> None:
        """Validate enquiry field constraints against target contract."""
        if not (5 <= len(self.subject) <= 100):
            raise ValueError(f"Subject length must be 5-100 characters, got {len(self.subject)}")
        if not (11 <= len(self.phone) <= 21):
            raise ValueError(f"Phone length must be 11-21 characters, got {len(self.phone)}")
        if not (20 <= len(self.description) <= 2000):
            raise ValueError(
                f"Description length must be 20-2000 characters, got {len(self.description)}"
            )
