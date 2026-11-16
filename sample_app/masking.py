def mask_secret(value: str, visible: int = 4) -> str:
    """Hide a secret, keeping only the last few characters."""
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]