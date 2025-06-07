#!/usr/bin/env python3
"""
Browser Use Web Interface (FIXED VERSION)
A modern chat-based frontend for browser automation with AI configuration.
Bug fixes and improvements included.
"""

import streamlit as st
import asyncio
import os
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
import html

# Import our browser use modules with error handling
try:
    from flexible_browser_use import (
        create_openai_llm, create_anthropic_llm, create_google_llm, 
        create_openrouter_llm, get_available_providers, run_task_with_llm
    )
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.error("Please ensure flexible_browser_use.py is in the same directory.")
    st.stop()

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Browser Use AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern chat UI
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: #3b82f6;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        margin-left: 20%;
        text-align: right;
        word-wrap: break-word;
        max-width: 75%;
        float: right;
        clear: both;
    }
    
    .ai-message {
        background: #e5e7eb;
        color: #1f2937;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        margin-right: 20%;
        word-wrap: break-word;
        max-width: 75%;
        float: left;
        clear: both;
    }
    
    .status-success {
        background: #dcfce7;
        color: #166534;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #22c55e;
        margin: 0.5rem 0;
    }
    
    .status-error {
        background: #fef2f2;
        color: #991b1b;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #ef4444;
        margin: 0.5rem 0;
    }
    
    .status-running {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #f59e0b;
        margin: 0.5rem 0;
    }
    
    .status-warning {
        background: #fefce8;
        color: #854d0e;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #eab308;
        margin: 0.5rem 0;
    }
    
    .chat-clear {
        clear: both;
        height: 10px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables with better defaults."""
    defaults = {
        "chat_history": [],
        "current_task": "",
        "task_running": False,
        "llm_provider": os.getenv("LLM_PROVIDER", "openai"),
        "model_name": "",
        "last_error": None,
        "task_count": 0
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def validate_api_key(key_value):
    """Validate API key format."""
    if not key_value or key_value.strip() == "":
        return False
    if key_value in ["your_api_key_here", "your_openai_api_key_here", "your_anthropic_api_key_here"]:
        return False
    if len(key_value.strip()) < 10:  # Basic length check
        return False
    return True

def save_api_keys(openai_key, anthropic_key, google_key, openrouter_key):
    """Save API keys to environment file with validation."""
    try:
        # Validate at least one key is provided
        valid_keys = [
            validate_api_key(openai_key),
            validate_api_key(anthropic_key),
            validate_api_key(google_key),
            validate_api_key(openrouter_key)
        ]
        
        if not any(valid_keys):
            st.error("❌ Please provide at least one valid API key")
            return False
        
        env_content = f"""# === API KEYS ===
OPENAI_API_KEY={openai_key.strip() if openai_key else ''}
ANTHROPIC_API_KEY={anthropic_key.strip() if anthropic_key else ''}
GOOGLE_API_KEY={google_key.strip() if google_key else ''}
OPENROUTER_API_KEY={openrouter_key.strip() if openrouter_key else ''}

# === PROVIDER SELECTION ===
LLM_PROVIDER={st.session_state.llm_provider}

# === MODEL SELECTION ===
OPENAI_MODEL={os.getenv('OPENAI_MODEL', 'gpt-4o')}
ANTHROPIC_MODEL={os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20240620')}
GOOGLE_MODEL={os.getenv('GOOGLE_MODEL', 'gemini-1.5-pro')}
OPENROUTER_MODEL={os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o')}

# === BROWSER USE SETTINGS ===
BROWSER_USE_LOGGING_LEVEL=debug
ANONYMIZED_TELEMETRY=false
INTERACTIVE_MODE=false

# === OPENROUTER SPECIFIC ===
OPENROUTER_SITE_URL=https://your-site.com
OPENROUTER_SITE_NAME=Browser Use Automation
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        # Reload environment
        load_dotenv(override=True)
        return True
        
    except Exception as e:
        st.error(f"❌ Error saving API keys: {str(e)}")
        return False

def render_chat_history():
    """Render the chat history in a modern chat format with proper escaping."""
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            timestamp = message.get("timestamp", "")
            # Escape HTML content to prevent XSS
            safe_content = html.escape(str(message["content"]))
            
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {safe_content}<br>
                    <small style="opacity: 0.7;">{timestamp}</small>
                </div>
                <div class="chat-clear"></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>🤖 AI Agent:</strong> {safe_content}<br>
                    <small style="opacity: 0.7;">{timestamp}</small>
                </div>
                <div class="chat-clear"></div>
                """, unsafe_allow_html=True)

def get_model_options(provider):
    """Get available models for the selected provider with better organization."""
    models = {
        "openai": [
            "gpt-4o",
            "gpt-4o-mini", 
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ],
        "anthropic": [
            "claude-3-5-sonnet-20240620",
            "claude-3-5-haiku-20241022", 
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ],
        "google": [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-pro-vision"
        ],
        "openrouter": [
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "anthropic/claude-3-5-sonnet",
            "anthropic/claude-3-5-haiku",
            "google/gemini-pro",
            "meta-llama/llama-3.1-405b",
            "mistralai/mistral-large",
            "cohere/command-r-plus"
        ]
    }
    return models.get(provider, [])

async def run_browser_task(task, provider, model=None):
    """Run browser automation task with comprehensive error handling."""
    try:
        # Validate inputs
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")
        
        if not provider:
            raise ValueError("Provider must be specified")
        
        # Create LLM based on provider with error handling
        llm = None
        if provider == "openai":
            llm = create_openai_llm(model)
        elif provider == "anthropic":
            llm = create_anthropic_llm(model)
        elif provider == "google":
            llm = create_google_llm(model)
        elif provider == "openrouter":
            llm = create_openrouter_llm(model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        if not llm:
            raise ValueError(f"Failed to create LLM for provider: {provider}")
        
        # Run the task with timeout
        result = await asyncio.wait_for(
            run_task_with_llm(task.strip(), llm),
            timeout=300  # 5 minute timeout
        )
        
        return result, None
        
    except asyncio.TimeoutError:
        return None, "Task timed out after 5 minutes. Please try a simpler task."
    except ValueError as e:
        return None, f"Configuration error: {str(e)}"
    except Exception as e:
        # Get full traceback for debugging
        error_traceback = traceback.format_exc()
        print(f"Debug - Full error traceback:\n{error_traceback}")
        return None, f"Execution error: {str(e)}"

def check_system_requirements():
    """Check if all system requirements are met."""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
    
    # Check if browser_use is available
    try:
        import browser_use
    except ImportError:
        issues.append("browser_use package not installed")
    
    # Check if playwright is available
    try:
        import playwright
    except ImportError:
        issues.append("playwright package not installed")
    
    return issues

def main():
    """Main Streamlit application with enhanced error handling."""
    
    # Check system requirements
    system_issues = check_system_requirements()
    if system_issues:
        st.error("❌ System Requirements Issues:")
        for issue in system_issues:
            st.error(f"• {issue}")
        st.error("Please resolve these issues before continuing.")
        st.stop()
    
    initialize_session_state()
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("## ⚙️ AI Configuration")
        
        # Provider selection with error handling
        try:
            available_providers = get_available_providers()
        except Exception as e:
            st.error(f"Error getting providers: {e}")
            available_providers = ["openai", "anthropic", "google", "openrouter"]
        
        if not available_providers:
            available_providers = ["openai", "anthropic", "google", "openrouter"]
            st.markdown('<div class="status-warning">⚠️ No providers configured. Please add API keys.</div>', unsafe_allow_html=True)
        
        # Safe provider selection
        try:
            current_index = available_providers.index(st.session_state.llm_provider) if st.session_state.llm_provider in available_providers else 0
        except (ValueError, IndexError):
            current_index = 0
        
        provider = st.selectbox(
            "Select AI Provider",
            available_providers,
            index=current_index,
            help="Choose your preferred AI provider"
        )
        st.session_state.llm_provider = provider
        
        # Model selection with error handling
        model_options = get_model_options(provider)
        if model_options:
            try:
                model = st.selectbox(
                    f"Select {provider.title()} Model",
                    model_options,
                    index=0,
                    help=f"Choose the specific {provider} model to use"
                )
                st.session_state.model_name = model
            except Exception as e:
                st.error(f"Error in model selection: {e}")
                st.session_state.model_name = model_options[0] if model_options else ""
        
        # API Key configuration
        st.markdown("### 🔑 API Keys")
        
        with st.expander("Configure API Keys", expanded=False):
            openai_key = st.text_input(
                "OpenAI API Key", 
                value=os.getenv("OPENAI_API_KEY", ""),
                type="password",
                help="Get your key from https://platform.openai.com/api-keys",
                key="openai_key_input"
            )
            
            anthropic_key = st.text_input(
                "Anthropic API Key", 
                value=os.getenv("ANTHROPIC_API_KEY", ""),
                type="password",
                help="Get your key from https://console.anthropic.com/",
                key="anthropic_key_input"
            )
            
            google_key = st.text_input(
                "Google API Key", 
                value=os.getenv("GOOGLE_API_KEY", ""),
                type="password",
                help="Get your key from https://makersuite.google.com/app/apikey",
                key="google_key_input"
            )
            
            openrouter_key = st.text_input(
                "OpenRouter API Key", 
                value=os.getenv("OPENROUTER_API_KEY", ""),
                type="password",
                help="Get your key from https://openrouter.ai/keys",
                key="openrouter_key_input"
            )
            
            if st.button("💾 Save API Keys", key="save_keys_btn"):
                if save_api_keys(openai_key, anthropic_key, google_key, openrouter_key):
                    st.success("✅ API keys saved successfully!")
                    st.balloons()
                    # Force a rerun to update the provider list
                    st.rerun()
        
        # Browser settings
        st.markdown("### 🌐 Browser Settings")
        
        headless = st.checkbox(
            "Headless Mode", 
            value=False, 
            help="Run browser without GUI for faster execution"
        )
        show_highlights = st.checkbox(
            "Highlight Elements", 
            value=True, 
            help="Highlight interacted elements for better visibility"
        )
        
        # Status section with enhanced checks
        st.markdown("### 📊 Status")
        
        # Check API key status
        current_key = os.getenv(f"{provider.upper()}_API_KEY")
        if validate_api_key(current_key):
            st.markdown('<div class="status-success">✅ API Key Configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ API Key Missing</div>', unsafe_allow_html=True)
        
        # Task running status
        if st.session_state.task_running:
            st.markdown('<div class="status-running">🔄 Task Running...</div>', unsafe_allow_html=True)
        
        # Show task count
        if st.session_state.task_count > 0:
            st.markdown(f'<div class="status-success">📊 Tasks Completed: {st.session_state.task_count}</div>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<h1 class="main-header">🤖 Browser Use AI Assistant</h1>', unsafe_allow_html=True)
    
    current_model = st.session_state.model_name if st.session_state.model_name else "Default Model"
    st.markdown(f"""
    <div style="background: #f1f5f9; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
        <strong>Current Setup:</strong> {provider.title()} • {current_model}
        <br><small>Status: {'✅ Ready' if validate_api_key(os.getenv(f"{provider.upper()}_API_KEY")) else '❌ API Key Required'}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    st.markdown("## 💬 Chat with AI Agent")
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        render_chat_history()
    
    # Input area
    st.markdown("### 📝 Give your AI agent a task:")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        task_input = st.text_area(
            "Enter your browser automation task:",
            value="",  # Don't persist the current task to avoid confusion
            placeholder="Examples:\n• Go to Google and search for 'latest AI news'\n• Visit GitHub and find trending Python repositories\n• Go to weather.com and tell me the weather in New York",
            height=100,
            key="task_input_field",
            help="Describe what you want the AI to do in the browser"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        
        # Check if we can start a task
        can_start_task = (
            not st.session_state.task_running and 
            task_input and 
            task_input.strip() and 
            validate_api_key(os.getenv(f"{provider.upper()}_API_KEY"))
        )
        
        start_button = st.button(
            "🚀 Start Task",
            type="primary",
            disabled=not can_start_task,
            use_container_width=True,
            help="Click to start the browser automation task"
        )
        
        if st.button("🗑️ Clear Chat", use_container_width=True, help="Clear the conversation history"):
            st.session_state.chat_history = []
            st.session_state.last_error = None
            st.rerun()
    
    # Handle task execution
    if start_button and task_input and task_input.strip():
        # Validate API key one more time
        if not validate_api_key(os.getenv(f"{provider.upper()}_API_KEY")):
            st.error(f"❌ {provider.upper()} API key is not configured. Please add it in the sidebar.")
            st.stop()
        
        # Add user message to chat
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "role": "user",
            "content": task_input.strip(),
            "timestamp": timestamp
        })
        
        st.session_state.task_running = True
        
        # Show running status
        with st.spinner(f"🤖 AI Agent is working on your task using {provider.title()} ({current_model})..."):
            try:
                # Run the browser task
                result, error = asyncio.run(run_browser_task(
                    task_input.strip(), 
                    provider, 
                    st.session_state.model_name
                ))
                
                if error:
                    # Add error message to chat
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"❌ Error: {error}",
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    st.session_state.last_error = error
                else:
                    # Add success message to chat
                    result_text = str(result) if result else "Task completed successfully!"
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"✅ Task completed!\n\n{result_text}",
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    st.session_state.task_count += 1
                    st.session_state.last_error = None
                
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"❌ {error_msg}",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.session_state.last_error = error_msg
        
        st.session_state.task_running = False
        st.rerun()
    
    # Example tasks
    st.markdown("### 💡 Example Tasks")
    
    examples = [
        "Go to Google and search for 'latest AI news'",
        "Visit GitHub and find trending Python repositories", 
        "Go to httpbin.org/get and tell me my IP address",
        "Search for 'browser automation' on DuckDuckGo",
        "Go to news.ycombinator.com and get the top 3 story titles"
    ]
    
    # Create columns for example buttons
    cols = st.columns(min(len(examples), 3))  # Max 3 columns
    for i, example in enumerate(examples):
        col_idx = i % len(cols)
        with cols[col_idx]:
            if st.button(
                f"📄 {example[:25]}...", 
                key=f"example_{i}", 
                use_container_width=True,
                help=example
            ):
                # Set the example in the text area
                st.session_state.current_task = example
                st.rerun()
    
    # Footer with useful links
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
        🤖 Browser Use AI Assistant • Powered by Browser-Use Framework<br>
        <a href="https://github.com/browser-use/browser-use" target="_blank">GitHub</a> • 
        <a href="https://openrouter.ai/docs/quickstart" target="_blank">OpenRouter Docs</a> •
        <a href="https://docs.streamlit.io/" target="_blank">Streamlit Docs</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 