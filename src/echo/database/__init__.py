"""
Echo Database Package
--------------------
Database management for the Echo package recommendation system.
"""

from .database import DatabaseManager
from .models import Package, UsagePattern, Recommendation, InstallationRecord

__all__ = [
    'DatabaseManager',
    'Package',
    'UsagePattern',
    'Recommendation',
    'InstallationRecord'
]
