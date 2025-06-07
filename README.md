# Browser Use AI Assistant

**An AI-powered browser automation framework with multi-provider support and modern web interface.**

This repository contains a comprehensive setup for [browser-use](https://github.com/browser-use/browser-use) with a beautiful chat-based frontend, supporting multiple AI providers including OpenAI, Anthropic, Google, and OpenRouter.

## ✨ Features

- 🤖 **Modern Chat Interface** - ChatGPT-style web UI for browser automation
- 🔧 **Multi-Provider Support** - OpenAI, Anthropic, Google, OpenRouter
- ⚙️ **Easy Configuration** - Web-based API key management
- 🌐 **Browser Automation** - Powered by browser-use framework
- 🔒 **Security First** - Secure API key handling and input validation

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

### 4. Start the Web Interface

Launch the modern chat interface:

```bash
python run_ui.py
```

Then open your browser to: `http://localhost:8501`

### 5. Configure API Keys

In the web interface sidebar:
1. Click "Configure API Keys" 
2. Add your API keys for desired providers
3. Click "Save API Keys"

## 🎯 Web Interface Features

### Chat-Based Automation
- Type natural language commands
- Real-time task execution
- Chat history with timestamps
- Example tasks for quick start

### Multi-Provider Configuration
- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-4-turbo
- **Anthropic**: Claude-3.5-Sonnet, Claude-3.5-Haiku
- **Google**: Gemini-1.5-Pro, Gemini-Flash
- **OpenRouter**: 200+ models including Llama, Mistral

### Example Tasks
```
Go to Google and search for 'latest AI news'
Visit GitHub and find trending Python repositories
Go to weather.com and tell me the weather in New York
```

## 📁 Files Overview

### `browser_use_ui.py`
Modern Streamlit-based web interface featuring:
- Chat-style conversation with AI agents
- Multi-provider AI configuration
- Real-time task execution and monitoring
- Secure API key management

### `flexible_browser_use.py`
Core automation engine with:
- Support for OpenAI, Anthropic, Google, OpenRouter
- Dynamic provider and model selection
- Environment-based configuration
- Interactive and automated modes

### `run_ui.py`
Simple launcher script for the web interface

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
