#!/usr/bin/env python3
"""
Browser Use Web Interface
A modern chat-based frontend for browser automation with AI configuration.
"""

import streamlit as st
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Import our browser use modules
from flexible_browser_use import (
    create_openai_llm, create_anthropic_llm, create_google_llm, 
    create_openrouter_llm, get_available_providers, run_task_with_llm
)

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
    }
    
    .ai-message {
        background: #e5e7eb;
        color: #1f2937;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        margin-right: 20%;
    }
    
    .status-success {
        background: #dcfce7;
        color: #166534;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #22c55e;
    }
    
    .status-error {
        background: #fef2f2;
        color: #991b1b;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #ef4444;
    }
    
    .status-running {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_task" not in st.session_state:
        st.session_state.current_task = ""
    if "task_running" not in st.session_state:
        st.session_state.task_running = False
    if "llm_provider" not in st.session_state:
        st.session_state.llm_provider = os.getenv("LLM_PROVIDER", "openai")
    if "model_name" not in st.session_state:
        st.session_state.model_name = ""

def save_api_keys(openai_key, anthropic_key, google_key, openrouter_key):
    """Save API keys to environment file."""
    env_content = f"""# === API KEYS ===
OPENAI_API_KEY={openai_key}
ANTHROPIC_API_KEY={anthropic_key}
GOOGLE_API_KEY={google_key}
OPENROUTER_API_KEY={openrouter_key}

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

def render_chat_history():
    """Render the chat history in a modern chat format."""
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            timestamp = message.get("timestamp", "")
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message["content"]}<br>
                    <small style="opacity: 0.7;">{timestamp}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>🤖 AI Agent:</strong> {message["content"]}<br>
                    <small style="opacity: 0.7;">{timestamp}</small>
                </div>
                """, unsafe_allow_html=True)

def get_model_options(provider):
    """Get available models for the selected provider."""
    models = {
        "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        "anthropic": ["claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
        "google": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
        "openrouter": ["openai/gpt-4o", "anthropic/claude-3-5-sonnet", "google/gemini-pro", 
                      "meta-llama/llama-3.1-405b", "mistralai/mistral-large", "cohere/command-r-plus"]
    }
    return models.get(provider, [])

async def run_browser_task(task, provider, model=None):
    """Run browser automation task."""
    try:
        # Create LLM based on provider
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
        
        # Run the task
        result = await run_task_with_llm(task, llm)
        return result, None
        
    except Exception as e:
        return None, str(e)

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("## ⚙️ AI Configuration")
        
        # Provider selection
        available_providers = get_available_providers()
        if not available_providers:
            available_providers = ["openai", "anthropic", "google", "openrouter"]
        
        provider = st.selectbox(
            "Select AI Provider",
            available_providers,
            index=available_providers.index(st.session_state.llm_provider) 
                  if st.session_state.llm_provider in available_providers else 0
        )
        st.session_state.llm_provider = provider
        
        # Model selection
        model_options = get_model_options(provider)
        if model_options:
            model = st.selectbox(
                f"Select {provider.title()} Model",
                model_options,
                index=0
            )
            st.session_state.model_name = model
        
        # API Key configuration
        st.markdown("### 🔑 API Keys")
        
        with st.expander("Configure API Keys", expanded=False):
            openai_key = st.text_input(
                "OpenAI API Key", 
                value=os.getenv("OPENAI_API_KEY", ""),
                type="password",
                help="Get your key from https://platform.openai.com/api-keys"
            )
            
            anthropic_key = st.text_input(
                "Anthropic API Key", 
                value=os.getenv("ANTHROPIC_API_KEY", ""),
                type="password",
                help="Get your key from https://console.anthropic.com/"
            )
            
            google_key = st.text_input(
                "Google API Key", 
                value=os.getenv("GOOGLE_API_KEY", ""),
                type="password",
                help="Get your key from https://makersuite.google.com/app/apikey"
            )
            
            openrouter_key = st.text_input(
                "OpenRouter API Key", 
                value=os.getenv("OPENROUTER_API_KEY", ""),
                type="password",
                help="Get your key from https://openrouter.ai/keys"
            )
            
            if st.button("💾 Save API Keys"):
                save_api_keys(openai_key, anthropic_key, google_key, openrouter_key)
                st.success("API keys saved successfully!")
                st.rerun()
        
        # Browser settings
        st.markdown("### 🌐 Browser Settings")
        
        headless = st.checkbox("Headless Mode", value=False, help="Run browser without GUI")
        show_highlights = st.checkbox("Highlight Elements", value=True, help="Highlight interacted elements")
        
        # Status
        st.markdown("### 📊 Status")
        
        # Check API key status
        current_key = os.getenv(f"{provider.upper()}_API_KEY")
        if current_key and current_key != "your_api_key_here" and current_key != "":
            st.markdown('<div class="status-success">✅ API Key Configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ API Key Missing</div>', unsafe_allow_html=True)
        
        if st.session_state.task_running:
            st.markdown('<div class="status-running">🔄 Task Running...</div>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<h1 class="main-header">🤖 Browser Use AI Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #f1f5f9; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
        <strong>Current Setup:</strong> {provider.title()} • {st.session_state.model_name if st.session_state.model_name else "Default Model"}
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
            value=st.session_state.current_task,
            placeholder="Examples:\n• Go to Google and search for 'latest AI news'\n• Visit GitHub and find trending Python repositories\n• Go to weather.com and tell me the weather in New York",
            height=100,
            key="task_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        
        start_button = st.button(
            "🚀 Start Task",
            type="primary",
            disabled=st.session_state.task_running or not task_input.strip(),
            use_container_width=True
        )
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Handle task execution
    if start_button and task_input.strip():
        # Add user message to chat
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "role": "user",
            "content": task_input.strip(),
            "timestamp": timestamp
        })
        
        st.session_state.current_task = task_input.strip()
        st.session_state.task_running = True
        
        # Show running status
        with st.spinner(f"🤖 AI Agent is working on your task using {provider.title()}..."):
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
                else:
                    # Add success message to chat
                    result_text = str(result) if result else "Task completed successfully!"
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"✅ Task completed!\n\n{result_text}",
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"❌ Unexpected error: {str(e)}",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
        
        st.session_state.task_running = False
        st.session_state.current_task = ""
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
    
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(f"📄 {example[:30]}...", key=f"example_{i}", use_container_width=True):
                st.session_state.current_task = example
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
        🤖 Browser Use AI Assistant • Powered by Browser-Use Framework<br>
        <a href="https://github.com/browser-use/browser-use" target="_blank">GitHub</a> • 
        <a href="https://openrouter.ai/docs/quickstart" target="_blank">OpenRouter Docs</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 