# 🤖 Browser Use AI Frontend

A modern, chat-based web interface for browser automation with AI. This frontend provides an intuitive way to interact with browser-use through a beautiful chat interface with comprehensive AI provider configuration.

![Browser Use UI](https://via.placeholder.com/800x500/1f2937/ffffff?text=Browser+Use+AI+Interface)

## ✨ Features

### 🎯 **Chat Interface**
- Modern chat-style UI similar to ChatGPT/Claude
- Real-time conversation with AI agent
- Task progress tracking and status updates
- Chat history with timestamps

### ⚙️ **Multi-Provider AI Support**
- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- **Anthropic**: Claude-3.5-Sonnet, Claude-3.5-Haiku, Claude-3-Opus
- **Google**: Gemini-1.5-Pro, Gemini-1.5-Flash, Gemini-Pro
- **OpenRouter**: Access to 200+ models (GPT-4o, Claude, Llama, Mistral, etc.)

### 🔧 **Configuration Panel**
- API key management for all providers
- Model selection per provider
- Browser settings (headless mode, element highlighting)
- Real-time status monitoring
- Settings persistence in `.env` file

### 🚀 **Browser Automation**
- Automated web browsing with AI guidance
- Task execution with natural language commands
- Error handling and detailed feedback
- Example tasks for quick start

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12+ with browser-use environment already set up
- Streamlit installed in the environment

### Quick Start

1. **Start the UI**:
   ```bash
   python run_ui.py
   ```
   Or directly:
   ```bash
   source browser_use_env/bin/activate
   streamlit run browser_use_ui.py
   ```

2. **Open your browser** to: `http://localhost:8501`

3. **Configure API Keys** (in the sidebar):
   - Click "Configure API Keys" to expand
   - Add your API keys for desired providers
   - Click "Save API Keys"

## 🔑 API Key Setup

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to the UI configuration

### Anthropic
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add it to the UI configuration

### Google AI
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add it to the UI configuration

### OpenRouter
1. Visit [OpenRouter Keys](https://openrouter.ai/keys)
2. Create an API key
3. Add it to the UI configuration

## 💬 Using the Chat Interface

### Basic Usage
1. **Select Provider**: Choose your AI provider from the sidebar
2. **Select Model**: Pick the specific model you want to use
3. **Enter Task**: Type your browser automation task in the text area
4. **Start Task**: Click the "🚀 Start Task" button
5. **Monitor Progress**: Watch the AI execute your task with real-time updates

### Example Tasks

#### 🔍 **Search & Research**
```
Go to Google and search for 'latest AI news' and tell me the top 3 headlines
```

#### 📈 **Data Gathering**
```
Visit GitHub and find the top 5 trending Python repositories this week
```

#### 🌐 **Web Navigation**
```
Go to news.ycombinator.com and get me the titles of the top 5 stories
```

#### 🔧 **API Testing**
```
Go to httpbin.org/get and tell me what my IP address is
```

#### 🛒 **E-commerce**
```
Go to Amazon and search for 'wireless headphones' and tell me the price of the first result
```

## 🎨 UI Components

### Sidebar Configuration
- **AI Configuration**: Provider and model selection
- **API Keys**: Secure key management with masked input
- **Browser Settings**: Headless mode, element highlighting
- **Status Monitor**: Real-time configuration status

### Main Chat Area
- **Header**: Current AI setup display
- **Chat History**: Conversation with timestamps
- **Input Area**: Task input with example placeholders
- **Action Buttons**: Start task, clear chat
- **Example Tasks**: Quick-start buttons

### Status Indicators
- ✅ **Green**: API key configured and ready
- ❌ **Red**: API key missing or invalid
- 🔄 **Yellow**: Task currently running

## 🚀 Advanced Features

### Multi-Provider Switching
Switch between AI providers seamlessly:
1. Select different provider in sidebar
2. Choose appropriate model
3. Ensure API key is configured
4. Start new tasks immediately

### Cost Optimization
- **OpenRouter**: Access cheaper models (Llama, Mistral)
- **Model Selection**: Choose appropriate model for task complexity
- **Provider Comparison**: Test different providers for best results

### Browser Settings
- **Headless Mode**: Run browser in background
- **Element Highlighting**: Visual feedback during automation
- **Debug Logging**: Detailed execution logs

## 🔧 Troubleshooting

### Common Issues

#### UI Won't Start
```bash
# Check if Streamlit is installed
source browser_use_env/bin/activate
pip install streamlit

# Run directly
streamlit run browser_use_ui.py
```

#### API Key Issues
- Ensure keys are properly formatted
- Check provider documentation for key format
- Verify account has sufficient credits
- Save keys through the UI configuration panel

#### Browser Tasks Fail
- Check if API key is configured for selected provider
- Verify internet connection
- Try simpler tasks first
- Check browser automation logs

#### Import Errors
```bash
# Ensure you're in the correct directory
cd /path/to/Bowsruse

# Check if flexible_browser_use.py exists
ls -la flexible_browser_use.py

# Activate environment
source browser_use_env/bin/activate
```

## 📊 Performance Tips

### Model Selection
- **GPT-4o**: Best for complex reasoning tasks
- **GPT-4o-mini**: Faster, cost-effective for simple tasks
- **Claude-3.5-Sonnet**: Excellent for detailed analysis
- **Gemini-1.5-Pro**: Good balance of speed and capability

### Task Optimization
- Be specific in your instructions
- Break complex tasks into smaller steps
- Use examples from the UI for guidance
- Monitor task execution in real-time

## 🛡️ Security & Best Practices

### API Key Security
- Keys are stored in `.env` file (add to `.gitignore`)
- UI input fields are masked for security
- Never share API keys publicly
- Rotate keys regularly

### Browser Safety
- Tasks run in isolated browser sessions
- No persistent data storage
- Automatic cleanup after tasks
- Safe defaults for all operations

## 🔄 Updates & Maintenance

### Updating the UI
```bash
# Pull latest changes
git pull origin main

# Restart the UI
python run_ui.py
```

### Environment Management
```bash
# Activate environment
source browser_use_env/bin/activate

# Update dependencies
pip install --upgrade streamlit browser-use

# Check status
pip list | grep -E "(streamlit|browser-use)"
```

## 📚 Resources

- [Browser-Use Documentation](https://github.com/browser-use/browser-use)
- [OpenRouter API Docs](https://openrouter.ai/docs/quickstart)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Anthropic API Reference](https://docs.anthropic.com/)
- [Google AI Documentation](https://ai.google.dev/)

## 🤝 Support

For issues and questions:
1. Check this README first
2. Review error messages in the UI
3. Check browser console for JavaScript errors
4. Verify API key configuration
5. Test with simple tasks first

---

**🎉 Enjoy your AI-powered browser automation experience!** 