from pydantic import BaseModel

class LogoInfo(BaseModel):
    """Information about a logo stored in ActiveStorage."""
    key: str
    filename: str
    content_type: str