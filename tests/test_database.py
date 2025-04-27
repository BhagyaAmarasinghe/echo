"""
Tests for Echo database module.
"""
import os
import tempfile
import pytest
from datetime import datetime
from src.echo.database import DatabaseManager, Package, UsagePattern, Recommendation, InstallationRecord

@pytest.fixture
def db_manager():
    """Create a temporary database for testing."""
    # Create a temporary file
    temp_db = tempfile.NamedTemporaryFile(delete=False).name
    
    # Initialize database manager
    manager = DatabaseManager(temp_db)
    manager.initialize()
    
    yield manager
    
    # Clean up
    manager.close()
    if os.path.exists(temp_db):
        os.unlink(temp_db)


def test_database_initialization(db_manager):
    """Test database initialization."""
    # Get version - should be 1 (or higher if manual init)
    version = db_manager.get_database_version()
    assert version >= 1, "Database should be initialized with version 1 or higher"


def test_package_operations(db_manager):
    """Test package CRUD operations."""
    # Create a test package
    test_package = Package(
        name="test-package",
        version="1.0.0",
        description="Test package for unit tests",
        installed_date=datetime.now(),
        dependencies=["dep1", "dep2"],
        tags=["test", "unit-test"]
    )
    
    # Insert package
    db_manager.insert_package(test_package)
    
    # Get package
    retrieved = db_manager.get_package_by_name("test-package")
    assert retrieved is not None, "Package should be retrieved"
    assert retrieved.name == "test-package", "Package name should match"
    assert retrieved.version == "1.0.0", "Package version should match"
    assert len(retrieved.dependencies) == 2, "Package should have 2 dependencies"
    assert len(retrieved.tags) == 2, "Package should have 2 tags"
    
    # Update package
    test_package.version = "1.1.0"
    test_package.dependencies.append("dep3")
    db_manager.insert_package(test_package)
    
    # Get updated package
    updated = db_manager.get_package_by_name("test-package")
    assert updated.version == "1.1.0", "Package version should be updated"
    assert len(updated.dependencies) == 3, "Package should have 3 dependencies"
    
    # Get all packages
    packages = db_manager.get_installed_packages()
    assert len(packages) == 1, "Database should have 1 package"


def test_usage_pattern_operations(db_manager):
    """Test usage pattern operations."""
    # First insert a package (required due to foreign key constraint)
    package = Package(
        name="test-package",
        version="1.0.0"
    )
    db_manager.insert_package(package)
    
    # Create a test usage pattern
    test_pattern = UsagePattern(
        package_name="test-package",
        frequency=10,
        last_used=datetime.now(),
        usage_contexts=["test", "development"],
        importance_score=0.75
    )
    
    # Insert usage pattern
    db_manager.update_usage_pattern(test_pattern)
    
    # Get all usage patterns
    patterns = db_manager.get_usage_patterns()
    assert len(patterns) == 1, "Database should have 1 usage pattern"
    assert patterns[0].package_name == "test-package", "Pattern package name should match"
    assert patterns[0].frequency == 10, "Pattern frequency should match"
    assert len(patterns[0].usage_contexts) == 2, "Pattern should have 2 contexts"
    
    # Update usage pattern
    test_pattern.frequency = 20
    test_pattern.usage_contexts.append("production")
    db_manager.update_usage_pattern(test_pattern)
    
    # Get updated pattern
    updated_patterns = db_manager.get_usage_patterns()
    assert updated_patterns[0].frequency == 20, "Pattern frequency should be updated"
    assert len(updated_patterns[0].usage_contexts) == 3, "Pattern should have 3 contexts"


def test_recommendation_operations(db_manager):
    """Test recommendation operations."""
    # Create a test recommendation
    test_recommendation = Recommendation(
        package_name="recommended-package",
        score=0.95,
        reason="Test recommendation",
        category="development",
        timestamp=datetime.now(),
        source="test"
    )
    
    # Insert recommendation
    db_manager.add_recommendation(test_recommendation)
    
    # Get recommendations
    recommendations = db_manager.get_recommendations()
    assert len(recommendations) == 1, "Database should have 1 recommendation"
    assert recommendations[0].package_name == "recommended-package", "Recommendation package name should match"
    assert recommendations[0].score == 0.95, "Recommendation score should match"
    assert recommendations[0].source == "test", "Recommendation source should match"
    
    # Add another recommendation
    another_recommendation = Recommendation(
        package_name="another-package",
        score=0.85,
        reason="Another test recommendation",
        category="system",
        timestamp=datetime.now(),
        source="ai"
    )
    db_manager.add_recommendation(another_recommendation)
    
    # Get all recommendations
    all_recommendations = db_manager.get_recommendations()
    assert len(all_recommendations) == 2, "Database should have 2 recommendations"
    
    # Get recommendations by source
    ai_recommendations = db_manager.get_recommendations(source="ai")
    assert len(ai_recommendations) == 1, "Should have 1 AI recommendation"
    assert ai_recommendations[0].package_name == "another-package", "AI recommendation should match"


def test_installation_history(db_manager):
    """Test installation history operations."""
    # Create a test installation record
    test_record = InstallationRecord(
        package_name="test-package",
        operation="install",
        timestamp=datetime.now(),
        success=True,
        details="Test installation"
    )
    
    # Record installation
    db_manager.record_installation(test_record)
    
    # Get installation history
    history = db_manager.get_installation_history()
    assert len(history) == 1, "Database should have 1 installation record"
    assert history[0].package_name == "test-package", "Record package name should match"
    assert history[0].operation == "install", "Record operation should match"
    assert history[0].success is True, "Record success should match"
    
    # Add another record
    another_record = InstallationRecord(
        package_name="test-package",
        operation="remove",
        timestamp=datetime.now(),
        success=False,
        details="Test removal"
    )
    db_manager.record_installation(another_record)
    
    # Get all history
    all_history = db_manager.get_installation_history()
    assert len(all_history) == 2, "Database should have 2 installation records"
    
    # Get history for specific package
    package_history = db_manager.get_installation_history(package_name="test-package")
    assert len(package_history) == 2, "Should have 2 records for test-package"