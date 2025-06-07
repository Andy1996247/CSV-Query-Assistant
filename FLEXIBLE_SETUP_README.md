# 🔥 Flexible Browser Use Setup

A comprehensive browser automation setup supporting multiple LLM providers with dynamic model selection.

## 🎯 Features

- **Multi-Provider Support**: OpenAI, Anthropic, Google, and [OpenRouter](https://openrouter.ai/docs/quickstart)
- **Dynamic Model Selection**: Choose models through environment variables or interactive mode
- **Automatic Provider Detection**: Only shows available providers based on configured API keys
- **OpenRouter Integration**: Access hundreds of models through a single API
- **Interactive Mode**: User-friendly provider and model selection
- **Flexible Configuration**: Environment-based or runtime configuration

## 🚀 Quick Start

### 1. Configure API Keys

Your `.env` file is already set up with your OpenAI key. Add other provider keys as needed:

```bash
# === API KEYS ===
OPENAI_API_KEY=sk-proj-... # ✅ Already configured
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# === PROVIDER SELECTION ===
LLM_PROVIDER=openai  # Change this to switch providers

# === MODEL SELECTION ===
OPENAI_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620
GOOGLE_MODEL=gemini-1.5-pro
OPENROUTER_MODEL=openai/gpt-4o
```

### 2. Run with Default Settings

```bash
source browser_use_env/bin/activate
python flexible_browser_use.py
```

### 3. Enable Interactive Mode

Set `INTERACTIVE_MODE=true` in `.env` for guided provider/model selection:

```bash
python flexible_browser_use.py
```

## 🔧 Provider Configuration

### OpenAI (✅ Ready)
```bash
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o  # or gpt-4o-mini, gpt-4-turbo
```

### Anthropic (Claude)
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Update `.env`:
   ```bash
   ANTHROPIC_API_KEY=your_actual_key
   LLM_PROVIDER=anthropic
   ANTHROPIC_MODEL=claude-3-5-sonnet-20240620
   ```

### Google (Gemini)
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Update `.env`:
   ```bash
   GOOGLE_API_KEY=your_actual_key
   LLM_PROVIDER=google
   GOOGLE_MODEL=gemini-1.5-pro
   ```

### OpenRouter (🔥 Recommended for Variety)
1. Get API key from [OpenRouter](https://openrouter.ai/keys)
2. Update `.env`:
   ```bash
   OPENROUTER_API_KEY=your_actual_key
   LLM_PROVIDER=openrouter
   OPENROUTER_MODEL=openai/gpt-4o  # or any available model
   ```

#### Popular OpenRouter Models:
- `openai/gpt-4o` - OpenAI's latest
- `anthropic/claude-3-5-sonnet` - Anthropic's best
- `google/gemini-pro` - Google's flagship
- `meta-llama/llama-3.1-405b` - Meta's largest
- `mistralai/mistral-large` - Mistral's top model
- `cohere/command-r-plus` - Cohere's latest

## 📋 Usage Examples

### Basic Usage (Environment-based)
```python
# Uses settings from .env file
python flexible_browser_use.py
```

### Interactive Mode
Set `INTERACTIVE_MODE=true` in `.env`, then:
```bash
python flexible_browser_use.py
```
You'll see:
```
🔧 Available LLM Providers:
  1. OPENAI
  2. ANTHROPIC
  3. GOOGLE
  4. OPENROUTER

Select provider (1-4) or press Enter for default (openai):
```

### Switching Providers Quickly
```bash
# Use OpenAI
echo "LLM_PROVIDER=openai" >> .env

# Use Claude
echo "LLM_PROVIDER=anthropic" >> .env

# Use OpenRouter with different model
echo "LLM_PROVIDER=openrouter" >> .env
echo "OPENROUTER_MODEL=meta-llama/llama-3.1-405b" >> .env
```

## 🎮 Custom Tasks

The script will prompt for your task, or you can modify the default:

```python
# Example tasks you can try:
"Go to Google and search for 'latest AI news'"
"Visit GitHub and find trending Python repositories"
"Go to weather.com and tell me the weather in New York"
"Search for 'browser automation' on DuckDuckGo and summarize results"
"Go to news.ycombinator.com and get the top 3 story titles"
```

## ⚙️ Advanced Configuration

### Model Temperature
All models are set to `temperature=0.0` for consistent results. Modify in `flexible_browser_use.py` if needed.

### OpenRouter Headers
For OpenRouter usage statistics and rankings:
```bash
OPENROUTER_SITE_URL=https://your-site.com
OPENROUTER_SITE_NAME=Your App Name
```

### Browser Settings
Customize browser behavior:
```python
browser_config = {
    "headless": False,  # Show browser window
    "viewport": {"width": 1280, "height": 720},
    "highlight_elements": True,
}
```

## 🔍 Debugging

### Enable Debug Mode
```bash
BROWSER_USE_LOGGING_LEVEL=debug
```

### Test Configuration
```bash
python test_setup.py
```

### Check Available Providers
The script automatically detects which providers have valid API keys configured.

## 💡 Cost Optimization Tips

### Using OpenRouter for Cost Efficiency
OpenRouter provides access to the same models at competitive prices:

1. **GPT-4o via OpenRouter**: Often cheaper than direct OpenAI API
2. **Alternative Models**: Try `anthropic/claude-3-5-haiku` for faster, cheaper responses
3. **Open Source Options**: Use `meta-llama/llama-3.1-70b` for cost-effective automation

### Model Selection by Use Case
- **Complex reasoning**: `openai/gpt-4o`, `anthropic/claude-3-5-sonnet`
- **Fast responses**: `openai/gpt-4o-mini`, `anthropic/claude-3-5-haiku`
- **Cost-effective**: OpenRouter's open-source models
- **Specialized tasks**: Google's `gemini-1.5-pro` for multimodal tasks

## 🛠️ Available Scripts

| Script | Purpose |
|--------|---------|
| `flexible_browser_use.py` | Main flexible automation script |
| `simple_browser_use.py` | Basic OpenAI-only example |
| `advanced_browser_use.py` | Advanced features demonstration |
| `test_setup.py` | Environment and setup testing |
| `create_env.py` | Generate comprehensive .env file |

## 🔗 Links and Resources

- [OpenRouter Documentation](https://openrouter.ai/docs/quickstart) - Access hundreds of models
- [Browser-use GitHub](https://github.com/browser-use/browser-use) - Original project
- [OpenAI Models](https://platform.openai.com/docs/models) - OpenAI model documentation
- [Anthropic Models](https://docs.anthropic.com/claude/docs/models-overview) - Claude model info
- [Google AI Models](https://ai.google.dev/models) - Gemini model details

## 🚦 Environment Variables Reference

### Required (at least one)
- `OPENAI_API_KEY` ✅ (configured)
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY` 
- `OPENROUTER_API_KEY`

### Configuration
- `LLM_PROVIDER` - Provider choice (openai, anthropic, google, openrouter)
- `INTERACTIVE_MODE` - Enable interactive selection (true/false)
- `*_MODEL` - Specific model for each provider

### Optional
- `BROWSER_USE_LOGGING_LEVEL` - Debug level
- `ANONYMIZED_TELEMETRY` - Telemetry setting
- `OPENROUTER_SITE_URL` - For OpenRouter rankings
- `OPENROUTER_SITE_NAME` - For OpenRouter rankings

## 🎉 Ready to Go!

Your setup is now configured with maximum flexibility. You can:

1. **Start immediately** with OpenAI (already configured)
2. **Add more providers** by updating API keys in `.env`
3. **Switch models easily** by changing environment variables
4. **Use interactive mode** for guided selection
5. **Access hundreds of models** through OpenRouter

Run `python flexible_browser_use.py` to get started! 🚀 