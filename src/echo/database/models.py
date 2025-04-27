"""
Echo Database Models
-------------------
Data models for the Echo package recommendation system.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class Package:
    """Data model for a software package."""
    name: str
    version: str
    description: Optional[str] = None
    installed_date: Optional[datetime] = None
    source: Optional[str] = None
    size: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "installed_date": self.installed_date,
            "source": self.source,
            "size": self.size,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Package':
        """Create a Package instance from a dictionary."""
        return cls(
            name=data["name"],
            version=data["version"],
            description=data.get("description"),
            installed_date=data.get("installed_date"),
            source=data.get("source"),
            size=data.get("size"),
            dependencies=data.get("dependencies", []),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )


@dataclass
class UsagePattern:
    """Data model for package usage patterns."""
    package_name: str
    frequency: int
    last_used: datetime
    usage_contexts: List[str] = field(default_factory=list)
    importance_score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "package_name": self.package_name,
            "frequency": self.frequency,
            "last_used": self.last_used,
            "usage_contexts": self.usage_contexts,
            "importance_score": self.importance_score,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UsagePattern':
        """Create a UsagePattern instance from a dictionary."""
        return cls(
            package_name=data["package_name"],
            frequency=data["frequency"],
            last_used=data["last_used"],
            usage_contexts=data.get("usage_contexts", []),
            importance_score=data.get("importance_score"),
            metadata=data.get("metadata", {})
        )


@dataclass
class Recommendation:
    """Data model for package recommendations."""
    package_name: str
    score: float
    reason: str
    category: str
    timestamp: datetime
    source: str  # 'ai', 'similarity', etc.
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "package_name": self.package_name,
            "score": self.score,
            "reason": self.reason,
            "category": self.category,
            "timestamp": self.timestamp,
            "source": self.source,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recommendation':
        """Create a Recommendation instance from a dictionary."""
        return cls(
            package_name=data["package_name"],
            score=data["score"],
            reason=data["reason"],
            category=data["category"],
            timestamp=data["timestamp"],
            source=data["source"],
            metadata=data.get("metadata", {})
        )


@dataclass
class InstallationRecord:
    """Data model for package installation records."""
    package_name: str
    operation: str  # 'install', 'remove', etc.
    timestamp: datetime
    success: bool
    details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "package_name": self.package_name,
            "operation": self.operation,
            "timestamp": self.timestamp,
            "success": self.success,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InstallationRecord':
        """Create an InstallationRecord instance from a dictionary."""
        return cls(
            package_name=data["package_name"],
            operation=data["operation"],
            timestamp=data["timestamp"],
            success=data["success"],
            details=data.get("details")
        )
