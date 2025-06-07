# Browser Use Setup Guide

This repository contains examples and setup for [browser-use](https://github.com/browser-use/browser-use), an AI-powered browser automation framework.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key (or other supported LLM API keys)
- Linux/macOS/Windows with Chrome/Chromium installed

### 1. Environment Setup

Your virtual environment is already set up! Activate it:

```bash
source browser_use_env/bin/activate
```

### 2. Install Dependencies

Browser-use is already installed. Verify the installation:

```bash
pip list | grep browser-use
```

### 3. Install Browser Dependencies

Install Playwright browsers (this may take a few minutes):

```bash
playwright install chromium --with-deps --no-shell
```

### 4. Configure API Keys

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   # Required for OpenAI
   OPENAI_API_KEY=your_actual_openai_api_key_here
   
   # Optional for other LLMs
   ANTHROPIC_API_KEY=your_anthropic_key_here
   GOOGLE_API_KEY=your_google_key_here
   
   # Browser-use settings
   BROWSER_USE_LOGGING_LEVEL=debug
   ANONYMIZED_TELEMETRY=false
   ```

### 5. Run Examples

#### Simple Example
```bash
python simple_browser_use.py
```

#### Advanced Examples
```bash
python advanced_browser_use.py
```

## 📁 Files Overview

### `simple_browser_use.py`
A basic example that demonstrates:
- Setting up an OpenAI LLM
- Creating a browser agent
- Running a simple web search task
- Error handling and setup validation

### `advanced_browser_use.py`
Advanced examples showcasing:
- Custom browser profiles and settings
- Multiple LLM providers (OpenAI, Anthropic)
- Multi-tab browser automation
- Parallel agent execution
- Browser session reuse

### `.env.example`
Template for environment variables including:
- API keys for various LLM providers
- Browser-use configuration options
- Debug and telemetry settings

## 🔧 Configuration Options

### Browser Settings

```python
from browser_use import BrowserProfile, BrowserSession

# Custom browser profile
browser_profile = BrowserProfile(
    headless=False,  # Show browser window
    viewport={"width": 1280, "height": 720},
    user_agent="custom user agent",
    highlight_elements=True,  # Highlight interacted elements
    wait_for_network_idle_page_load_time=2.0,
    allowed_domains=['*.google.com', '*.wikipedia.org'],
)

# Browser session with profile
browser_session = BrowserSession(
    browser_profile=browser_profile,
    keep_alive=True,  # Reuse browser between agents
)
```

### LLM Providers

#### OpenAI (GPT-4o)
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
)
```

#### Anthropic (Claude)
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    timeout=60,
)
```

#### Google (Gemini)
```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.0,
)
```

## 📚 Common Use Cases

### Web Scraping
```python
agent = Agent(
    task="Go to news.ycombinator.com and extract the top 5 story titles",
    llm=llm,
)
```

### Form Filling
```python
agent = Agent(
    task="Go to example.com/contact, fill out the contact form with sample data",
    llm=llm,
)
```

### Research Tasks
```python
agent = Agent(
    task="Research the latest AI developments by searching multiple sources and create a summary",
    llm=llm,
)
```

### E-commerce Automation
```python
agent = Agent(
    task="Search for 'wireless headphones' on Amazon, compare the top 3 results by price and reviews",
    llm=llm,
)
```

## 🛡️ Security Best Practices

### Sensitive Data Handling
```python
# Use sensitive data placeholders
sensitive_data = {
    'https://*.example.com': {
        'x_username': 'actual_username',
        'x_password': 'actual_password',
    },
}

agent = Agent(
    task="Login to example.com using x_username and x_password",
    llm=llm,
    sensitive_data=sensitive_data,
    use_vision=False,  # Disable vision to prevent seeing entered values
)
```

### Domain Restrictions
```python
# Restrict domains the agent can visit
browser_session = BrowserSession(
    allowed_domains=['*.trusted-site.com', 'https://specific-site.com']
)
```

## 🔍 Debugging

### Enable Debug Logging
Add to your `.env` file:
```bash
BROWSER_USE_LOGGING_LEVEL=debug
```

### Disable Headless Mode
```python
browser_profile = BrowserProfile(headless=False)
```

### Element Highlighting
```python
browser_profile = BrowserProfile(highlight_elements=True)
```

## 📈 Performance Tips

1. **Reuse Browser Sessions**: Use `keep_alive=True` for multiple tasks
2. **Optimize Viewport**: Set appropriate viewport size for your tasks
3. **Network Idle Time**: Adjust `wait_for_network_idle_page_load_time` for slow sites
4. **Temperature Setting**: Use `temperature=0.0` for consistent results

## 🆘 Troubleshooting

### Common Issues

1. **Playwright Browser Not Found**
   ```bash
   playwright install chromium --with-deps --no-shell
   ```

2. **API Key Errors**
   - Check your `.env` file exists and has correct API keys
   - Ensure the `.env` file is in the same directory as your script

3. **Permission Errors**
   - On Linux, you may need to install additional dependencies
   - Run the chromium install command with `--with-deps` flag

4. **Import Errors**
   - Ensure your virtual environment is activated
   - Reinstall browser-use: `pip install browser-use --upgrade`

### Getting Help

- [Browser-use GitHub Issues](https://github.com/browser-use/browser-use/issues)
- [Browser-use Documentation](https://docs.browser-use.com/)
- [LangChain Documentation](https://python.langchain.com/docs/)

## 📝 License

This setup is based on the browser-use framework. See the [original repository](https://github.com/browser-use/browser-use) for license information. 