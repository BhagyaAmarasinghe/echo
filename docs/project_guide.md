# Echo Project Comprehensive Guide

## Overview

Echo is a smart Linux package recommendation system powered by AI that helps users discover, install, and manage packages based on their workflow and usage patterns. The project combines system package detection, usage analysis, and AI-powered recommendations to provide intelligent package suggestions.

## Project Structure

```
echo/
├── LICENSE                 # MIT License
├── README.md               # Project overview and documentation
├── pyproject.toml          # Python build system configuration
├── requirements.txt        # Project dependencies
├── setup.py                # Package installation and metadata
├── src/
│   └── echo/
│       ├── __init__.py     # Exports PackageRecommender and version
│       ├── config.py       # Configuration settings
│       ├── cli.py          # Command-line interface
│       ├── main.py         # Core PackageRecommender class
│       ├── database/       # Database management
│       ├── services/       # Core service modules
│       ├── utils/          # Utility functions
│       └── reports/        # Report generation
├── tests/                  # Test suite
├── examples/               # Usage examples
└── docs/                   # Documentation
```

## Key Components

### Core Components

1. **PackageRecommender** (`main.py`)
   - Main class that orchestrates all services
   - Provides API for package recommendations
   - Integrates various data sources for intelligent suggestions

2. **Command-Line Interface** (`cli.py`)
   - Built with Click and Rich libraries
   - Provides interactive commands for package management
   - Supports workflow-based recommendations

3. **Configuration** (`config.py`)
   - Central configuration settings
   - Paths, API endpoints, defaults, etc.

### Database Module

1. **Database Manager** (`database/database.py`)
   - SQLite-based database with Liquibase schema management
   - Handles all data persistence operations
   - Manages database connections and queries

2. **Data Models** (`database/models.py`)
   - Package - System package information
   - UsagePattern - How packages are used
   - Recommendation - Package suggestions
   - InstallationRecord - Installation history

3. **Schema Management** (`database/migrations/`)
   - Liquibase XML changesets
   - Version-controlled schema changes
   - Support for schema upgrades and rollbacks

### Services

1. **Package Detector** (`services/package_detector.py`)
   - Detects installed packages on the system
   - Supports different Linux distributions (Ubuntu, Fedora, CentOS, etc.)
   - Extracts package metadata and dependencies

2. **Package Manager** (`services/package_manager.py`)
   - Installs and removes packages
   - Interfaces with system package managers (apt, dnf, yum)
   - Records installation history

3. **Log Analyzer** (`services/log_analyzer.py`)
   - Analyzes system logs to determine package usage patterns
   - Identifies frequently used packages
   - Tracks usage contexts and frequencies

4. **AI Recommender** (`services/ai_recommender.py`)
   - Integrates with Ollama for AI-powered recommendations
   - Generates intelligent suggestions based on workflow descriptions
   - Combines package metadata with usage patterns

5. **Similarity Analyzer** (`services/similarity_analyzer.py`)
   - Finds packages similar to ones the user already uses
   - Calculates similarity scores between packages
   - Recommends complementary tools

### Utilities and Reports

1. **Logger** (`utils/logger.py`)
   - Configurable logging setup
   - Consistent logging across modules

2. **System Utilities** (`utils/system.py`)
   - Distribution detection
   - System-specific operations

3. **Report Generator** (`reports/report_generator.py`)
   - Creates recommendation reports
   - Formats results for display

## Key Technologies

1. **Python 3.8+** - Core programming language
2. **SQLite** - File-based database
3. **Liquibase** - Database schema management
4. **Click** - Command-line interface framework
5. **Rich** - Terminal UI formatting
6. **Ollama** - AI model integration
7. **Pytest** - Testing framework

## Workflows

### Installation Workflow

1. User installs Echo: `pip install echo`
2. Echo initializes database in `~/.echo/echo.db`
3. Echo detects the Linux distribution and available package managers

### Recommendation Workflow

1. User requests recommendations: `echo recommend -w "data science tools"`
2. Echo analyzes installed packages and usage patterns
3. Echo sends workflow description to AI recommender
4. Echo combines AI suggestions with similarity analysis
5. Echo presents recommendations to the user

### Package Management Workflow

1. User requests package installation: `echo install jupyter pandas`
2. Echo shows package details and confirms with user
3. Echo calls appropriate system package manager (apt, dnf, etc.)
4. Echo records installation result in database
5. Echo updates usage patterns based on the installation

## Database Schema

### Tables

1. **packages** - System packages
   - name (TEXT, PK)
   - version (TEXT)
   - description (TEXT)
   - installed_date (TIMESTAMP)
   - source (TEXT)
   - size (INTEGER)
   - metadata (TEXT)

2. **package_dependencies** - Package dependencies
   - package_name (TEXT, PK, FK)
   - dependency_name (TEXT, PK)

