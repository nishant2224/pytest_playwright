"""Application facades for GuestApp and AdminApp."""

from quality_demo.apps.admin.facade import AdminApp
from quality_demo.apps.guest.facade import GuestApp

__all__ = ["AdminApp", "GuestApp"]
