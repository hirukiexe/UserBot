import re

# Default prefixes
PREFIXES = r"[@\*\#\$\&\+\!\?\/]{1,2}"  # single or double

def pattern(commands: str, prefixes: str = PREFIXES):
    """
    Create a Telethon regex pattern for multiple commands with optional prefixes.
    Supports multi-line values.

    Args:
        commands (str): command names separated by '|', e.g. "start|nice"
        prefixes (str): regex pattern for prefixes (default: *@#$&+!?/ single or double)

    Returns:
        re.Pattern: compiled regex pattern
    """
    # ^        → start of message
    # (prefix) → group 1: the prefix (@, //, @@ etc.)
    # (commands) → group 2: command name
    # \s*      → optional whitespace
    # (.*)     → group 3: rest of message (multi-line)
    pattern_str = rf"^({prefixes})({commands})\s*(.*)$"

    # re.DOTALL ensures '.' matches newline too
    return re.compile(pattern_str, re.IGNORECASE | re.DOTALL)
