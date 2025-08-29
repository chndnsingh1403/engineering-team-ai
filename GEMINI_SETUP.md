# LLM Configuration Guide

Your engineering team now supports multiple LLM providers using the OpenAI SDK. Simply configure the `.env` file with your preferred provider.

## 🚀 Quick Start with Gemini (FREE)

### 1. Get Google Gemini API Key (FREE)
1. Visit: https://aistudio.google.com/
2. Sign in with your Google account
3. Click "Get API key" → "Create API key" 
4. Copy your API key

### 2. Update .env file:
```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_API_KEY=your-google-api-key-here
```

## 🎯 Other Provider Options

### OpenAI
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-openai-api-key
```

### Anthropic Claude (via OpenRouter)
```env
LLM_PROVIDER=anthropic
LLM_MODEL=anthropic/claude-3-sonnet-20240229
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=your-openrouter-api-key
```

### Local Ollama
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama2
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=fake-key
```

## 📊 Free Tier Comparison

| Provider | Model | Rate Limits | Cost |
|----------|-------|-------------|------|
| **Gemini** | gemini-1.5-flash | 15 req/min, 1500 req/day | **FREE** |
| **Gemini** | gemini-1.5-pro | 2 req/min, 50 req/day | **FREE** |
| OpenAI | gpt-3.5-turbo | Pay per use | ~$0.002/1K tokens |
| OpenAI | gpt-4 | Pay per use | ~$0.03/1K tokens |
| Ollama | Any model | No limits | **FREE** (local) |

## 🔧 Configuration Options

```env
# Model selection
LLM_MODEL=gemini-1.5-flash  # or gemini-1.5-pro, gpt-4, etc.

# Generation parameters  
LLM_TEMPERATURE=0.7         # Creativity (0.0-1.0)
LLM_MAX_TOKENS=4000        # Response length

# Advanced settings
LLM_BASE_URL=custom-url     # Custom API endpoint
LLM_API_KEY=your-key       # Your API key
```

## ✅ Test Your Setup

1. Update your `.env` file
2. Restart the backend: `npm run dev` (in frontend) and backend server
3. Submit a test project through the web interface
4. Watch the logs for successful LLM calls

## 🚨 Troubleshooting

- **"Invalid API key"**: Check your API key is correct
- **"Rate limit exceeded"**: Switch to a different model or provider
- **"Connection error"**: Verify the base URL is correct

## 💡 Recommendations

- **Start with Gemini 1.5 Flash** - Fast, free, and reliable
- **Use Gemini 1.5 Pro** for complex projects
- **Local Ollama** for privacy-sensitive projects
- **OpenAI GPT-4** for highest quality (paid)
