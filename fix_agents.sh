#!/bin/bash

# Script to fix all call_openai calls to use _call_llm with proper message format

files=(
    "backend/agents/backend_dev_agent.py"
    "backend/agents/frontend_dev_agent.py" 
    "backend/agents/test_dev_agent.py"
    "backend/agents/documentation_agent.py"
    "backend/agents/test_agent.py"
    "backend/agents/backend_agent.py"
    "backend/agents/frontend_agent.py"
)

for file in "${files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "Fixing $file..."
        # Use sed to convert the pattern
        # This is a complex replacement that extracts system messages and converts them
        python3 << EOF
import re

with open('$file', 'r') as f:
    content = f.read()

# Pattern to match the old call format and extract system and user messages
pattern = r'await self\._call_llm\(\[\s*\{"role":\s*"system",\s*"content":\s*"([^"]+)"\},\s*\{"role":\s*"user",\s*"content":\s*([^}]+)\}\s*\]\)'

def replace_func(match):
    system_content = match.group(1)
    user_content = match.group(2)
    return f'await self._call_llm([\n            {{"role": "user", "content": {user_content}}}\n        ], system_prompt="{system_content}")'

content = re.sub(pattern, replace_func, content, flags=re.MULTILINE | re.DOTALL)

with open('$file', 'w') as f:
    f.write(content)
EOF
    fi
done

echo "All files fixed!"
