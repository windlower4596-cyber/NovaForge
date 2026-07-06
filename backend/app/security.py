import re
from fastapi import HTTPException

# Common prompt injection patterns (case-insensitive)
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?instructions",
    r"override\s+(?:all\s+)?settings",
    r"system\s+prompt\s+override",
    r"you\s+are\s+no\s+longer",
    r"forget\s+(?:everything\s+)?before",
    r"new\s+role\s*:",
    r"execute\s+code\s*:",
    r"drop\s+table",
    r"select\s+.*\s+from\s+sqlite",
]

# Allow lists for executable commands if needed in agent execution
ALLOWED_COMMANDS = [
    r"^python\s+backend/mcp_server\.py",
    r"^python\s+cli\.py",
]

def sanitize_input(text: str) -> str:
    """
    Remove HTML tags and escape characters to prevent basic script injection.
    """
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r"<[^>]*>", "", text)
    # Basic character escapes (quotes, brackets)
    clean = clean.replace("<", "&lt;").replace(">", "&gt;")
    return clean.strip()

def detect_prompt_injection(text: str) -> bool:
    """
    Scans input text for potential prompt injection attempts.
    """
    if not text:
        return False
    
    text_lower = text.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
            
    return False

def validate_user_idea(idea: str) -> str:
    """
    Performs full input validation and sanitization.
    Throws HTTPException if validation fails.
    """
    sanitized = sanitize_input(idea)
    
    if len(sanitized) < 10:
        raise HTTPException(
            status_code=400,
            detail="Input idea is too short. Minimum length is 10 characters."
        )
        
    if len(sanitized) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Input idea is too long. Maximum length is 2000 characters."
        )
        
    if detect_prompt_injection(sanitized):
        raise HTTPException(
            status_code=400,
            detail="Security Warning: Potential prompt injection or system override pattern detected."
        )
        
    return sanitized

def verify_command_safety(command: str) -> bool:
    """
    Verifies that a command matches the strict whitelist of safe commands before execution.
    """
    if not command:
        return False
    
    command = command.strip()
    for pattern in ALLOWED_COMMANDS:
        if re.match(pattern, command):
            return True
            
    return False
