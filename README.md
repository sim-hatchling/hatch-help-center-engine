# Hatch Help Center Engine

A Python-based system for managing the Hatch Help Center content through Intercom's API.

## Core Components

### Services

- `intercom_service.py`: Wrapper for Intercom's API with proper error handling and response formatting

### Utilities

- `html_helpers.py`: Common HTML element creation functions
- `article_formatter.py`: Article content formatting and cleaning utilities

## Setup

1. Clone the repository:
```bash
git clone https://github.com/sim-hatchling/hatch-help-center-engine.git
cd hatch-help-center-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Article Formatting

```python
from utils.article_formatter import format_content

# Format markdown content
html = format_content(markdown_content)

# Format with title
html = format_content(markdown_content, add_title=True, title="Article Title")
```

### Intercom API

```python
from services.intercom_service import IntercomService
from config import Config

# Initialize service
intercom = IntercomService(Config.INTERCOM_ACCESS_TOKEN)

# Create article
response = intercom.create_article(
    title="Article Title",
    body=article_content
)

# Update article
response = intercom.update_article(
    article_id="123",
    body=updated_content
)
```

## Development

### Code Style

- Use type hints
- Follow PEP 8
- Add docstrings to all functions
- Keep functions focused and modular

### Testing

Before committing:
1. Test any new functionality
2. Verify API responses
3. Check content formatting in Intercom

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT