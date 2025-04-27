<div align="center">
  <h1>Echo</h1>
  <p>A smart Linux package recommendation system powered by AI 🚀</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
</div>

## ✨ Features

- 🔍 **Smart Detection** - Automatically detects installed packages across Linux distributions
- 📊 **Usage Analysis** - Analyzes system logs to understand your package usage patterns
- 🤖 **AI-Powered** - Uses Ollama for intelligent recommendations based on your workflow
- 📈 **Similarity Matching** - Suggests packages similar to ones you frequently use
- 🖥️ **Interactive CLI** - Rich command-line interface with interactive package selection
- 📝 **Detailed Reports** - Generates comprehensive recommendation reports
- 🔄 **History Tracking** - Maintains installation and usage history

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama
- Linux-based OS (Ubuntu, Debian, Fedora, RHEL, or CentOS)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/echo.git
cd echo

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt
pip install -e .
```

## 💻 Usage

### Get Recommendations
```bash
# Basic recommendations
echo recommend -w "I need data science tools"

# Interactive mode
echo recommend -w "data science tools" -i
```

### Package Management
```bash
# Install packages
echo install jupyter pandas scikit-learn

# Uninstall packages
echo uninstall jupyter
```

### Search and Info
```bash
# Search packages
echo search jupyter

# Get package details
echo info pandas
```

### View History
```bash
# Recent installations
echo history

# Last 20 operations
echo history --limit 20
```

## 🌟 Interactive Mode

Echo's interactive mode provides a rich CLI experience:

```bash
$ echo recommend -w "data science tools" -i

Recommended Packages
┌────────┬────────────┬─────────────────────────┬───────┐
│ Select │ Package    │ Description             │ Score │
├────────┼────────────┼─────────────────────────┼───────┤
│   1    │ jupyter    │ Interactive notebooks   │  0.95 │
│   2    │ pandas     │ Data analysis library   │  0.92 │
│   3    │ matplotlib │ Visualization toolkit   │  0.88 │
└────────┴────────────┴─────────────────────────┴───────┘

Enter numbers to install (e.g., 1,2): █
```

## 🔧 CLI Options

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Interactive package selection |
| `-v, --verbose` | Detailed output |
| `-y, --yes` | Auto-confirm prompts |
| `-h, --help` | Show help message |

## 📘 Python API

```python
from echo import PackageRecommender

recommender = PackageRecommender()
workflow = "I need data science tools"
recommendations = recommender.get_recommendations(workflow)
```

## 🛠️ Development

```bash
# Setup development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/

# Format code
black src/ tests/
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Ollama](https://github.com/ollama/ollama) for the AI model
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [Click](https://github.com/pallets/click) for CLI functionality

## 🗺️ Roadmap

- [ ] Package dependency visualization
- [ ] System resource usage tracking
- [ ] Custom recommendation profiles
- [ ] Integration with more package managers
- [ ] Package security scanning

## 📫 Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/BhagyaAmarasinghe/echo](https://github.com/BhagyaAmarasinghe/echo)

---
<div align="center">
  Made with ❤️ for the open-source community
</div>