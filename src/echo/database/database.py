"""
Echo Database Manager
-------------------
Database management for the Echo package recommendation system.
"""

import os
import json
import sqlite3
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union

# Import models
from .models import Package, UsagePattern, Recommendation, InstallationRecord

# Will be replaced with proper logger when utils module is implemented
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages database operations for the Echo package recommender.
    Handles database schema management using Liquibase.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = os.path.expanduser(db_path)
        self._ensure_directory()
        self.conn = None
    
    def _ensure_directory(self):
        """Ensure the directory for the database exists."""
        db_dir = os.path.dirname(self.db_path)
        Path(db_dir).mkdir(parents=True, exist_ok=True)
    
    def _get_connection(self):
        """Get a database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(
                self.db_path,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def initialize(self):
        """Initialize the database schema using Liquibase if available."""
        logger.info("Initializing database")
        
        # Try to run Liquibase update
        if self._run_liquibase_update():
            return
        
        # Fall back to manual schema creation if Liquibase fails or is unavailable
        logger.info("Falling back to manual schema creation")
        self._initialize_manual_schema()
    
    def _run_liquibase_update(self) -> bool:
        """
        Run Liquibase update to apply any pending changes.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if Liquibase is installed
            try:
                subprocess.run(['liquibase', '--version'], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                logger.warning("Liquibase not found, skipping Liquibase update")
                return False
            
            # Get path to migrations directory
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
            if not os.path.exists(migrations_dir):
                logger.warning(f"Migrations directory not found: {migrations_dir}")
                return False
                
            changelog_file = os.path.join(migrations_dir, 'changelog-master.xml')
            if not os.path.exists(changelog_file):
                logger.warning(f"Changelog file not found: {changelog_file}")
                return False
            
            # Build command
            cmd = [
                'liquibase',
                f'--changeLogFile={changelog_file}',
                f'--url=jdbc:sqlite:{self.db_path}',
                'update'
            ]
            
            # Execute Liquibase
            logger.info(f"Running Liquibase: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            logger.info("Liquibase update completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Liquibase update failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error running Liquibase: {e}")
            return False
    
    def _initialize_manual_schema(self):
        """Initialize the database schema manually."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create packages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS packages (
            name TEXT PRIMARY KEY,
            version TEXT NOT NULL,
            description TEXT,
            installed_date TIMESTAMP,
            source TEXT,
            size INTEGER,
            metadata TEXT
        )
        ''')
        
        # Create package_dependencies table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS package_dependencies (
            package_name TEXT,
            dependency_name TEXT,
            PRIMARY KEY (package_name, dependency_name),
            FOREIGN KEY (package_name) REFERENCES packages (name)
        )
        ''')
        
        # Create package_tags table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS package_tags (
            package_name TEXT,
            tag TEXT,
            PRIMARY KEY (package_name, tag),
            FOREIGN KEY (package_name) REFERENCES packages (name)
        )
        ''')
        
        # Create usage_patterns table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_patterns (
            package_name TEXT PRIMARY KEY,
            frequency INTEGER NOT NULL,
            last_used TIMESTAMP,
            importance_score REAL,
            metadata TEXT,
            FOREIGN KEY (package_name) REFERENCES packages (name)
        )
        ''')
        
        # Create usage_contexts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_contexts (
            package_name TEXT,
            context TEXT,
            PRIMARY KEY (package_name, context),
            FOREIGN KEY (package_name) REFERENCES packages (name)
        )
        ''')
        
        # Create recommendations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_name TEXT NOT NULL,
            score REAL NOT NULL,
            reason TEXT,
            category TEXT,
            timestamp TIMESTAMP,
            source TEXT,
            metadata TEXT
        )
        ''')
        
        # Create installation_history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS installation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_name TEXT NOT NULL,
            operation TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            success BOOLEAN NOT NULL,
            details TEXT
        )
        ''')
        
        # Create database_version table for manual version tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS database_version (
            version INTEGER PRIMARY KEY,
            applied_at TIMESTAMP NOT NULL,
            description TEXT
        )
        ''')
        
        # Insert initial version
        cursor.execute('''
        INSERT OR IGNORE INTO database_version (version, applied_at, description)
        VALUES (1, ?, 'Initial schema creation')
        ''', (datetime.now(),))
        
        conn.commit()
        logger.info("Database initialized successfully")
    
    def execute(self, query: str, params: Tuple = ()) -> None:
        """
        Execute a SQL query with no return value.
        
        Args:
            query (str): SQL query to execute
            params (Tuple): Parameters for the query
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    
    def query(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return the results.
        
        Args:
            query (str): SQL query to execute
            params (Tuple): Parameters for the query
            
        Returns:
            List[Dict[str, Any]]: Query results as a list of dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({key: row[key] for key in row.keys()})
        
        return results
    
    def insert_package(self, package: Union[Package, Dict[str, Any]]) -> None:
        """
        Insert or update a package in the database.
        
        Args:
            package (Union[Package, Dict[str, Any]]): Package information
        """
        # Convert to dict if Package object
        if isinstance(package, Package):
            package_dict = package.to_dict()
        else:
            package_dict = package
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Convert metadata to JSON string
        metadata = package_dict.get('metadata')
        metadata_str = json.dumps(metadata) if metadata else None
        
        # Insert or update package
        cursor.execute('''
        INSERT OR REPLACE INTO packages 
        (name, version, description, installed_date, source, size, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            package_dict['name'],
            package_dict['version'],
            package_dict.get('description'),
            package_dict.get('installed_date'),
            package_dict.get('source'),
            package_dict.get('size'),
            metadata_str
        ))
        
        # Handle dependencies
        if 'dependencies' in package_dict and package_dict['dependencies']:
            # Delete old dependencies
            cursor.execute('''
            DELETE FROM package_dependencies WHERE package_name = ?
            ''', (package_dict['name'],))
            
            # Insert new dependencies
            for dep in package_dict['dependencies']:
                cursor.execute('''
                INSERT INTO package_dependencies 
                (package_name, dependency_name)
                VALUES (?, ?)
                ''', (package_dict['name'], dep))
        
        # Handle tags
        if 'tags' in package_dict and package_dict['tags']:
            # Delete old tags
            cursor.execute('''
            DELETE FROM package_tags WHERE package_name = ?
            ''', (package_dict['name'],))
            
            # Insert new tags
            for tag in package_dict['tags']:
                cursor.execute('''
                INSERT INTO package_tags 
                (package_name, tag)
                VALUES (?, ?)
                ''', (package_dict['name'], tag))
        
        conn.commit()
    
    def update_usage_pattern(self, usage: Union[UsagePattern, Dict[str, Any]]) -> None:
        """
        Update usage pattern for a package.
        
        Args:
            usage (Union[UsagePattern, Dict[str, Any]]): Usage pattern information
        """
        # Convert to dict if UsagePattern object
        if isinstance(usage, UsagePattern):
            usage_dict = usage.to_dict()
        else:
            usage_dict = usage
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Convert metadata to JSON string
        metadata = usage_dict.get('metadata')
        metadata_str = json.dumps(metadata) if metadata else None
        
        # Insert or update usage pattern
        cursor.execute('''
        INSERT OR REPLACE INTO usage_patterns 
        (package_name, frequency, last_used, importance_score, metadata)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            usage_dict['package_name'],
            usage_dict['frequency'],
            usage_dict.get('last_used', datetime.now()),
            usage_dict.get('importance_score'),
            metadata_str
        ))
        
        # Handle usage contexts
        if 'usage_contexts' in usage_dict and usage_dict['usage_contexts']:
            # Delete old contexts
            cursor.execute('''
            DELETE FROM usage_contexts WHERE package_name = ?
            ''', (usage_dict['package_name'],))
            
            # Insert new contexts
            for context in usage_dict['usage_contexts']:
                cursor.execute('''
                INSERT INTO usage_contexts 
                (package_name, context)
                VALUES (?, ?)
                ''', (usage_dict['package_name'], context))
        
        conn.commit()
    
    def add_recommendation(self, recommendation: Union[Recommendation, Dict[str, Any]]) -> None:
        """
        Add a package recommendation to the database.
        
        Args:
            recommendation (Union[Recommendation, Dict[str, Any]]): Recommendation information
        """
        # Convert to dict if Recommendation object
        if isinstance(recommendation, Recommendation):
            rec_dict = recommendation.to_dict()
        else:
            rec_dict = recommendation
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Convert metadata to JSON string
        metadata = rec_dict.get('metadata')
        metadata_str = json.dumps(metadata) if metadata else None
        
        # Insert recommendation
        cursor.execute('''
        INSERT INTO recommendations 
        (package_name, score, reason, category, timestamp, source, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            rec_dict['package_name'],
            rec_dict['score'],
            rec_dict.get('reason'),
            rec_dict.get('category', 'general'),
            rec_dict.get('timestamp', datetime.now()),
            rec_dict.get('source', 'unknown'),
            metadata_str
        ))
        
        conn.commit()
    
    def record_installation(self, record: Union[InstallationRecord, Dict[str, Any]]) -> None:
        """
        Record a package installation or removal operation.
        
        Args:
            record (Union[InstallationRecord, Dict[str, Any]]): Installation record
        """
        # Convert to dict if InstallationRecord object
        if isinstance(record, InstallationRecord):
            record_dict = record.to_dict()
        else:
            record_dict = record
        
        self.execute(
            """
            INSERT INTO installation_history 
            (package_name, operation, timestamp, success, details)
            VALUES (?, ?, ?, ?, ?)
            """, 
            (
                record_dict['package_name'],
                record_dict['operation'],
                record_dict.get('timestamp', datetime.now()),
                record_dict['success'],
                record_dict.get('details')
            )
        )
    
    def get_installed_packages(self) -> List[Package]:
        """
        Get all installed packages from the database.
        
        Returns:
            List[Package]: List of installed packages
        """
        packages = []
        
        # Query basic package info
        package_rows = self.query("""
            SELECT * FROM packages
        """)
        
        for row in package_rows:
            # Convert metadata string to dict
            if row.get('metadata'):
                try:
                    row['metadata'] = json.loads(row['metadata'])
                except json.JSONDecodeError:
                    row['metadata'] = {}
            
            # Get package dependencies
            deps_rows = self.query("""
                SELECT dependency_name FROM package_dependencies
                WHERE package_name = ?
            """, (row['name'],))
            
            row['dependencies'] = [dep['dependency_name'] for dep in deps_rows]
            
            # Get package tags
            tags_rows = self.query("""
                SELECT tag FROM package_tags
                WHERE package_name = ?
            """, (row['name'],))
            
            row['tags'] = [tag['tag'] for tag in tags_rows]
            
            # Create Package object
            packages.append(Package.from_dict(row))
        
        return packages
    
    def get_package_by_name(self, name: str) -> Optional[Package]:
        """
        Get a package by name.
        
        Args:
            name (str): Package name
            
        Returns:
            Optional[Package]: Package or None if not found
        """
        rows = self.query("SELECT * FROM packages WHERE name = ?", (name,))
        if not rows:
            return None
        
        row = rows[0]
        
        # Convert metadata string to dict
        if row.get('metadata'):
            try:
                row['metadata'] = json.loads(row['metadata'])
            except json.JSONDecodeError:
                row['metadata'] = {}
        
        # Get package dependencies
        deps_rows = self.query("""
            SELECT dependency_name FROM package_dependencies
            WHERE package_name = ?
        """, (name,))
        
        row['dependencies'] = [dep['dependency_name'] for dep in deps_rows]
        
        # Get package tags
        tags_rows = self.query("""
            SELECT tag FROM package_tags
            WHERE package_name = ?
        """, (name,))
        
        row['tags'] = [tag['tag'] for tag in tags_rows]
        
        return Package.from_dict(row)
    
    def get_usage_patterns(self) -> List[UsagePattern]:
        """
        Get all usage patterns from the database.
        
        Returns:
            List[UsagePattern]: List of usage patterns
        """
        patterns = []
        
        # Query usage patterns
        pattern_rows = self.query("""
            SELECT * FROM usage_patterns 
            ORDER BY frequency DESC
        """)
        
        for row in pattern_rows:
            # Convert metadata string to dict
            if row.get('metadata'):
                try:
                    row['metadata'] = json.loads(row['metadata'])
                except json.JSONDecodeError:
                    row['metadata'] = {}
            
            # Get usage contexts
            contexts_rows = self.query("""
                SELECT context FROM usage_contexts
                WHERE package_name = ?
            """, (row['package_name'],))
            
            row['usage_contexts'] = [ctx['context'] for ctx in contexts_rows]
            
            # Create UsagePattern object
            patterns.append(UsagePattern.from_dict(row))
        
        return patterns
    
    def get_recommendations(self, limit: int = 10, source: Optional[str] = None) -> List[Recommendation]:
        """
        Get recent recommendations from the database.
        
        Args:
            limit (int): Maximum number of recommendations to return
            source (Optional[str]): Filter by source (ai, similarity, etc.)
            
        Returns:
            List[Recommendation]: List of recommendations
        """
        query = "SELECT * FROM recommendations"
        params = ()
        
        if source:
            query += " WHERE source = ?"
            params = (source,)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params = params + (limit,)
        
        recommendation_rows = self.query(query, params)
        recommendations = []
        
        for row in recommendation_rows:
            # Convert metadata string to dict
            if row.get('metadata'):
                try:
                    row['metadata'] = json.loads(row['metadata'])
                except json.JSONDecodeError:
                    row['metadata'] = {}
            
            # Create Recommendation object
            recommendations.append(Recommendation.from_dict(row))
        
        return recommendations
    
    def get_installation_history(self, limit: int = 10, package_name: Optional[str] = None) -> List[InstallationRecord]:
        """
        Get installation history from the database.
        
        Args:
            limit (int): Maximum number of records to return
            package_name (Optional[str]): Filter by package name
            
        Returns:
            List[InstallationRecord]: List of installation records
        """
        query = "SELECT * FROM installation_history"
        params = ()
        
        if package_name:
            query += " WHERE package_name = ?"
            params = (package_name,)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params = params + (limit,)
        
        history_rows = self.query(query, params)
        records = []
        
        for row in history_rows:
            # Create InstallationRecord object
            records.append(InstallationRecord.from_dict(row))
        
        return records
    
    def get_database_version(self) -> int:
        """
        Get the current database schema version.
        
        Returns:
            int: Current schema version
        """
        try:
            result = self.query("""
                SELECT MAX(version) as version FROM database_version
            """)
            return result[0]['version'] if result else 0
        except sqlite3.OperationalError:
            # Table doesn't exist yet
            return 0
