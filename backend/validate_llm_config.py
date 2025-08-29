#!/usr/bin/env python3
"""
LLM Configuration Validator and Setup Helper
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from config import settings


def validate_openai_config():
    """Validate OpenAI configuration"""
    if not settings.openai_api_key:
        print("❌ OpenAI API Key is missing")
        print("   Set OPENAI_API_KEY in your .env file")
        return False
    
    try:
        from openai import AsyncOpenAI
        print("✅ OpenAI configuration is valid")
        print(f"   Model: {settings.llm_model}")
        return True
    except ImportError:
        print("❌ OpenAI package not installed")
        print("   Run: pip install openai")
        return False


def validate_anthropic_config():
    """Validate Anthropic configuration"""
    if not settings.anthropic_api_key:
        print("❌ Anthropic API Key is missing")
        print("   Set ANTHROPIC_API_KEY in your .env file")
        return False
    
    try:
        import anthropic
        print("✅ Anthropic configuration is valid")
        return True
    except ImportError:
        print("❌ Anthropic package not installed")
        print("   Run: pip install anthropic")
        return False


def validate_azure_config():
    """Validate Azure OpenAI configuration"""
    if not settings.azure_openai_endpoint or not settings.azure_openai_key:
        print("❌ Azure OpenAI configuration is incomplete")
        print("   Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY in your .env file")
        return False
    
    try:
        from openai import AsyncAzureOpenAI
        print("✅ Azure OpenAI configuration is valid")
        return True
    except ImportError:
        print("❌ OpenAI package not installed")
        print("   Run: pip install openai")
        return False


def validate_ollama_config():
    """Validate Ollama configuration"""
    try:
        import aiohttp
        print("✅ Ollama configuration is valid")
        print(f"   Base URL: {settings.ollama_base_url}")
        print(f"   Model: {settings.ollama_model}")
        return True
    except ImportError:
        print("❌ aiohttp package not installed")
        print("   Run: pip install aiohttp")
        return False


def main():
    print("🔧 LLM Configuration Validator")
    print("=" * 40)
    
    print(f"Current LLM Provider: {settings.llm_provider}")
    print(f"Current Model: {settings.llm_model}")
    print(f"Temperature: {settings.llm_temperature}")
    print(f"Max Tokens: {settings.llm_max_tokens}")
    print("-" * 40)
    
    provider = settings.llm_provider.lower()
    
    if provider == "openai":
        is_valid = validate_openai_config()
    elif provider == "anthropic":
        is_valid = validate_anthropic_config()
    elif provider == "azure_openai":
        is_valid = validate_azure_config()
    elif provider == "ollama":
        is_valid = validate_ollama_config()
    else:
        print(f"❌ Unknown provider: {provider}")
        print("   Supported providers: openai, anthropic, azure_openai, ollama")
        is_valid = False
    
    print("-" * 40)
    
    if is_valid:
        print("🎉 Configuration is ready!")
        print("You can now run your engineering team with the configured LLM provider.")
    else:
        print("⚠️  Configuration needs attention.")
        print("Please fix the issues above before running the application.")
        
    print("\n💡 Configuration Examples:")
    print("\nFor OpenAI GPT-4:")
    print("LLM_PROVIDER=openai")
    print("LLM_MODEL=gpt-4-turbo-preview")
    print("OPENAI_API_KEY=your_key_here")
    
    print("\nFor Anthropic Claude:")
    print("LLM_PROVIDER=anthropic")
    print("LLM_MODEL=claude-3-sonnet-20240229")
    print("ANTHROPIC_API_KEY=your_key_here")
    
    print("\nFor Local Ollama:")
    print("LLM_PROVIDER=ollama")
    print("LLM_MODEL=llama2")
    print("OLLAMA_BASE_URL=http://localhost:11434")


if __name__ == "__main__":
    main()
