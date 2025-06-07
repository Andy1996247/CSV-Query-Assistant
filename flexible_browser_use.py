#!/usr/bin/env python3
"""
Flexible Browser Use Example
This script allows you to choose between different LLM providers and models
through environment variables or interactive selection.
"""

import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession, BrowserProfile

# Load environment variables
load_dotenv()

def create_openai_llm(model_name=None):
    """Create OpenAI LLM instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    model = model_name or os.getenv("OPENAI_MODEL", "gpt-4o")
    return ChatOpenAI(
        model=model,
        temperature=0.0,
        api_key=api_key
    )

def create_anthropic_llm(model_name=None):
    """Create Anthropic (Claude) LLM instance."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        raise ValueError("ANTHROPIC_API_KEY not found or not configured in environment variables")
    
    model = model_name or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")
    return ChatAnthropic(
        model_name=model,
        temperature=0.0,
        timeout=60,
        anthropic_api_key=api_key
    )

def create_google_llm(model_name=None):
    """Create Google (Gemini) LLM instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        raise ValueError("GOOGLE_API_KEY not found or not configured in environment variables")
    
    model = model_name or os.getenv("GOOGLE_MODEL", "gemini-1.5-pro")
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0.0,
        google_api_key=api_key
    )

def create_openrouter_llm(model_name=None):
    """Create OpenRouter LLM instance using OpenAI SDK with custom base URL."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_api_key_here":
        raise ValueError("OPENROUTER_API_KEY not found or not configured in environment variables")
    
    model = model_name or os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
    
    # OpenRouter headers (optional but recommended for rankings)
    extra_headers = {}
    site_url = os.getenv("OPENROUTER_SITE_URL")
    site_name = os.getenv("OPENROUTER_SITE_NAME")
    
    if site_url:
        extra_headers["HTTP-Referer"] = site_url
    if site_name:
        extra_headers["X-Title"] = site_name
    
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model=model,
        temperature=0.0,
        default_headers=extra_headers
    )

def get_available_providers():
    """Get list of available providers based on configured API keys."""
    providers = []
    
    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    
    if os.getenv("ANTHROPIC_API_KEY") and os.getenv("ANTHROPIC_API_KEY") != "your_anthropic_api_key_here":
        providers.append("anthropic")
    
    if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_API_KEY") != "your_google_api_key_here":
        providers.append("google")
    
    if os.getenv("OPENROUTER_API_KEY") and os.getenv("OPENROUTER_API_KEY") != "your_openrouter_api_key_here":
        providers.append("openrouter")
    
    return providers

def create_llm(provider=None, model=None):
    """Create LLM instance based on provider choice."""
    
    if not provider:
        provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    print(f"🤖 Using LLM Provider: {provider.upper()}")
    
    if provider == "openai":
        llm = create_openai_llm(model)
        print(f"📝 Model: {model or os.getenv('OPENAI_MODEL', 'gpt-4o')}")
    elif provider == "anthropic":
        llm = create_anthropic_llm(model)
        print(f"📝 Model: {model or os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20240620')}")
    elif provider == "google":
        llm = create_google_llm(model)
        print(f"📝 Model: {model or os.getenv('GOOGLE_MODEL', 'gemini-1.5-pro')}")
    elif provider == "openrouter":
        llm = create_openrouter_llm(model)
        print(f"📝 Model: {model or os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o')}")
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    
    return llm

def interactive_provider_selection():
    """Interactive provider and model selection."""
    available_providers = get_available_providers()
    
    if not available_providers:
        print("❌ No LLM providers configured. Please set up API keys in your .env file.")
        return None, None
    
    print("🔧 Available LLM Providers:")
    for i, provider in enumerate(available_providers, 1):
        print(f"  {i}. {provider.upper()}")
    
    while True:
        try:
            choice = input(f"\nSelect provider (1-{len(available_providers)}) or press Enter for default ({available_providers[0]}): ").strip()
            if not choice:
                provider = available_providers[0]
                break
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_providers):
                provider = available_providers[choice_idx]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Model selection based on provider
    model_suggestions = {
        "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        "anthropic": ["claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
        "google": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
        "openrouter": ["openai/gpt-4o", "anthropic/claude-3-5-sonnet", "google/gemini-pro", "meta-llama/llama-3.1-405b"]
    }
    
    suggestions = model_suggestions.get(provider, [])
    if suggestions:
        print(f"\n📝 Popular {provider.upper()} models:")
        for i, model in enumerate(suggestions[:4], 1):
            print(f"  {i}. {model}")
        
        model_choice = input(f"\nEnter model name or press Enter for default ({suggestions[0]}): ").strip()
        model = model_choice if model_choice else None
    else:
        model = input("\nEnter model name (or press Enter for default): ").strip() or None
    
    return provider, model

async def run_task_with_llm(task, llm, browser_config=None):
    """Run a browser task with the specified LLM."""
    
    # Create custom browser profile if specified
    if browser_config:
        browser_profile = BrowserProfile(**browser_config)
        browser_session = BrowserSession(browser_profile=browser_profile)
        agent = Agent(task=task, llm=llm, browser_session=browser_session)
    else:
        agent = Agent(task=task, llm=llm)
    
    result = await agent.run()
    return result

async def main():
    """Main function with flexible LLM selection."""
    
    print("🚀 Flexible Browser Use Setup")
    print("=" * 50)
    
    # Check if we should use interactive mode
    use_interactive = os.getenv("INTERACTIVE_MODE", "false").lower() == "true"
    
    if use_interactive:
        provider, model = interactive_provider_selection()
        if not provider:
            return
    else:
        provider = os.getenv("LLM_PROVIDER")
        model = None
    
    try:
        # Create LLM
        llm = create_llm(provider, model)
        
        # Define task
        task = input("\n📋 Enter your browser automation task (or press Enter for default): ").strip()
        if not task:
            task = "Go to https://httpbin.org/get and tell me what my IP address is"
        
        print(f"\n🎯 Task: {task}")
        print("⏳ Starting browser automation...")
        
        # Run task
        result = await run_task_with_llm(task, llm)
        
        print("\n✅ Task completed successfully!")
        print("📋 Result:")
        print("-" * 50)
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your API keys in .env file")
        print("2. Ensure the selected provider is properly configured")
        print("3. Verify the model name is correct for the provider")

def show_configuration_help():
    """Show help for configuring the environment."""
    print("""
🔧 Configuration Help:

Create a .env file with the following variables:

# === API KEYS ===
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  
GOOGLE_API_KEY=your_google_key
OPENROUTER_API_KEY=your_openrouter_key

# === PROVIDER SELECTION ===
LLM_PROVIDER=openai  # or anthropic, google, openrouter

# === MODEL SELECTION ===
OPENAI_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620
GOOGLE_MODEL=gemini-1.5-pro
OPENROUTER_MODEL=openai/gpt-4o

# === INTERACTIVE MODE ===
INTERACTIVE_MODE=true  # Enable interactive provider/model selection

# === OPENROUTER SPECIFIC ===
OPENROUTER_SITE_URL=https://your-site.com
OPENROUTER_SITE_NAME=Your App Name

# === BROWSER USE SETTINGS ===
BROWSER_USE_LOGGING_LEVEL=debug
ANONYMIZED_TELEMETRY=false
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_configuration_help()
    else:
        asyncio.run(main()) 