3. **package_tags** - Package tags
   - package_name (TEXT, PK, FK)
   - tag (TEXT, PK)

4. **usage_patterns** - Usage statistics
   - package_name (TEXT, PK, FK)
   - frequency (INTEGER)
   - last_used (TIMESTAMP)
   - importance_score (REAL)
   - metadata (TEXT)

5. **usage_contexts** - Usage contexts
   - package_name (TEXT, PK, FK)
   - context (TEXT, PK)

6. **recommendations** - Package recommendations
   - id (INTEGER, PK, autoincrement)
   - package_name (TEXT)
   - score (REAL)
   - reason (TEXT)
   - category (TEXT)
   - timestamp (TIMESTAMP)
   - source (TEXT)
   - metadata (TEXT)

7. **installation_history** - Installation records
   - id (INTEGER, PK, autoincrement)
   - package_name (TEXT)
   - operation (TEXT)
   - timestamp (TIMESTAMP)
   - success (BOOLEAN)
   - details (TEXT)

8. **database_version** - Schema version tracking
   - version (INTEGER, PK)
   - applied_at (TIMESTAMP)
   - description (TEXT)

## API Examples

### Python API

```python
from echo import PackageRecommender

# Initialize recommender
recommender = PackageRecommender()

# Get recommendations
workflow = "I need tools for web development with Python"
recommendations = recommender.get_recommendations(workflow)

# Print top recommendations
for rec in recommendations['ai_suggestions'][:3]:
    print(f"{rec['package']} - {rec['reason']} (Score: {rec['score']:.2f})")
```

### CLI Commands

```bash
# Get recommendations
echo recommend -w "data science tools"

# Install packages
echo install jupyter pandas scikit-learn

# Search for packages
echo search jupyter

# Show package info
echo info pandas

# View installation history
echo history
```

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/echo.git
   cd echo
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

5. **Setup Liquibase (optional):**
   ```bash
   # Install Liquibase
   # Details depend on your OS
   ```

## Testing Strategy

1. **Unit Tests:**
   - Test each service in isolation
   - Mock external dependencies

2. **Integration Tests:**
   - Test interactions between services
   - Use temporary databases

3. **System Tests:**
   - Test full workflows
   - Command-line interface tests

## Architecture Considerations

### Multi-Distribution Support

Echo supports multiple Linux distributions by:
- Detecting the distribution at runtime
- Using distribution-specific commands for package operations
- Handling different package formats and metadata

### Extensibility

Echo is designed for extensibility:
- Service-based architecture for modular development
- Well-defined interfaces between components
- Database abstraction for potential future changes

### Performance

Performance considerations include:
- Caching package information for faster lookups
- Efficient database queries with proper indexing
- Minimizing system command calls

## AWS Architecture (Future)

Echo's AWS architecture includes:
- ECS Fargate for containerized services
- RDS for PostgreSQL database
- ElasticSearch for log analysis
- S3 for storage
- Lambda for serverless functions

See `Echo AWS Architecture with Tools.mermaid` for the detailed architecture diagram.

## Roadmap

1. **Version 0.1.0** (Current)
   - Core package recommendation
   - Basic CLI
   - SQLite database

2. **Version 0.2.0**
   - Enhanced AI recommendations
   - Package dependency visualization
   - Performance improvements

3. **Version 0.3.0**
   - Web API
   - Cloud synchronization
   - Multi-user support

4. **Version 1.0.0**
   - Stable API
   - Comprehensive documentation
   - Production readiness

## Troubleshooting

### Common Issues

1. **Database initialization fails:**
   - Check if the database directory is writable
   - Verify SQLite is properly installed
   - Check Liquibase installation if using it

2. **Package operations fail:**
   - Ensure proper permissions for package management
   - Verify the detected distribution is correct
   - Check network connectivity for package downloads

3. **AI recommendations unavailable:**
   - Verify Ollama is installed and running
   - Check API endpoint configuration
   - Ensure network connectivity

## Documentation Resources

1. **README.md** - Project overview and quick start
2. **docs/installation.md** - Detailed installation instructions
3. **docs/cli.md** - Command-line interface documentation
4. **docs/api.md** - Python API documentation
5. **examples/** - Example scripts showing usage patterns

## Contributing Guidelines

1. **Code Style:**
   - Follow PEP 8 guidelines
   - Use Black for formatting
   - Write docstrings for all functions and classes

2. **Testing:**
   - Write tests for all new functionality
   - Maintain 80%+ code coverage
   - Use pytest for all tests

3. **Pull Requests:**
   - Create feature branches from develop
   - Include tests with all changes
   - Update documentation as needed
   - Reference issues in PR descriptions

## Contact and Support

- GitHub Issues: https://github.com/yourusername/echo/issues
- Documentation: https://echo-package.readthedocs.io/
- Contact: your.email@example.com